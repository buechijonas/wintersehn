# home

Frontend for home.wintersehn.ch. Lists all apps as cards and links to them. Only signed-in admins (`can_view_admin`) can open it, everyone else is sent to the login or to wintersehn.ch. Shares layout, auth and settings with the other frontends via `../core` (`@core/…`).

```sh
npm install
npm run dev   # http://localhost:5170
```
