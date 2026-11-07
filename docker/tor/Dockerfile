FROM alpine:3.22

RUN apk add --no-cache tor curl

RUN install -d -o tor -g tor -m 700 /var/lib/tor /var/lib/tor/onion

COPY torrc onion.torrc /etc/tor/
COPY --chmod=755 watchdog.sh /usr/local/bin/watchdog

USER tor

CMD ["watchdog"]
