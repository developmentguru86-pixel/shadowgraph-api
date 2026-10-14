// Is it down? Node 18+ (built-in fetch), no dependencies, no API key.
// Usage: node is-it-down.mjs netflix
const API = "https://shadowalpha.online/_api";
const query = process.argv.slice(2).join(" ");
if (!query) { console.log("usage: node is-it-down.mjs <service name or domain>"); process.exit(1); }

const search = await (await fetch(`${API}/search?q=${encodeURIComponent(query)}&quick=1`)).json();
const slug = search.services?.[0]?.slug;
if (!slug) { console.log(`"${query}" is not monitored yet.`); process.exit(2); }

const page = await (await fetch(`${API}/status/page?slug=${encodeURIComponent(slug)}`)).json();
const rows = page.rows ?? [];
const incident = (page.incidents ?? []).find((i) => i.status === "open");
const down = rows.filter((r) => r.state === "down").length;
const degraded = rows.filter((r) => r.state === "degraded").length;

const verdict = incident ? `DOWN - provider incident on ${incident.provider} since ${incident.startedAt}`
  : down ? `NOT ANSWERING - ${down} of ${rows.length} endpoints down`
  : degraded ? `one failed check (${degraded} of ${rows.length}), re-checked every 5 minutes`
  : "up";

console.log(`${page.name}: ${verdict} (checked ${page.checkedAt})`);
for (const layer of page.infrastructure ?? []) console.log(`  ${layer.layer.padEnd(8)} ${layer.name}`);
console.log(`  details: https://shadowalpha.online/status/${slug}`);
