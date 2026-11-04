# search

Frontend for search.wintersehn.ch. The browser queries SearXNG (`../searxng`) directly through the proxy at `/searxng/search`; no backend involved. In production SearXNG reaches all search engines only through Tor (`../tor`). Search settings live in the browser (`localStorage`). Shares auth and settings components with `wintersehn/` via `../core` (`@core/…`).

```sh
npm install
npm run dev   # http://localhost:5171
```
