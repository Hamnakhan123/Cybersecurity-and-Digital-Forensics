// A tiny web server and a client in one script: watch one HTTP request/response.
const http = require("http");

const server = http.createServer((req, res) => {
  console.log(`SERVER got  : ${req.method} ${req.url} HTTP/${req.httpVersion}`);
  console.log(`SERVER saw  : Host=${req.headers.host.replace(/:\d+$/, ":<port>")}, User-Agent=${req.headers["user-agent"]}`);
  if (req.url === "/") {
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8", "X-Content-Type-Options": "nosniff" });
    res.end("<!DOCTYPE html><title>Hi</title><h1>Hello from the lab server</h1>");
  } else {
    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("Not found");
  }
});

server.listen(0, "127.0.0.1", async () => {
  const base = `http://127.0.0.1:${server.address().port}`;
  for (const path of ["/", "/admin"]) {
    const r = await fetch(base + path, { headers: { "User-Agent": "CyberLabClient/1.0" } });
    console.log(`CLIENT got  : ${r.status} ${r.statusText}`);
    console.log(`CLIENT type : ${r.headers.get("content-type")}`);
    console.log(`CLIENT body : ${await r.text()}\n`);
  }
  server.close();
});
