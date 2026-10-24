// Compute CSS specificity (ids, classes/attributes/pseudo-classes, elements) and pick the winner.
function specificity(sel) {
  const el = (sel.match(/::[a-z-]+/g) || []).length;    // pseudo-elements count as elements
  const s = sel.replace(/::[a-z-]+/g, "");
  const ids = (s.match(/#[\w-]+/g) || []).length;
  const cls = (s.match(/\.[\w-]+|\[[^\]]+\]|:[\w-]+(\([^)]*\))?/g) || []).length;
  const elements = (s.replace(/#[\w-]+|\.[\w-]+|\[[^\]]+\]|:[\w-]+(\([^)]*\))?/g, " ")
                      .match(/(^|[\s>+~])([a-z][\w-]*)/gi) || []).length;
  return [ids, cls, elements + el];
}

const selectors = ["p", "li:nth-child(odd)", ".card", ".card.critical", "#summary",
                   "div.card.critical", ".critical .badge", "a:hover", ".badge::before", "body main section p"];
console.log("Selector".padEnd(22), "(id, class, element)");
for (const s of selectors) console.log(s.padEnd(22), `(${specificity(s).join(", ")})`);

// Which rule wins for <div class="card critical"> border-color?
const rules = [
  { sel: ".card", value: "#ccc", order: 1 },
  { sel: ".card.critical", value: "var(--danger)", order: 2 },
  { sel: "div", value: "black", order: 3 },
];
const cmp = (a, b) => {
  const x = specificity(a.sel), y = specificity(b.sel);
  for (let i = 0; i < 3; i++) if (x[i] !== y[i]) return y[i] - x[i];
  return b.order - a.order;  // same specificity: later rule wins
};
const winner = [...rules].sort(cmp)[0];
console.log(`\nborder-color for <div class="card critical"> -> ${winner.value} (from "${winner.sel}")`);

// Box model: total width with content-box vs border-box
const width = 300, padding = 16, border = 2;
console.log(`content-box total width: ${width + 2 * padding + 2 * border}px`);
console.log(`border-box  total width: ${width}px (content shrinks to ${width - 2 * padding - 2 * border}px)`);
