// Build an HTML table from data. Escape every value, or a "name" becomes a script (XSS).
const escapeHtml = s => String(s).replace(/[&<>"']/g, c =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const logins = [
  { user: "ayesha", ip: "10.0.0.15", status: "success" },
  { user: "bilal", ip: "10.0.0.22", status: "failed" },
  { user: "<img src=x onerror=alert(1)>", ip: "203.0.113.9", status: "failed" },
];

function toTable(rows, safe) {
  const cell = v => (safe ? escapeHtml(v) : v);
  const cols = Object.keys(rows[0]);
  const head = "  <thead><tr>" + cols.map(c => `<th scope="col">${c}</th>`).join("") + "</tr></thead>";
  const body = rows.map(r => "    <tr>" + cols.map(c => `<td>${cell(r[c])}</td>`).join("") + "</tr>").join("\n");
  return `<table>\n  <caption>Login attempts</caption>\n${head}\n  <tbody>\n${body}\n  </tbody>\n</table>`;
}

console.log("UNSAFE (string concatenation):");
console.log(toTable(logins, false).split("\n").slice(-3, -2)[0]);
console.log("\nSAFE (escaped):");
console.log(toTable(logins, true));

const failed = logins.filter(r => r.status === "failed").length;
console.log(`\nSummary row: ${failed} of ${logins.length} attempts failed`);

// Choosing media formats: which <source> would a browser pick?
const sources = [{ src: "talk.webm", type: "video/webm" }, { src: "talk.mp4", type: "video/mp4" }];
for (const supported of [["video/mp4"], ["video/webm", "video/mp4"], []]) {
  const pick = sources.find(s => supported.includes(s.type));
  console.log(`browser supports [${supported.join(", ")}] -> ${pick ? pick.src : "fallback text shown"}`);
}
