// Modern syntax used every day since ES2015-ES2021, plus later additions you will meet.
const report = { host: "web01", scan: { ports: [22, 443], os: null } };

// Optional chaining ?. and nullish coalescing ??
console.log("os            :", report.scan?.os ?? "unknown");
console.log("missing path  :", report.vuln?.cve?.id ?? "none recorded");

// Logical assignment (ES2021)
report.scan.os ??= "Linux";
report.tags ||= ["dmz"];
console.log("after ??= ||= :", report.scan.os, report.tags);

// Numeric separators (ES2021) and BigInt (ES2020)
const bytes = 1_073_741_824;
console.log("1 GiB         :", bytes, "bytes");
console.log("2n ** 64n     :", (2n ** 64n).toString(), "(IPv6 needs 128-bit numbers)");

// Promise.allSettled vs Promise.all
const check = (host, ok) => new Promise((res, rej) => setTimeout(() => ok ? res(`${host} up`) : rej(new Error(`${host} down`)), 5));
(async () => {
  const results = await Promise.allSettled([check("10.0.0.1", true), check("10.0.0.2", false), check("10.0.0.3", true)]);
  console.log("\nallSettled    :");
  results.forEach(r => console.log("  ", r.status.padEnd(9), r.value ?? r.reason.message));
  try { await Promise.all([check("a", true), check("b", false)]); }
  catch (e) { console.log("Promise.all   : rejected on first failure ->", e.message); }

  // Later additions you will see in current browsers and Node 22
  const sev = [3, 9, 5, 7];
  console.log("\nfindLast >5   :", sev.findLast(n => n > 5), "(ES2023)");
  console.log("toSorted      :", sev.toSorted((a, b) => a - b), "original:", sev, "(ES2023)");
  const grouped = Object.groupBy(sev, n => (n >= 7 ? "high" : "low"));
  console.log("Object.groupBy:", JSON.stringify(grouped), "(ES2024)");
})();
