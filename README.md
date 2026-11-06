# wintersehn

```
backend/            Django API for all apps
frontend/
  core/             shared layout, components, auth and settings (@core/…)
  wintersehn/       wintersehn.ch
  monolith/         monolith.wintersehn.ch
  search/           search.wintersehn.ch
  home/             home.wintersehn.ch
  atlas/            atlas.wintersehn.ch
docker/
  proxy/            Caddy edge and origin config, production image with all frontends
  searxng/          SearXNG image and settings used by search
  tor/              Tor image SearXNG uses in production
bin/                release and deploy scripts
docs/               documents
```

```sh
docker compose up -d --build
```

| App        | URL                          |
| ---------- | ---------------------------- |
| atlas      | http://localhost:5169        |
| home       | http://localhost:5170        |
| search     | http://localhost:5171        |
| monolith   | http://localhost:5172        |
| wintersehn | http://localhost:5173        |
| backend    | http://localhost:8000        |
