#!/bin/sh
tor -f /etc/tor/torrc &
pid=$!
failures=0
sleep "${WATCHDOG_GRACE:-120}"
while kill -0 "$pid" 2>/dev/null; do
  if curl -sf --max-time 30 --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/api/ip | grep -q '"IsTor":true'; then
    failures=0
  else
    failures=$((failures + 1))
  fi
  if [ "$failures" -ge "${WATCHDOG_FAILURES:-3}" ]; then
    kill "$pid"
    exit 1
  fi
  sleep "${WATCHDOG_INTERVAL:-300}"
done
exit 1
