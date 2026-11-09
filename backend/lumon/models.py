import uuid
from urllib.parse import quote

from django.db import models
from django.db.models import Max, Q

from . import library


class TitleQuerySet(models.QuerySet):
    def saved(self):
        return {
            (media_type, catalog_id): key
            for media_type, catalog_id, key in self.values_list(
                "media_type", "catalog_id", "uuid"
            )
        }


class Title(models.Model):
    MOVIE = "movie"
    TV = "tv"
    MEDIA_TYPES = [(MOVIE, "Film"), (TV, "Serie")]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    catalog_id = models.PositiveIntegerField()
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    title = models.CharField(max_length=255)
    poster = models.CharField(max_length=500, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = TitleQuerySet.as_manager()

    class Meta:
        ordering = ["-added_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["catalog_id", "media_type"], name="lumon_unique_title"
            )
        ]

    def __str__(self):
        return self.title


class MediaFileQuerySet(models.QuerySet):
    def library(self, media_type):
        return (
            self.filter(media_type=media_type)
            .values_list("catalog_id", flat=True)
            .annotate(latest=Max("uploaded_at"))
            .order_by("-latest")
        )

    def movie(self, catalog_id):
        return self.filter(media_type=Title.MOVIE, catalog_id=catalog_id).first()

    def register(self, path, **identity):
        relative = str(path.relative_to(library.root()))
        media = self.filter(
            **{
                key: identity[key]
                for key in ("media_type", "catalog_id", "season", "episode")
            }
        ).first()
        if media and media.path != relative:
            (library.root() / media.path).unlink(missing_ok=True)
        if media:
            media.path, media.title = relative, identity["title"]
            media.duration = media.position = 0
            media.played = False
            media.save()
            return media
        return self.create(path=relative, **identity)

    def next_up(self, catalog_id):
        episodes = self.filter(media_type=Title.TV, catalog_id=catalog_id)
        return episodes.filter(played=False).first() or episodes.first()

    def episodes(self, catalog_id, season):
        return {
            media.episode: media
            for media in self.filter(
                media_type=Title.TV, catalog_id=catalog_id, season=season
            )
        }


class MediaFile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    media_type = models.CharField(max_length=5, choices=Title.MEDIA_TYPES)
    catalog_id = models.PositiveIntegerField()
    season = models.PositiveSmallIntegerField(null=True, blank=True)
    episode = models.PositiveSmallIntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    path = models.CharField(max_length=500)
    duration = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(default=0)
    played = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now=True)

    objects = MediaFileQuerySet.as_manager()

    class Meta:
        ordering = ["catalog_id", "season", "episode"]
        constraints = [
            models.UniqueConstraint(
                fields=["media_type", "catalog_id", "season", "episode"],
                name="lumon_unique_media_file",
                nulls_distinct=False,
            )
        ]

    def __str__(self):
        return self.path

    @property
    def stream(self):
        return f"/lumon-media/{quote(self.path)}"

    @property
    def subtitle(self):
        if self.media_type == Title.MOVIE:
            return ""
        return f"S{self.season:02d}E{self.episode:02d}"

    @property
    def following(self):
        if self.media_type == Title.MOVIE:
            return None
        return (
            MediaFile.objects.filter(media_type=Title.TV, catalog_id=self.catalog_id)
            .filter(
                Q(season=self.season, episode__gt=self.episode)
                | Q(season__gt=self.season)
            )
            .first()
        )


class UploadError(Exception):
    pass


class Upload(models.Model):
    EXTENSIONS = ["mp4", "m4v", "webm", "mkv", "mov"]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    media_type = models.CharField(max_length=5, choices=Title.MEDIA_TYPES)
    catalog_id = models.PositiveIntegerField()
    season = models.PositiveSmallIntegerField(null=True, blank=True)
    episode = models.PositiveSmallIntegerField(null=True, blank=True)
    extension = models.CharField(max_length=4)
    size = models.PositiveBigIntegerField()
    received = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} {self.catalog_id}"

    @property
    def partial(self):
        return library.root() / ".uploads" / f"{self.uuid}.part"

    def append(self, stream, offset):
        if offset != self.received:
            raise UploadError("Unerwartete Position im Upload.")
        self.partial.parent.mkdir(parents=True, exist_ok=True)
        with self.partial.open("ab") as target:
            while chunk := stream.read(1024 * 1024):
                self.received += len(chunk)
                if self.received > self.size:
                    raise UploadError("Die Datei ist grösser als angekündigt.")
                target.write(chunk)
        self.save(update_fields=["received"])

    def target(self, fields):
        if self.media_type == Title.MOVIE:
            return library.movie_path(fields, self.catalog_id, self.extension)
        return library.episode_path(
            fields, self.catalog_id, self.season, self.episode, self.extension
        )

    def complete(self, fields):
        if self.received != self.size:
            raise UploadError("Der Upload ist noch nicht vollständig.")
        path, nfo_path, nfo = self.target(fields)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not nfo_path.exists():
            nfo_path.write_text(nfo)
        self.partial.replace(path)
        media = MediaFile.objects.register(
            path,
            media_type=self.media_type,
            catalog_id=self.catalog_id,
            season=self.season,
            episode=self.episode,
            title=fields["title"],
        )
        self.delete()
        return media

    def discard(self):
        self.partial.unlink(missing_ok=True)
        self.delete()
