# search

Frontend for search.wintersehn.ch. The browser queries SearXNG (`docker/searxng`) through the proxy at `/searxng/search`, which only accepts requests from this app. In production SearXNG reaches the search engines through three Tor instances (`docker/tor`); a query guard plugin blocks harmful queries before they leave the server.

The backend (`backend/search`) stores the settings in the account if wanted, enforces child protection for minors and rates result domains (Mozilla Observatory headers and lookalike detection). Without an account the settings stay in the browser. Brave and Qwant are disabled on the server because they block Tor and datacenter addresses; Brave becomes available again with `SEARXNG_BRAVE_API_KEY`.

```sh
npm install
npm run dev   # http://localhost:5171
```

## Networks

SearXNG always offers Tor. Optional networks become selectable in the privacy settings when configured in the server's `.env`:

- `SEARXNG_CUSTOM_PROXY=socks5h://user:pass@host:port` (or `http://…`) for a proxy you run yourself.
- `SEARXNG_VPN_PROXY=http://vpn:8888` together with `COMPOSE_PROFILES=vpn` and the WireGuard settings for gluetun.
