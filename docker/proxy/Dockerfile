FROM node:24-alpine AS wintersehn-build

WORKDIR /app

COPY --from=wintersehn package*.json ./

RUN npm ci

COPY --from=wintersehn index.html jsconfig.json vite.config.js ./
COPY --from=wintersehn src ./src
COPY --from=wintersehn public ./public
COPY --from=core . /core

RUN npm run build

FROM node:24-alpine AS monolith-build

WORKDIR /app

COPY --from=monolith package*.json ./

RUN npm ci

COPY --from=monolith index.html jsconfig.json vite.config.js ./
COPY --from=monolith src ./src
COPY --from=monolith public ./public
COPY --from=core . /core

RUN npm run build

FROM node:24-alpine AS search-build

WORKDIR /app

COPY --from=search package*.json ./

RUN npm ci

COPY --from=search index.html jsconfig.json vite.config.js ./
COPY --from=search src ./src
COPY --from=search public ./public
COPY --from=core . /core

RUN npm run build

FROM node:24-alpine AS home-build

WORKDIR /app

COPY --from=home package*.json ./

RUN npm ci

COPY --from=home index.html jsconfig.json vite.config.js ./
COPY --from=home src ./src
COPY --from=home public ./public
COPY --from=core . /core

RUN npm run build

FROM node:24-alpine AS atlas-build

WORKDIR /app

COPY --from=atlas package*.json ./

RUN npm ci

COPY --from=atlas index.html jsconfig.json vite.config.js ./
COPY --from=atlas src ./src
COPY --from=atlas public ./public
COPY --from=core . /core

RUN npm run build

FROM caddy:2-alpine

COPY --from=wintersehn-build /app/dist /srv/wintersehn
COPY --from=monolith-build /app/dist /srv/monolith
COPY --from=search-build /app/dist /srv/search
COPY --from=home-build /app/dist /srv/home
COPY --from=atlas-build /app/dist /srv/atlas
COPY Caddyfile /etc/caddy/Caddyfile
COPY Caddyfile.edge /etc/caddy/Caddyfile.edge
