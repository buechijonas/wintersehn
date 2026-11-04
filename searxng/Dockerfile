FROM searxng/searxng:latest

COPY settings.yml settings.dev.yml configure.py /usr/local/searxng/config/
COPY image_proxy_rewrite.py /usr/local/searxng/searx/plugins/

ENV SEARXNG_BASE_SETTINGS=/usr/local/searxng/config/settings.yml
ENV SEARXNG_SETTINGS_PATH=/tmp/settings.yml

ENTRYPOINT ["/bin/sh", "-c", "/usr/local/searxng/.venv/bin/python /usr/local/searxng/config/configure.py && exec /usr/local/searxng/entrypoint.sh"]
