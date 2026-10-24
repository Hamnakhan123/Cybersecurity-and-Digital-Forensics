// The same rules the form declares (required, minlength, pattern, type=email, min/max),
// re-checked on the server. Browser validation is for convenience; it is NOT security.
const rules = {
  name:  { required: true, minlength: 3, maxlength: 40 },
  email: { required: true, type: "email" },
  sid:   { required: true, pattern: /^[0-9]{5}$/ },
  pw:    { required: true, minlength: 12 },
  year:  { type: "number", min: 1, max: 4 },
  aup:   { required: true },
};

function validate(data) {
  const errors = [];
  for (const [field, r] of Object.entries(rules)) {
    const v = (data[field] ?? "").toString().trim();
    if (r.required && v === "") { errors.push(`${field}: required`); continue; }
    if (v === "") continue;
    if (r.minlength && v.length < r.minlength) errors.push(`${field}: at least ${r.minlength} characters`);
    if (r.maxlength && v.length > r.maxlength) errors.push(`${field}: at most ${r.maxlength} characters`);
    if (r.pattern && !r.pattern.test(v)) errors.push(`${field}: wrong format`);
    if (r.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) errors.push(`${field}: not an email`);
    if (r.type === "number") {
      const n = Number(v);
      if (!Number.isInteger(n) || n < r.min || n > r.max) errors.push(`${field}: must be ${r.min}-${r.max}`);
    }
  }
  const unknown = Object.keys(data).filter(k => !(k in rules) && !["lab", "os", "why", "csrf"].includes(k));
  if (unknown.length) errors.push(`unexpected fields: ${unknown.join(", ")}`);
  return errors;
}

const submissions = {
  "good student": { name: "Ayesha Khan", email: "ayesha@uni.edu.pk", sid: "20431", pw: "correct-horse-battery", year: "2", aup: "on" },
  "empty form":   {},
  "bypassed UI (sent with curl)": { name: "x", email: "not-an-email", sid: "1' OR '1'='1", pw: "123", year: "9", aup: "on", role: "admin" },
};
for (const [label, data] of Object.entries(submissions)) {
  const e = validate(data);
  console.log(`${label}: ${e.length ? "REJECTED" : "ACCEPTED"}`);
  e.forEach(msg => console.log("   - " + msg));
}
