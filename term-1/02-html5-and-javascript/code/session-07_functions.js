// JavaScript II: functions, closures, objects, arrays and JSON.

// 1. Three ways to define a function
function add(a, b) { return a + b; }                 // declaration (hoisted)
const multiply = function (a, b) { return a * b; };  // expression
const square = x => x * x;                           // arrow
console.log("add, multiply, square:", add(2, 3), multiply(4, 5), square(9));

// 2. Default and rest parameters
function scan(host, ...ports) {
  const list = ports.length ? ports : [80, 443];
  return `${host}: ${list.join(", ")}`;
}
console.log("scan:", scan("10.0.0.5"), "|", scan("10.0.0.6", 22, 3389));

// 3. Closure: a rate limiter that remembers its own counter
function makeLimiter(max) {
  let used = 0;                       // private: only the inner function sees it
  return () => (++used <= max ? `allowed (${used}/${max})` : "blocked");
}
const loginLimiter = makeLimiter(3);
for (let i = 1; i <= 5; i++) console.log(`  request ${i}: ${loginLimiter()}`);

// 4. Objects, methods and this
const device = {
  hostname: "lab-ws-07",
  ip: "192.168.56.107",
  openPorts: [22, 80],
  describe() { return `${this.hostname} (${this.ip}) ports ${this.openPorts.join("/")}`; },
};
console.log("\nobject:", device.describe());
const { hostname, ip } = device;                     // destructuring
console.log("destructured:", hostname, ip);
const hardened = { ...device, openPorts: [22] };     // spread copy
console.log("copy:", hardened.describe(), "| original still:", device.openPorts);

// 5. Array higher-order functions
const alerts = [
  { id: 1, sev: 9, src: "10.0.0.9" }, { id: 2, sev: 3, src: "10.0.0.4" },
  { id: 3, sev: 7, src: "10.0.0.9" }, { id: 4, sev: 5, src: "10.0.0.2" },
];
console.log("\nhigh severity ids :", alerts.filter(a => a.sev >= 7).map(a => a.id));
console.log("average severity  :", alerts.reduce((s, a) => s + a.sev, 0) / alerts.length);
console.log("first from .9     :", alerts.find(a => a.src === "10.0.0.9").id);
console.log("sorted by severity:", [...alerts].sort((a, b) => b.sev - a.sev).map(a => a.sev));

// 6. JSON round trip and safe parsing
const json = JSON.stringify(device, ["hostname", "ip", "openPorts"]);
console.log("\nJSON.stringify ->", json);
console.log("JSON.parse     ->", JSON.parse(json).openPorts[1]);
function safeParse(text) {
  try { return JSON.parse(text); }
  catch (e) { return { error: e.name }; }
}
console.log("bad JSON       ->", safeParse("{ip: '1.2.3.4'}"));
