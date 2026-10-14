"""Is it down? Live answer for any service ShadowGraph monitors.

Usage:  python is_it_down.py github
Needs:  pip install requests   (no API key)
"""
import sys
import requests

API = "https://shadowalpha.online/_api"


def find_slug(query: str) -> str | None:
    r = requests.get(f"{API}/search", params={"q": query, "quick": "1"}, timeout=20)
    r.raise_for_status()
    services = r.json().get("services") or []
    return services[0]["slug"] if services else None


def verdict(page: dict) -> str:
    rows = page.get("rows") or []
    open_incident = next((i for i in page.get("incidents") or [] if i.get("status") == "open"), None)
    down = [r for r in rows if r.get("state") == "down"]
    degraded = [r for r in rows if r.get("state") == "degraded"]
    if open_incident:
        return f"DOWN - provider incident on {open_incident['provider']} since {open_incident['startedAt']}"
    if down:
        since = min((r["since"] for r in down if r.get("since")), default=None)
        return f"NOT ANSWERING - {len(down)} of {len(rows)} endpoints down" + (f" since {since}" if since else "")
    if degraded:
        return f"one failed check ({len(degraded)} of {len(rows)} endpoints), re-checked every 5 minutes"
    return "up"


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    slug = find_slug(" ".join(sys.argv[1:]))
    if not slug:
        print("Not monitored yet. Try the brand name or the domain.")
        return 2
    page = requests.get(f"{API}/status/page", params={"slug": slug}, timeout=20).json()
    print(f"{page['name']}: {verdict(page)}")
    print(f"  checked {page.get('checkedAt')}, outages in the last 30 days: {page.get('issues30d', 0)}")
    for layer in page.get("infrastructure") or []:
        print(f"  {layer['layer']:<8} {layer['name']}")
    print(f"  details: https://shadowalpha.online/status/{slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
