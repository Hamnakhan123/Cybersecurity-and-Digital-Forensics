// JavaScript I: variables, types, operators and type coercion.
const course = "Cyber Lab";      // cannot be reassigned
let attempts = 0;                // can change
attempts += 1;

const values = [42, 3.14, "42", true, null, undefined, { port: 22 }, [1, 2], () => 1, 10n];
console.log("typeof each value:");
for (const v of values) console.log(`  ${String(typeof v === "bigint" ? v + "n" : JSON.stringify(v) ?? v).padEnd(12)} -> ${typeof v}`);

console.log("\nArithmetic and strings:");
console.log("  7 / 2      =", 7 / 2);
console.log("  7 % 2      =", 7 % 2);
console.log("  2 ** 10    =", 2 ** 10);
console.log('  "5" + 3    =', "5" + 3, " (string concatenation)");
console.log('  "5" - 3    =', "5" - 3, "   (numeric conversion)");
console.log("  0.1 + 0.2  =", 0.1 + 0.2);
console.log('  Number("x")=', Number("x"));

console.log("\nLoose == vs strict ===:");
const show = v => (typeof v === "string" ? `"${v}"` : String(v));
for (const [a, b] of [[0, "0"], [0, ""], [null, undefined], ["1", 1], [NaN, NaN]]) {
  console.log(`  ${(show(a) + " == " + show(b)).padEnd(20)} -> ${String(a == b).padEnd(5)}  === -> ${a === b}`);
}

console.log("\nTruthy / falsy:");
for (const v of [0, "", "0", [], null, "false", NaN]) console.log(`  ${(Array.isArray(v) ? "[]" : show(v)).padEnd(8)} is ${v ? "truthy" : "falsy"}`);

console.log("\nLogical operators:");
const username = "";
console.log("  username || 'guest'  ->", username || "guest");
console.log("  username ?? 'guest'  ->", JSON.stringify(username ?? "guest"), "(?? only replaces null/undefined)");
console.log(`  Template literal     -> Welcome to ${course}, attempt ${attempts}`);
