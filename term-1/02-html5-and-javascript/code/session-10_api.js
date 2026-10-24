// Calling a JSON REST API with fetch: a tiny local API server, CORS headers, errors and timeouts.
const http = require("http");

const advisories = [
  { id: "ADV-1", title: "Update the lab router firmware", severity: "high" },
  { id: "ADV-2", title: "Rotate shared Wi-Fi password", severity: "medium" },
];

const server = http.createServer((req, res) => {
  const send = (code, body, extra = {}) => {
    res.writeHead(code, { "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "https://lab.example.edu", ...extra });   // CORS: who may read this
    res.end(JSON.stringify(body));
  };
  const url = new URL(req.url, "http://localhost");
  if (url.pathname === "/api/advisories") {
    const sev = url.searchParams.get("severity");
    return send(200, sev ? advisories.filter(a => a.severity === sev) : advisories);
  }
  if (url.pathname === "/api/slow") return setTimeout(() => send(200, { ok: true }), 500);
  if (url.pathname === "/api/admin") return send(401, { error: "API key required" });
  send(404, { error: "no such endpoint" });
});

async function getJSON(url, ms = 200) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), ms);
  try {
    const res = await fetch(url, { signal: ctrl.signal, headers: { Accept: "application/json" } });
    const body = await res.json();
    if (!res.ok) return `HTTP ${res.status}: ${body.error}`;
    return { cors: res.headers.get("access-control-allow-origin"), body };
  } catch (e) {
    return e.name === "AbortError" ? `timed out after ${ms} ms` : `network error: ${e.message}`;
  } finally { clearTimeout(timer); }
}

server.listen(0, "127.0.0.1", async () => {
  const base = `http://127.0.0.1:${server.address().port}`;
  const all = await getJSON(base + "/api/advisories");
  console.log("GET /api/advisories");
  console.log("  CORS allow-origin:", all.cors);
  all.body.forEach(a => console.log(`  ${a.id}  ${a.severity.padEnd(6)}  ${a.title}`));
  const high = await getJSON(base + "/api/advisories?severity=high");
  console.log("GET ?severity=high ->", high.body.map(a => a.id).join(", "));
  console.log("GET /api/admin     ->", await getJSON(base + "/api/admin"));
  console.log("GET /api/missing   ->", await getJSON(base + "/api/missing"));
  console.log("GET /api/slow      ->", await getJSON(base + "/api/slow"));
  server.close();
  setTimeout(() => process.exit(0), 600);
});
