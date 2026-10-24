// JavaScript I: decisions and loops on a small login log.
const log = [
  "08:01 ayesha OK", "08:03 bilal FAIL", "08:03 bilal FAIL", "08:04 bilal FAIL",
  "08:05 bilal FAIL", "08:09 sara OK", "08:10 root FAIL", "08:11 bilal FAIL",
];

// for...of + if/else: count failures per user
const fails = {};
for (const line of log) {
  const [time, user, result] = line.split(" ");
  if (result === "FAIL") fails[user] = (fails[user] || 0) + 1;
}
console.log("Failures per user:", fails);

// switch: classify severity
function severity(count) {
  switch (true) {
    case count >= 5: return "HIGH - lock the account";
    case count >= 3: return "MEDIUM - require CAPTCHA";
    default:         return "LOW";
  }
}
for (const [user, n] of Object.entries(fails)) console.log(`  ${user.padEnd(6)} ${n} -> ${severity(n)}`);

// while + break: stop at the first moment any user reaches 3 failures
let i = 0;
const running = {};
while (i < log.length) {
  const [time, user, result] = log[i].split(" ");
  if (result === "FAIL") {
    running[user] = (running[user] || 0) + 1;
    if (running[user] === 3) {
      console.log(`\nAlert at ${time}: ${user} reached 3 failures (line ${i + 1})`);
      break;
    }
  }
  i++;
}

// classic for + continue: print only successful logins
console.log("\nSuccessful logins:");
for (let j = 0; j < log.length; j++) {
  if (!log[j].endsWith("OK")) continue;
  console.log("  " + log[j]);
}

// do...while: password strength loop over candidate passwords
const candidates = ["12345", "password1", "Lab#2026-secure"];
let k = 0, pw;
do {
  pw = candidates[k++];
  const strong = pw.length >= 12 && /[A-Z]/.test(pw) && /[0-9]/.test(pw) && /[^A-Za-z0-9]/.test(pw);
  console.log(`\nTry "${pw}": ${strong ? "strong, accepted" : "weak, try again"}`);
  if (strong) break;
} while (k < candidates.length);
