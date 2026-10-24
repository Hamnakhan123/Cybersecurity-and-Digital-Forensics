// ECMAScript 2022 features, each shown with real output.

// 1. Class fields, private #fields and #methods, static fields and a static block
class Session {
  static count = 0;                 // static public field
  static #secretPrefix;             // static private field
  static { Session.#secretPrefix = "sid_"; }   // static initialisation block

  user;                             // public instance field
  #token;                           // private instance field
  #createdAt = 1700000000;

  constructor(user) {
    this.user = user;
    this.#token = Session.#secretPrefix + Math.abs(this.#hash(user)).toString(16);
    Session.count++;
  }
  #hash(s) { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) | 0; return h; }
  get masked() { return this.#token.slice(0, 6) + "****"; }
  static isSession(obj) { return #token in obj; }    // ergonomic brand check
}

const s1 = new Session("ayesha"), s2 = new Session("bilal");
console.log("users        :", s1.user, s2.user, "| Session.count =", Session.count);
console.log("masked token :", s1.masked);
console.log("JSON view    :", JSON.stringify(s1), "(private fields are not exposed)");
console.log("#token in obj:", Session.isSession(s1), Session.isSession({ user: "fake" }));
try { eval("s1.#token"); } catch (e) { console.log("outside access:", e.name); }

// 2. Array.prototype.at() / String.prototype.at()
const logins = ["08:01", "08:05", "08:30", "09:12"];
console.log("\nat(0), at(-1)     :", logins.at(0), logins.at(-1));
console.log('"ROOT".at(-2)     :', "ROOT".at(-2));

// 3. Object.hasOwn() instead of hasOwnProperty
const cfg = JSON.parse('{"debug": false, "__proto__": {"isAdmin": true}}');
console.log("\ncfg.isAdmin       :", cfg.isAdmin, "(JSON.parse made __proto__ a plain own key)");
console.log("hasOwn(cfg,'__proto__'):", Object.hasOwn(cfg, "__proto__"));
console.log("hasOwn(cfg,'debug'):", Object.hasOwn(cfg, "debug"));
const bare = Object.create(null); bare.k = 1;
console.log("hasOwn on null-proto object:", Object.hasOwn(bare, "k"));

// 4. Error cause: wrap a low-level error without losing it
function loadPolicy(text) {
  try { return JSON.parse(text); }
  catch (err) { throw new Error("Could not load firewall policy", { cause: err }); }
}
try { loadPolicy("{bad"); }
catch (e) { console.log("\nerror :", e.message); console.log("cause :", e.cause.name); }

// 5. RegExp match indices with the /d flag
const line = "Failed password for root from 203.0.113.9 port 22";
const m = /from (?<ip>\d+\.\d+\.\d+\.\d+)/d.exec(line);
console.log("\nip found          :", m.groups.ip, "at indices", m.indices.groups.ip);

// 6. Top-level await is for ES modules (.mjs or type="module"); in a script use an async function
(async () => {
  const delay = (ms, v) => new Promise(r => setTimeout(() => r(v), ms));
  const result = await delay(10, "scan finished");
  console.log("\nawait            :", result);
})();
