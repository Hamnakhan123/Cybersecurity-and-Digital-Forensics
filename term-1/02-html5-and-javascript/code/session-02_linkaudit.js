// Audit every hyperlink in a page: type, broken in-page anchors, unsafe target=_blank, plain http.
const fs = require("fs");
const html = fs.readFileSync("session-02_links.html", "utf8");

const ids = new Set([...html.matchAll(/\sid="([^"]+)"/g)].map(m => m[1]));
const links = [...html.matchAll(/<a\s+([^>]*)>(.*?)<\/a>/gi)].map(m => {
  const attr = name => (m[1].match(new RegExp(`${name}="([^"]*)"`)) || [])[1];
  return { text: m[2], href: attr("href"), target: attr("target"), rel: attr("rel") || "" };
});

function kind(href) {
  if (href.startsWith("#")) return "in-page";
  if (href.startsWith("mailto:")) return "email";
  if (href.startsWith("tel:")) return "phone";
  if (/^https?:\/\//.test(href)) return "absolute";
  return "relative";
}

let warnings = 0;
console.log("Text".padEnd(18), "Type".padEnd(9), "Href");
for (const l of links) {
  console.log(l.text.padEnd(18), kind(l.href).padEnd(9), l.href);
  if (kind(l.href) === "in-page" && !ids.has(l.href.slice(1))) {
    console.log("   ! broken anchor: no element has id=" + l.href.slice(1)); warnings++;
  }
  if (l.target === "_blank" && !l.rel.includes("noopener")) {
    console.log("   ! target=_blank without rel=noopener (tab-nabbing risk)"); warnings++;
  }
  if (l.href.startsWith("http://")) {
    console.log("   ! plain http: traffic can be read or changed in transit"); warnings++;
  }
}
console.log(`\n${links.length} links checked, ${warnings} warnings`);
