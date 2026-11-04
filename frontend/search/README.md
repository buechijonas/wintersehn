# search

Frontend for search.wintersehn.ch. The browser queries SearXNG (`docker/searxng`) directly through the proxy at `/searxng/search`; no backend involved. In production SearXNG reaches all search engines only through Tor (`docker/tor`). Search settings live in the browser (`localStorage`). Shares auth and settings components with `wintersehn/` via `../core` (`@core/…`).

```sh
npm install
npm run dev   # http://localhost:5171
```

## Networks

SearXNG always offers Tor. Two optional networks become selectable in the privacy settings when configured in the server's `.env`:

- `SEARXNG_VPN_PROXY=http://vpn:8888` together with `COMPOSE_PROFILES=vpn` and the WireGuard settings `VPN_SERVICE_PROVIDER`, `VPN_WIREGUARD_PRIVATE_KEY`, `VPN_WIREGUARD_ADDRESSES` and optionally `VPN_SERVER_COUNTRIES` (runs gluetun).
- `SEARXNG_CUSTOM_PROXY=socks5h://user:pass@host:port` (or `http://…`) for a proxy you run yourself.
