// Inspect an HTML file without a browser: doctype, language, charset and outline.
const fs = require("fs");
const html = fs.readFileSync("session-01_page.html", "utf8");

console.log("Doctype present :", /^<!DOCTYPE html>/i.test(html.trim()));
console.log("lang attribute  :", (html.match(/<html[^>]*lang="([^"]+)"/i) || [])[1]);
console.log("charset         :", (html.match(/<meta charset="([^"]+)"/i) || [])[1]);
console.log("title           :", (html.match(/<title>(.*?)<\/title>/i) || [])[1]);

// Count every opening tag
const counts = {};
for (const m of html.matchAll(/<([a-z][a-z0-9]*)\b/gi)) {
  const tag = m[1].toLowerCase();
  counts[tag] = (counts[tag] || 0) + 1;
}
console.log("\nTag counts:");
for (const [tag, n] of Object.entries(counts).sort()) console.log(`  ${tag.padEnd(8)} ${n}`);

// Heading outline
console.log("\nDocument outline:");
for (const m of html.matchAll(/<h([1-6])>(.*?)<\/h\1>/gi)) {
  console.log("  " + "  ".repeat(Number(m[1]) - 1) + `h${m[1]}: ${m[2]}`);
}
