// A faithful model of the Web Storage API (localStorage / sessionStorage) so it runs in Node.
class WebStorage {
  #data = new Map();
  #quota;
  constructor(quotaChars = 5_000_000) { this.#quota = quotaChars; }
  get length() { return this.#data.size; }
  key(i) { return [...this.#data.keys()][i] ?? null; }
  getItem(k) { return this.#data.has(String(k)) ? this.#data.get(String(k)) : null; }
  setItem(k, v) {
    const used = [...this.#data].reduce((s, [a, b]) => s + a.length + b.length, 0);
    if (used + String(k).length + String(v).length > this.#quota) throw new Error("QuotaExceededError");
    this.#data.set(String(k), String(v));      // everything is stored as a string
  }
  removeItem(k) { this.#data.delete(String(k)); }
  clear() { this.#data.clear(); }
}

const localStorage = new WebStorage();
localStorage.setItem("theme", "dark");
localStorage.setItem("visits", 3);
localStorage.setItem("prefs", { lang: "en" });       // mistake: object without JSON
console.log("theme  :", localStorage.getItem("theme"));
console.log("visits :", localStorage.getItem("visits"), "->", typeof localStorage.getItem("visits"));
console.log("prefs  :", localStorage.getItem("prefs"), "<- object was turned into a useless string");

localStorage.setItem("prefs", JSON.stringify({ lang: "en", fontSize: 14 }));
console.log("prefs  :", JSON.parse(localStorage.getItem("prefs")).fontSize, "<- JSON round trip works");
console.log("missing:", localStorage.getItem("nope"));

console.log("\nAll keys:");
for (let i = 0; i < localStorage.length; i++) console.log("  ", localStorage.key(i), "=", localStorage.getItem(localStorage.key(i)));

const tiny = new WebStorage(20);
try { tiny.setItem("log", "x".repeat(50)); } catch (e) { console.log("\nquota  :", e.message); }

// Security check: what an injected script could steal from storage
localStorage.setItem("authToken", "eyJhbGciOi...secret");
const exposed = [];
for (let i = 0; i < localStorage.length; i++) {
  const k = localStorage.key(i);
  if (/token|password|secret|session/i.test(k)) exposed.push(k);
}
console.log("\nKeys any XSS payload could read:", exposed.join(", ") || "none");
console.log("Advice: keep session tokens in HttpOnly cookies, not in Web Storage.");
localStorage.removeItem("authToken");
console.log("After removeItem, keys left:", localStorage.length);
