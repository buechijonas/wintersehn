# search

Frontend for search.wintersehn.ch. The browser queries SearXNG (`docker/searxng`) through the proxy at `/searxng/search`, which only accepts requests from this app. In production SearXNG reaches the search engines through five Tor instances (`docker/tor`); a query guard plugin blocks harmful queries before they leave the server.

The backend (`backend/search`) stores the settings in the account if wanted, enforces child protection for minors and rates result domains (Mozilla Observatory headers and lookalike detection). Without an account the settings stay in the browser. Brave and Qwant are disabled on the server because they block Tor and datacenter addresses; Brave becomes available again with `SEARXNG_BRAVE_API_KEY`.

```sh
npm install
npm run dev   # http://localhost:5171
```

## Networks

All queries leave the server through Tor, never directly. "Tor" spreads them over five Tor instances; "Tor streng" ("strict") additionally gives every request its own circuit so a provider cannot link consecutive searches. Each provider is queried separately, results appear as soon as the first provider answers, and a provider that fails on one network is retried once on the other.

Providers that block Tor (Google, Mojeek, Qwant, Vimeo) are not offered.
