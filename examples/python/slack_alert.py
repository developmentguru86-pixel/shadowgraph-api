"""Post to Slack when one of your dependencies goes down or recovers.

Usage:
    export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
    python slack_alert.py stripe-api github aws cloudflare

Polls every 5 minutes (the radar's own cadence). Slugs come from
https://shadowalpha.online/_api/search?q=<name> or the /status/<slug> page URL.
Run it under cron/systemd or as a long-running process. Needs: pip install requests
"""
import os
import sys
import time
import requests

API = "https://shadowalpha.online/_api"
WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL")
INTERVAL_S = 300


def state_of(slug: str) -> tuple[str, str]:
    page = requests.get(f"{API}/status/page", params={"slug": slug}, timeout=20).json()
    rows = page.get("rows") or []
    if any(i.get("status") == "open" for i in page.get("incidents") or []) or any(r.get("state") == "down" for r in rows):
        return "down", page.get("name", slug)
    return "up", page.get("name", slug)  # a single failed check ("degraded") is not an outage yet


def notify(text: str) -> None:
    if WEBHOOK:
        requests.post(WEBHOOK, json={"text": text}, timeout=10)
    print(text, flush=True)


def main() -> None:
    slugs = sys.argv[1:]
    if not slugs:
        sys.exit(__doc__)
    last: dict[str, str] = {}
    while True:
        for slug in slugs:
            try:
                state, name = state_of(slug)
            except requests.RequestException as e:
                print(f"{slug}: check failed ({e})", flush=True)
                continue
            if slug in last and state != last[slug]:
                icon = ":red_circle:" if state == "down" else ":large_green_circle:"
                notify(f"{icon} {name} is {state.upper()} - https://shadowalpha.online/status/{slug}")
            last[slug] = state
        time.sleep(INTERVAL_S)


if __name__ == "__main__":
    main()
