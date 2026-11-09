# monolith

Frontend for monolith.wintersehn.ch: dossiers about people with relationships, events, chat references, character, stances, addictions, a trust ledger and trust circles, a network graph, and sharing by account or password-protected link. Sensitive fields are encrypted in `backend/monolith`; tags stay searchable through a blind index. Markdown is rendered and cleaned in the backend. Shares layout, components, auth and legal pages with `wintersehn/` via `../core` (`@core/…`).

```sh
npm install
npm run dev   # http://localhost:5172
```
