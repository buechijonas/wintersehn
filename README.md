# wintersehn

Self-hosted platform behind wintersehn.ch: six Vue frontends, one Django backend and a private search, all running on a single server. The architecture, principles and a few solved problems are shown on the Engineering page of wintersehn.ch.

```
backend/            Django project serving the API for all apps
  commons/          shared base: models, querysets with apply_acl, serializers, viewsets,
                    permissions, HTTP client, images, Markdown, test fixtures
  wintersehn/       content (pages, roles, dashboard) and accounts (govex login, consent)
  search/           search settings, child protection, host ratings
  atlas/            institutions, subjects, documentations, learning sets, exams
  lumon/            movie and series catalog (TVmaze, Wikidata), own media library
  monolith/         encrypted dossiers, events, trust and sharing
frontend/
  core/             shared layout, components, auth and settings (@core/…)
  wintersehn/       wintersehn.ch
  home/             home.wintersehn.ch
  search/           search.wintersehn.ch
  atlas/            atlas.wintersehn.ch
  lumon/            lumon.wintersehn.ch
  monolith/         monolith.wintersehn.ch
docker/
  proxy/            Caddy edge and origin config, production image with all frontends
  searxng/          SearXNG image, settings and the query guard plugin
  tor/              Tor image with watchdog used by SearXNG
bin/                release and deploy scripts
```

## Stack

Vue 3, Pinia, Vite, Tailwind CSS 4 and daisyUI in the frontends. Django 6, Django REST Framework and PostgreSQL in the backend. SearXNG over Tor for the search. Caddy, Anubis and Docker Compose in production. Sign-in for all apps goes through govex (OIDC).

## Development

```sh
docker compose up -d --build
docker compose exec backend python manage.py test
```

| App        | URL                   |
| ---------- | --------------------- |
| atlas      | http://localhost:5169 |
| home       | http://localhost:5170 |
| search     | http://localhost:5171 |
| monolith   | http://localhost:5172 |
| wintersehn | http://localhost:5173 |
| lumon      | http://localhost:5177 |
| backend    | http://localhost:8000 |

Local LUMON videos live in `lumon-media/` (ignored by git). `python manage.py scan_media` registers files copied there by hand, `python manage.py warm_catalog` preloads the catalog cache.

## Conventions

`commons/tests.py` checks every rule marked with ✓ on each test run.

- Logic lives in the backend, the frontends only render.
- ✓ Every view builds on `BaseViewSet` from `commons`, next to `UUIDModel`, querysets with `apply_acl(user)` and serializer groups with `read`, `list`, `retrieve` and `write`.
- ✓ No `getattr`, `setattr`, `hasattr` or `isinstance`.
- ✓ No comments, unless something is really unclear without one.
- ✓ Choice values in English, as are code and identifiers; only the UI text is German.
- ✓ Small pure functions and comprehensions, at most two nested blocks.
- ✓ A `models.py` over 500 lines becomes a `models/` package split by domain.
- ✓ Data lives in `.txt` or `.json` files next to the code, not in Python literals.
- ✓ Everything stored on the client or in the cache is namespaced with `wntrs`: cookies (`wntrs_session`), browser storage (`wntrs-theme`), cache keys (`KEY_PREFIX = "wntrs"`) and design tokens (`wntrs-muted`).
- ✓ Outgoing requests go through `commons.http` and identify as `wintersehn`.

## Release and deploy

```sh
bin/release        # builds and pushes the backend, proxy, SearXNG and Tor images
./deploy           # on the server: zero-downtime backend swap, then the other services
```
