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
from .sources.http import CatalogUnavailable

SHOW = {
    "id": 2,
    "name": "Cowboy Bebop",
    "premiered": "1998-04-03",
    "genres": ["Anime", "Science-Fiction"],
    "weight": 90,
    "image": {"medium": "https://static.tvmaze.com/bebop.jpg"},
    "summary": "<p>Space <b>bounty</b> hunters.</p>",
    "rating": {"average": 8.9},
    "averageRuntime": 24,
    "webChannel": None,
    "network": {"name": "TV Tokyo", "officialSite": None},
    "officialSite": "https://example.org/bebop",
    "_embedded": {"seasons": [{"number": 1, "episodeOrder": 2}]},
}
EPISODES = [
    {
        "season": 1,
        "number": 1,
        "name": "Asteroid Blues",
        "runtime": 24,
        "airdate": "1998-10-24",
    },
    {
        "season": 1,
        "number": 2,
        "name": "Stray Dog Strut",
        "runtime": 24,
        "airdate": "1998-10-31",
    },
]


def reference(entity_id):
    return {"mainsnak": {"datavalue": {"value": {"id": entity_id}}}}


ENTITIES = {
    "Q1": {
        "id": "Q1",
        "labels": {"de": {"value": "Alien"}},
        "descriptions": {"de": {"value": "Film von Ridley Scott"}},
        "claims": {
            "P31": [reference("Q11424")],
            "P136": [reference("Q200092")],
            "P577": [
                {
                    "mainsnak": {
                        "datavalue": {"value": {"time": "+1979-05-25T00:00:00Z"}}
                    }
                }
            ],
            "P2047": [
                {
                    "mainsnak": {
                        "datavalue": {
                            "value": {
                                "amount": "+7020",
                                "unit": "http://www.wikidata.org/entity/Q11574",
                            }
                        }
                    }
                }
            ],
        },
    },
    "Q200092": {"id": "Q200092", "labels": {"de": {"value": "Horrorfilm"}}},
}


def fake_http(url, ttl, **params):
    if url.endswith("/search/shows"):
        return [{"show": SHOW}]
    if url.endswith("/schedule/web"):
        return [{"_embedded": {"show": SHOW}}]
    if url.endswith("/shows"):
        return [SHOW] if params["page"] == 0 else []
    if url.endswith("/shows/2"):
        return SHOW
    if url.endswith("/shows/2/images"):
        return [
            {
                "type": "background",
                "resolutions": {
                    "original": {"url": "https://static.tvmaze.com/bg.jpg"}
                },
            }
        ]
    if url.endswith("/shows/2/episodes"):
        return EPISODES
    if params.get("list") == "search":
        return {"query": {"search": [{"title": "Q1"}]}}
    if params.get("action") == "wbgetentities":
        ids = params["ids"].split("|")
        return {
            "entities": {
                entity: ENTITIES[entity] for entity in ids if entity in ENTITIES
            }
        }
    return {
        "results": {
            "bindings": [
                {
                    "film": {"value": "http://www.wikidata.org/entity/Q1"},
                    "popularity": {"value": "100"},
                }
            ]
        }
    }


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


def media_file(**identity):
    return MediaFile.objects.create(
        **{
            "media_type": "tv",
            "catalog_id": 2,
            "season": 1,
            "episode": 1,
            "title": "Cowboy Bebop",
            "path": "shows/Cowboy Bebop (1998)/Season 01/Cowboy Bebop S01E01.mp4",
            **identity,
        }
    )


@patch("lumon.sources.http.get", side_effect=fake_http)
class CatalogTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(create_user("admin"))

    def test_non_admin_is_forbidden(self, http):
        self.client.force_authenticate(create_user("guest", admin=False))
        self.assertEqual(self.client.get("/api/lumon/catalog/search/").status_code, 403)

    def test_categories_are_listed(self, http):
        response = self.client.get("/api/lumon/catalog/categories/")
        self.assertEqual(
            [category["label"] for category in response.data],
            ["Sci-Fi", "Anime", "Horror", "Komödie"],
        )

    def test_search_combines_films_and_series_and_marks_saved(self, http):
        saved = Title.objects.create(catalog_id=1, media_type="movie", title="Alien")
        response = self.client.get("/api/lumon/catalog/search/?q=alien")
        self.assertEqual(
            [(item["title"], item["media_type"]) for item in response.data],
            [("Alien", "movie"), ("Cowboy Bebop", "tv")],
        )
        self.assertEqual(response.data[0]["saved"], str(saved.uuid))
        self.assertEqual(
            response.data[0]["poster"], "/api/lumon/catalog/movie/1/poster/"
        )
        self.assertEqual(
            response.data[1]["poster"], "https://static.tvmaze.com/bebop.jpg"
        )

    def test_search_filters_by_category(self, http):
        response = self.client.get("/api/lumon/catalog/search/?q=a&category=anime")
        self.assertEqual([item["title"] for item in response.data], ["Cowboy Bebop"])

    def test_category_without_query_lists_matching_titles(self, http):
        response = self.client.get("/api/lumon/catalog/search/?category=horror")
        self.assertEqual([item["title"] for item in response.data], ["Alien"])

    def test_unknown_category_is_rejected(self, http):
        response = self.client.get("/api/lumon/catalog/search/?category=western")
        self.assertEqual(response.status_code, 400)

    def test_browse_lists_rows_and_featured_title(self, http):
        Title.objects.create(catalog_id=2, media_type="tv", title="Cowboy Bebop")
        response = self.client.get("/api/lumon/catalog/browse/tv/")
        self.assertEqual(
            [row["key"] for row in response.data["rows"]],
            ["library", "popular", "sci-fi", "anime", "horror", "comedy"],
        )
        self.assertEqual(response.data["featured"]["channel"]["name"], "TV Tokyo")

    def test_unavailable_source_leaves_rows_empty(self, http):
        http.side_effect = CatalogUnavailable()
        response = self.client.get("/api/lumon/catalog/browse/movie/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual({len(row["items"]) for row in response.data["rows"]}, {0})
        self.assertIsNone(response.data["featured"])

    def test_series_detail_from_tvmaze(self, http):
        response = self.client.get("/api/lumon/catalog/tv/2/")
        self.assertEqual(response.data["overview"], "Space bounty hunters.")
        self.assertEqual(
            response.data["seasons"],
            [{"number": 1, "name": "Staffel 1", "episodes": 2}],
        )
        self.assertEqual(response.data["backdrop"], "https://static.tvmaze.com/bg.jpg")

    def test_film_detail_from_wikidata(self, http):
        response = self.client.get("/api/lumon/catalog/movie/1/")
        self.assertEqual((response.data["year"], response.data["runtime"]), (1979, 117))
        self.assertEqual(response.data["genres"], ["Horrorfilm"])
        self.assertEqual(
            response.data["backdrop"], "/api/lumon/catalog/movie/1/backdrop/"
        )
        self.assertIsNone(response.data["channel"])

    def test_film_poster_is_generated(self, http):
        response = self.client.get("/api/lumon/catalog/movie/1/poster/")
        self.assertEqual(response["Content-Type"], "image/svg+xml")
        self.assertIn("Alien", response.content.decode())

    def test_saving_a_title_fills_it_from_the_catalog(self, http):
        response = self.client.post(
            "/api/lumon/titles/",
            {"catalog_id": 1, "media_type": "movie"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        title = Title.objects.get()
        self.assertEqual(
            (title.title, title.year, title.poster),
            ("Alien", 1979, "/api/lumon/catalog/movie/1/poster/"),
        )

    def test_removing_a_title(self, http):
        title = Title.objects.create(catalog_id=1, media_type="movie", title="Alien")
        self.assertEqual(
            self.client.delete(f"/api/lumon/titles/{title.uuid}/").status_code, 204
        )
        self.assertFalse(Title.objects.exists())


@patch("lumon.sources.http.get", side_effect=fake_http)
class MediaLibraryTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(create_user("admin"))

    def test_browse_starts_with_media_library(self, http):
        media_file(
            media_type="movie", catalog_id=1, season=None, episode=None, title="Alien"
        )
        response = self.client.get("/api/lumon/catalog/browse/movie/")
        self.assertEqual(response.data["rows"][0]["key"], "media")
        self.assertEqual(response.data["rows"][0]["items"][0]["catalog_id"], 1)
        self.assertIsNotNone(response.data["featured"]["media"])

    def test_movie_detail_offers_playback_with_position(self, http):
        movie = media_file(
            media_type="movie",
            catalog_id=1,
            season=None,
            episode=None,
            title="Alien",
            position=600,
        )
        response = self.client.get("/api/lumon/catalog/movie/1/")
        self.assertEqual(response.data["media"]["id"], str(movie.uuid))
        self.assertEqual(response.data["media"]["position"], 600)

    def test_series_detail_offers_next_unwatched_episode(self, http):
        media_file(played=True)
        second = media_file(episode=2, path="shows/x/Season 01/x S01E02.mp4")
        response = self.client.get("/api/lumon/catalog/tv/2/")
        self.assertEqual(response.data["media"]["id"], str(second.uuid))
        self.assertEqual(response.data["media"]["subtitle"], "S01E02")

    def test_season_marks_available_episodes(self, http):
        episode = media_file(played=True)
        response = self.client.get("/api/lumon/catalog/tv/2/seasons/1/")
        self.assertEqual(response.data[0]["title"], "Asteroid Blues")
        self.assertEqual(response.data[0]["media"]["id"], str(episode.uuid))
        self.assertTrue(response.data[0]["media"]["played"])
        self.assertIsNone(response.data[1]["media"])

    def test_playback_streams_the_file_directly(self, http):
        episode = media_file()
        following = media_file(episode=2, path="shows/x/Season 01/x S01E02.mp4")
        response = self.client.get(f"/api/lumon/media/{episode.uuid}/")
        self.assertEqual(
            response.data["stream"],
            "/lumon-media/shows/Cowboy%20Bebop%20%281998%29/Season%2001/Cowboy%20Bebop%20S01E01.mp4",
        )
        self.assertEqual(response.data["next"], str(following.uuid))

    def test_last_episode_has_no_next(self, http):
        episode = media_file()
        self.assertIsNone(
            self.client.get(f"/api/lumon/media/{episode.uuid}/").data["next"]
        )

    def test_progress_is_stored(self, http):
        episode = media_file()
        response = self.client.post(
            f"/api/lumon/media/{episode.uuid}/progress/",
            {"position": 90, "duration": 1440},
            format="json",
        )
        self.assertEqual(response.status_code, 204)
        episode.refresh_from_db()
        self.assertEqual((episode.position, episode.duration), (90, 1440))

    def test_stream_auth_requires_admin(self, http):
        self.assertEqual(self.client.get("/api/lumon/media/auth/").status_code, 204)
        self.client.force_authenticate(create_user("guest", admin=False))
        self.assertEqual(self.client.get("/api/lumon/media/auth/").status_code, 403)

    def test_detects_known_episodes_and_marks_existing(self, http):
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


@patch("lumon.sources.http.get", side_effect=fake_http)
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
                "catalog_id": 1,
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

    def test_movie_upload_is_playable_right_away(self, http):
        uuid = self.start().data["uuid"]
        self.send(uuid, 0, b"abc")
        self.assertEqual(self.send(uuid, 3, b"def").data["received"], 6)
        response = self.complete(uuid)
        folder = Path(self.root.name, "movies", "Alien (1979)")
        self.assertEqual((folder / "Alien (1979).mp4").read_bytes(), b"abcdef")
        self.assertIn(
            '<uniqueid type="wikidata" default="true">Q1</uniqueid>',
            (folder / "movie.nfo").read_text(),
        )
        self.assertEqual(response.data["id"], str(MediaFile.objects.get().uuid))
        self.assertFalse(Upload.objects.exists())

    def test_episode_upload_uses_season_folder(self, http):
        uuid = self.start(
            media_type="tv", catalog_id=2, season=1, episode=3, size=1
        ).data["uuid"]
        self.send(uuid, 0, b"x")
        self.complete(uuid)
        media = MediaFile.objects.get()
        self.assertEqual(
            media.path, "shows/Cowboy Bebop (1998)/Season 01/Cowboy Bebop S01E03.mp4"
        )
        self.assertTrue(Path(self.root.name, media.path).exists())

    def test_replacing_a_video_removes_the_old_file(self, http):
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

    def test_episode_needs_season_and_number(self, http):
        self.assertEqual(self.start(media_type="tv").status_code, 400)

    def test_unknown_extension_is_rejected(self, http):
        self.assertEqual(self.start(filename="alien.exe").status_code, 400)

    def test_chunk_at_wrong_offset_is_rejected(self, http):
        uuid = self.start().data["uuid"]
        self.assertEqual(self.send(uuid, 3, b"def").status_code, 400)

    def test_incomplete_upload_cannot_complete(self, http):
        uuid = self.start().data["uuid"]
        self.send(uuid, 0, b"abc")
        self.assertEqual(self.complete(uuid).status_code, 400)

    def test_cancelled_upload_removes_partial_file(self, http):
        uuid = self.start().data["uuid"]
        self.send(uuid, 0, b"abc")
        self.client.delete(f"/api/lumon/uploads/{uuid}/")
        self.assertEqual(list(Path(self.root.name, ".uploads").iterdir()), [])

    def test_scan_registers_videos_by_nfo(self, http):
        season = Path(self.root.name, "shows", "Bebop", "Season 01")
        season.mkdir(parents=True)
        (season.parent / "tvshow.nfo").write_text(
            library.nfo("tvshow", "Bebop", 1998, 2)
        )
        (season / "Bebop S01E04.mkv").write_bytes(b"x")
        film = Path(self.root.name, "movies", "Alien (1979)")
        film.mkdir(parents=True)
        (film / "movie.nfo").write_text(library.nfo("movie", "Alien", 1979, 1))
        (film / "Alien (1979).mp4").write_bytes(b"x")
        call_command("scan_media", stdout=StringIO())
        self.assertEqual(
            sorted(
                MediaFile.objects.values_list(
                    "media_type", "catalog_id", "season", "episode"
                )
            ),
            [("movie", 1, None, None), ("tv", 2, 1, 4)],
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
