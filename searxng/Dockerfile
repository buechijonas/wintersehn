FROM searxng/searxng:latest

COPY settings.yml settings.dev.yml /usr/local/searxng/config/
COPY image_proxy_rewrite.py /usr/local/searxng/searx/plugins/

ENV SEARXNG_SETTINGS_PATH=/usr/local/searxng/config/settings.yml
