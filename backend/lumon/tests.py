from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.management import call_command
from django.test import SimpleTestCase, override_settings
from rest_framework.test import APITestCase

from wintersehn.accounts.models import UserProfile

from . import catalog, library
from .models import MediaFile, Title, Upload

MOVIE = {
    "id": 1,
    "title": "Alien",
    "release_date": "1979-05-25",
    "poster_path": "/alien.jpg",
    "genre_ids": [27, 878],
    "original_language": "en",
}
SERIES = {
    "id": 2,
    "name": "Cowboy Bebop",
    "first_air_date": "1998-04-03",
    "poster_path": "/bebop.jpg",
    "genre_ids": [16, 10765],
    "original_language": "ja",
}
DETAIL = {
    **MOVIE,
    "overview": "Im Weltraum hört dich niemand schreien.",
    "backdrop_path": "/alien-wide.jpg",
    "genres": [{"id": 27, "name": "Horror"}],
    "vote_average": 8.16,
    "vote_count": 100,
    "runtime": 117,
    "watch/providers": {
        "results": {
            "CH": {
                "link": "https://www.themoviedb.org/movie/1/watch?locale=CH",
                "flatrate": [{"provider_name": "Disney Plus", "logo_path": "/d.jpg"}],
            }
        }
    },
}


def fake_get(path, **params):
    if path == "/search/multi":
        return {
            "results": [
                {**MOVIE, "media_type": "movie"},
                {**SERIES, "media_type": "tv"},
                {"id": 3, "name": "Person", "media_type": "person"},
            ]
        }
    if path == "/discover/movie":
        return {"results": [MOVIE]}
    if path == "/discover/tv":
        return {"results": [SERIES]}
    if path.endswith("/popular"):
        return {"results": [MOVIE]}
    if path == "/trending/all/week":
        return {"results": [{**SERIES, "media_type": "tv"}]}
    return DETAIL


def create_user(username, admin=True):
    user = get_user_model().objects.create_user(username)
    UserProfile.objects.create(user=user, verified=True)
    if admin:
        user.user_permissions.add(
            Permission.objects.get(
                codename="view_admin", content_type__app_label="content"
            )
        )
    return user


@override_settings(TMDB_API_KEY="test")
@patch("lumon.tmdb.get", side_effect=fake_get)
class LumonTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(create_user("admin"))

    def test_non_admin_is_forbidden(self, tmdb):
        self.client.force_authenticate(create_user("guest", admin=False))
        self.assertEqual(self.client.get("/api/lumon/catalog/search/").status_code, 403)

    def test_search_skips_people_and_marks_saved_titles(self, tmdb):
        saved = Title.objects.create(tmdb_id=1, media_type="movie", title="Alien")
        response = self.client.get("/api/lumon/catalog/search/?q=alien")
        self.assertEqual(
            [(item["title"], item["media_type"]) for item in response.data],
            [("Alien", "movie"), ("Cowboy Bebop", "tv")],
        )
        self.assertEqual(response.data[0]["saved"], str(saved.uuid))
        self.assertEqual(response.data[0]["year"], 1979)
        self.assertEqual(
            response.data[0]["poster"], "https://image.tmdb.org/t/p/w342/alien.jpg"
        )

    def test_search_filters_query_by_category(self, tmdb):
        response = self.client.get("/api/lumon/catalog/search/?q=a&category=anime")
        self.assertEqual([item["title"] for item in response.data], ["Cowboy Bebop"])

    def test_category_without_query_skips_types_without_genre(self, tmdb):
        response = self.client.get("/api/lumon/catalog/search/?category=horror")
        self.assertEqual([item["media_type"] for item in response.data], ["movie"])

    def test_unknown_category_is_rejected(self, tmdb):
        response = self.client.get("/api/lumon/catalog/search/?category=western")
        self.assertEqual(response.status_code, 400)

    def test_browse_starts_with_library_row(self, tmdb):
        Title.objects.create(tmdb_id=2, media_type="tv", title="Cowboy Bebop")
        response = self.client.get("/api/lumon/catalog/browse/tv/")
        self.assertEqual(
            [row["key"] for row in response.data["rows"]],
            ["library", "popular", "sci-fi", "anime", "comedy"],
        )

    def test_detail_lists_swiss_providers(self, tmdb):
        response = self.client.get("/api/lumon/catalog/movie/1/")
        self.assertEqual(response.data["rating"], 8.2)
        self.assertEqual(
            response.data["providers"]["flatrate"][0]["name"], "Disney Plus"
        )
        self.assertEqual(response.data["providers"]["rent"], [])

    def test_saving_a_title_fills_it_from_tmdb(self, tmdb):
        response = self.client.post(
            "/api/lumon/titles/", {"tmdb_id": 1, "media_type": "movie"}
        )
        self.assertEqual(response.status_code, 201)
        title = Title.objects.get()
        self.assertEqual(
            (title.title, title.year, title.poster_path), ("Alien", 1979, "/alien.jpg")
        )

    def test_removing_a_title(self, tmdb):
        title = Title.objects.create(tmdb_id=1, media_type="movie", title="Alien")
        response = self.client.delete(f"/api/lumon/titles/{title.uuid}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Title.objects.exists())


class TmdbKeyTests(APITestCase):
    @override_settings(TMDB_API_KEY="")
    def test_missing_key_reports_unavailable(self):
        self.client.force_authenticate(create_user("admin"))
        response = self.client.get("/api/lumon/catalog/search/")
        self.assertEqual(response.status_code, 502)

    def test_fake_posters_are_unavailable_outside_debug(self):
        response = self.client.get("/api/lumon/fake/posters/101.svg")
        self.assertEqual(response.status_code, 404)


SEASON = {
    "episodes": [
        {"episode_number": 1, "name": "Asteroid Blues", "runtime": 24},
        {"episode_number": 2, "name": "Stray Dog Strut", "runtime": 24},
    ]
}


def fake_tmdb_with_seasons(path, **params):
    if path == "/tv/2/season/1":
        return SEASON
    if path == "/tv/2":
        return {
            **SERIES,
            "seasons": [{"season_number": 1, "name": "Staffel 1", "episode_count": 2}],
        }
    return fake_get(path, **params)


def media_file(**identity):
    return MediaFile.objects.create(
        **{
            "media_type": "tv",
            "tmdb_id": 2,
            "season": 1,
            "episode": 1,
            "title": "Cowboy Bebop",
            "path": "shows/Cowboy Bebop (1998)/Season 01/Cowboy Bebop S01E01.mp4",
            **identity,
        }
    )


@override_settings(TMDB_API_KEY="test")
@patch("lumon.tmdb.get", side_effect=fake_tmdb_with_seasons)
class MediaLibraryTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(create_user("admin"))

    def test_browse_starts_with_media_library(self, tmdb):
        media_file(
            media_type="movie", tmdb_id=1, season=None, episode=None, title="Alien"
        )
        response = self.client.get("/api/lumon/catalog/browse/movie/")
        self.assertEqual(response.data["rows"][0]["key"], "media")
        self.assertEqual(response.data["rows"][0]["items"][0]["tmdb_id"], 1)
        self.assertEqual(response.data["featured"]["tmdb_id"], 1)
        self.assertIsNotNone(response.data["featured"]["media"])

    def test_movie_detail_offers_playback_with_position(self, tmdb):
        movie = media_file(
            media_type="movie",
            tmdb_id=1,
            season=None,
            episode=None,
            title="Alien",
            position=600,
        )
        response = self.client.get("/api/lumon/catalog/movie/1/")
        self.assertEqual(response.data["media"]["id"], str(movie.uuid))
        self.assertEqual(response.data["media"]["position"], 600)

    def test_series_detail_offers_next_unwatched_episode(self, tmdb):
        media_file(played=True)
        second = media_file(episode=2, path="shows/x/Season 01/x S01E02.mp4")
        response = self.client.get("/api/lumon/catalog/tv/2/")
        self.assertEqual(response.data["media"]["id"], str(second.uuid))
        self.assertEqual(response.data["media"]["subtitle"], "S01E02")

    def test_season_marks_available_episodes(self, tmdb):
        episode = media_file(played=True)
        response = self.client.get("/api/lumon/catalog/tv/2/seasons/1/")
        self.assertEqual(response.data[0]["media"]["id"], str(episode.uuid))
        self.assertTrue(response.data[0]["media"]["played"])
        self.assertIsNone(response.data[1]["media"])

    def test_playback_streams_the_file_directly(self, tmdb):
        episode = media_file()
        following = media_file(episode=2, path="shows/x/Season 01/x S01E02.mp4")
        response = self.client.get(f"/api/lumon/media/{episode.uuid}/")
        self.assertEqual(
            response.data["stream"],
            "/lumon-media/shows/Cowboy%20Bebop%20%281998%29/Season%2001/Cowboy%20Bebop%20S01E01.mp4",
        )
        self.assertEqual(response.data["subtitle"], "S01E01")
        self.assertEqual(response.data["next"], str(following.uuid))

    def test_last_episode_has_no_next(self, tmdb):
        episode = media_file()
        self.assertIsNone(
            self.client.get(f"/api/lumon/media/{episode.uuid}/").data["next"]
        )

    def test_progress_is_stored(self, tmdb):
        episode = media_file()
        response = self.client.post(
            f"/api/lumon/media/{episode.uuid}/progress/",
            {"position": 90, "duration": 1440},
            format="json",
        )
        self.assertEqual(response.status_code, 204)
        episode.refresh_from_db()
        self.assertEqual((episode.position, episode.duration), (90, 1440))

    def test_stream_auth_requires_admin(self, tmdb):
        self.assertEqual(self.client.get("/api/lumon/media/auth/").status_code, 204)
        self.client.force_authenticate(create_user("guest", admin=False))
        self.assertEqual(self.client.get("/api/lumon/media/auth/").status_code, 403)


@override_settings(TMDB_API_KEY="test")
@patch("lumon.tmdb.get", side_effect=fake_get)
class UploadTests(APITestCase):
    def setUp(self):
        self.root = TemporaryDirectory()
        self.addCleanup(self.root.cleanup)
        self.enterContext(override_settings(LUMON_MEDIA_ROOT=self.root.name))
        self.client.force_authenticate(create_user("admin"))

    def start(self, **data):
        return self.client.post(
            "/api/lumon/uploads/",
            {
                "media_type": "movie",
                "tmdb_id": 1,
                "filename": "alien.MP4",
                "size": 6,
                **data,
            },
            format="json",
        )

    def send(self, uuid, offset, chunk):
        return self.client.put(
            f"/api/lumon/uploads/{uuid}/chunk/?offset={offset}",
            chunk,
            content_type="application/octet-stream",
        )

    def complete(self, uuid):
        return self.client.post(f"/api/lumon/uploads/{uuid}/complete/")

    def test_movie_upload_is_playable_right_away(self, tmdb):
        uuid = self.start().data["uuid"]
        self.send(uuid, 0, b"abc")
        self.assertEqual(self.send(uuid, 3, b"def").data["received"], 6)
        response = self.complete(uuid)
        folder = Path(self.root.name, "movies", "Alien (1979)")
        self.assertEqual((folder / "Alien (1979).mp4").read_bytes(), b"abcdef")
        self.assertIn(
            '<uniqueid type="tmdb" default="true">1</uniqueid>',
            (folder / "movie.nfo").read_text(),
        )
        self.assertEqual(response.data["id"], str(MediaFile.objects.get().uuid))
        self.assertFalse(Upload.objects.exists())

    def test_episode_upload_uses_season_folder(self, tmdb):
        uuid = self.start(media_type="tv", tmdb_id=2, season=1, episode=3, size=1).data[
            "uuid"
        ]
        self.send(uuid, 0, b"x")
        self.complete(uuid)
        media = MediaFile.objects.get()
        self.assertEqual(media.path, "shows/Alien (1979)/Season 01/Alien S01E03.mp4")
        self.assertTrue(Path(self.root.name, media.path).exists())

    def test_replacing_a_video_removes_the_old_file(self, tmdb):
        first = self.start(filename="alien.mkv", size=1).data["uuid"]
        self.send(first, 0, b"x")
        self.complete(first)
        second = self.start(size=1).data["uuid"]
        self.send(second, 0, b"y")
        self.complete(second)
        folder = Path(self.root.name, "movies", "Alien (1979)")
        self.assertFalse((folder / "Alien (1979).mkv").exists())
        self.assertEqual(
            MediaFile.objects.get().path, "movies/Alien (1979)/Alien (1979).mp4"
        )

    def test_episode_needs_season_and_number(self, tmdb):
        self.assertEqual(self.start(media_type="tv").status_code, 400)

    def test_unknown_extension_is_rejected(self, tmdb):
        self.assertEqual(self.start(filename="alien.exe").status_code, 400)

    def test_chunk_at_wrong_offset_is_rejected(self, tmdb):
        uuid = self.start().data["uuid"]
        self.assertEqual(self.send(uuid, 3, b"def").status_code, 400)

    def test_incomplete_upload_cannot_complete(self, tmdb):
        uuid = self.start().data["uuid"]
        self.send(uuid, 0, b"abc")
        self.assertEqual(self.complete(uuid).status_code, 400)

    def test_cancelled_upload_removes_partial_file(self, tmdb):
        uuid = self.start().data["uuid"]
        self.send(uuid, 0, b"abc")
        self.client.delete(f"/api/lumon/uploads/{uuid}/")
        self.assertEqual(list(Path(self.root.name, ".uploads").iterdir()), [])

    def test_scan_registers_videos_by_nfo(self, tmdb):
        show = Path(self.root.name, "shows", "Bebop", "Season 01")
        show.mkdir(parents=True)
        (show.parent / "tvshow.nfo").write_text(library.nfo("tvshow", "Bebop", 1998, 2))
        (show / "Bebop S01E04.mkv").write_bytes(b"x")
        call_command("scan_media", stdout=StringIO())
        self.assertEqual(
            list(MediaFile.objects.values_list("tmdb_id", "season", "episode")),
            [(2, 1, 4)],
        )


class EpisodeParsingTests(SimpleTestCase):
    def test_reads_common_episode_names(self):
        cases = {
            "Orbitwache.S02E05.1080p.mkv": (2, 5),
            "orbitwache 1x03.mp4": (1, 3),
            "Staffel 3 - Folge 12.mp4": (3, 12),
            "Folge 7.mp4": (4, 7),
            "trailer.mp4": (4, None),
        }
        for filename, expected in cases.items():
            with self.subTest(filename):
                self.assertEqual(catalog.parse_episode(filename, 4), expected)


@override_settings(TMDB_API_KEY="test")
@patch("lumon.tmdb.get", side_effect=fake_tmdb_with_seasons)
class DetectTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(create_user("admin"))

    def test_detects_known_episodes_and_marks_existing(self, tmdb):
        media_file()
        response = self.client.post(
            "/api/lumon/catalog/tv/2/detect/",
            {"filenames": ["Bebop S01E01.mkv", "Bebop S01E02.mkv", "Bebop S09E01.mkv"]},
            format="json",
        )
        self.assertEqual(
            [
                (item["season"], item["episode"], item["exists"])
                for item in response.data
            ],
            [(1, 1, True), (1, 2, False), (None, None, False)],
        )
        self.assertEqual(response.data[1]["title"], "Stray Dog Strut")
