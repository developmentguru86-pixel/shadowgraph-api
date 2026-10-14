#!/usr/bin/env bash
# Usage: ./is-it-down.sh stripe        -> "Stripe API: up (checked 2026-10-14T17:06:40Z)"
# Needs curl and jq. No API key.
set -euo pipefail
API="https://shadowalpha.online/_api"
q="${1:?usage: $0 <service name or domain>}"

slug=$(curl -sf "$API/search?q=$(jq -rn --arg q "$q" '$q|@uri')&quick=1" | jq -r '.services[0].slug // empty')
if [ -z "$slug" ]; then echo "\"$q\" is not monitored yet."; exit 2; fi

curl -sf "$API/status/page?slug=$slug" | jq -r '
  (.incidents | map(select(.status == "open")) | first) as $inc
  | ([.rows[] | select(.state == "down")] | length) as $down
  | ([.rows[] | select(.state == "degraded")] | length) as $err
  | "\(.name): " + (
      if $inc then "DOWN - provider incident on \($inc.provider) since \($inc.startedAt)"
      elif $down > 0 then "NOT ANSWERING - \($down) of \(.rows | length) endpoints down"
      elif $err > 0 then "one failed check (\($err) of \(.rows | length)), re-checked every 5 min"
      else "up" end
    ) + " (checked \(.checkedAt))"'
