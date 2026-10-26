"""Session 11 - Check passwords against an acceptable-use / password policy
and estimate their strength. Modern guidance (e.g. NIST SP 800-63B) favours
length and a block-list over forced complexity and frequent changes.
Run:  python session-11_password_policy.py
"""
import math
import string

BLOCKLIST = {"password", "123456", "qwerty", "admin", "welcome", "cisco", "letmein"}
POLICY = {"min_length": 12, "max_length": 64}


def entropy_bits(pw):
    pool = 0
    if any(c in string.ascii_lowercase for c in pw): pool += 26
    if any(c in string.ascii_uppercase for c in pw): pool += 26
    if any(c in string.digits for c in pw): pool += 10
    if any(c in string.punctuation or c == " " for c in pw): pool += 33
    return len(pw) * math.log2(pool) if pool else 0


def check(pw, username):
    problems = []
    if len(pw) < POLICY["min_length"]: problems.append(f"shorter than {POLICY['min_length']}")
    if len(pw) > POLICY["max_length"]: problems.append("too long")
    low = pw.lower()
    if any(b in low for b in BLOCKLIST): problems.append("contains a block-listed word")
    if username.lower() in low: problems.append("contains the username")
    if len(set(pw)) <= 3: problems.append("too repetitive")
    return problems


if __name__ == "__main__":
    tests = [("hamna", "Cisco123"), ("hamna", "P@ssw0rd2026!"), ("ali", "ali-network-2026"),
             ("sara", "aaaaaaaaaaaaaaa"), ("lab", "river tulip lantern seventy"), ("lab", "x7#Qp!2vR9$m")]
    for user, pw in tests:
        p = check(pw, user)
        verdict = "ACCEPT" if not p else "REJECT: " + "; ".join(p)
        print(f"{pw!r:<32} ~{entropy_bits(pw):>5.0f} bits  {verdict}")
