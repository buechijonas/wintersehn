FROM alpine:3.22

RUN apk add --no-cache tor

RUN install -d -o tor -g tor -m 700 /var/lib/tor /var/lib/tor/onion

COPY torrc onion.torrc /etc/tor/

USER tor

CMD ["tor", "-f", "/etc/tor/torrc"]
