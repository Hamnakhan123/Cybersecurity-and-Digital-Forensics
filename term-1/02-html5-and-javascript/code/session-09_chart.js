// The maths behind the canvas bar chart: every fillRect call the page makes, plus a text preview.
const data = [{ h: "08", n: 4 }, { h: "09", n: 12 }, { h: "10", n: 30 }, { h: "11", n: 7 }, { h: "12", n: 2 }];
const max = Math.max(...data.map(d => d.n)), base = 190, barW = 50, gap = 30;

console.log("Canvas origin (0,0) is the TOP-LEFT corner; y grows downward.\n");
console.log("hour  count  fillRect(x, y, w, h)        colour");
for (const [i, d] of data.entries()) {
  const x = 40 + i * (barW + gap), h = Math.round((d.n / max) * 160);
  const colour = d.n >= 20 ? "#c0392b (red)" : "#2e86de (blue)";
  console.log(`${d.h}:00 ${String(d.n).padStart(5)}  fillRect(${x}, ${base - h}, ${barW}, ${h})`.padEnd(42) + colour);
}

console.log("\nText preview (each # = 2 logins):");
for (const d of data) console.log(`${d.h}:00 | ${"#".repeat(Math.round(d.n / 2)).padEnd(15)} ${d.n}`);
