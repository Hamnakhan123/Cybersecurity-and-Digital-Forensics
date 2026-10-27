"""Session 4 - Adaptive (risk-based) access control written as policy-as-code.

Traditional access control asks one question: "Is the password right?" Adaptive access,
used in Zero Trust and modern IAM products, asks: "Given everything we know right now,
how risky is this request, and how sensitive is what is being requested?"

The script combines:
  - signals: device compliance, network, location, time, and a behaviour (UBA) risk score
  - resource sensitivity: public, internal, confidential, restricted
  - rules from a written policy (each rule has an ID so auditors can trace decisions)
and returns ALLOW, ALLOW WITH MFA, ALLOW READ-ONLY or DENY, with an audit line per request.
All people and systems are fictional.
Run:  python session-04_adaptive_access.py
"""

SENSITIVITY = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}
RESOURCES = {"Course portal": "internal", "Grades database": "restricted",
             "Library catalogue": "public", "HR payroll": "confidential"}


def risk(sig):
    """Return (risk 0-100, reasons). Weights come from the written access policy."""
    r, why = 0, []
    if not sig["device_compliant"]:
        r += 30; why.append("device not compliant (no disk encryption or old patches)")
    if sig["network"] == "public_wifi":
        r += 15; why.append("public Wi-Fi")
    if sig["country"] != "PK":
        r += 20; why.append(f"outside usual country ({sig['country']})")
    if not 7 <= sig["hour"] <= 22:
        r += 10; why.append(f"outside working hours ({sig['hour']:02d}:00 PKT)")
    r += sig["uba_score"] // 2
    if sig["uba_score"] >= 40:
        why.append(f"behaviour analytics score {sig['uba_score']}")
    return min(r, 100), why


def decide(sig, resource):
    level = SENSITIVITY[RESOURCES[resource]]
    r, why = risk(sig)
    # Rules are checked in order; the first match wins (like a firewall).
    if sig["role"] not in sig["allowed_roles"]:
        return "DENY", "AC-1 role not authorised for resource", r, why
    if r >= 70:
        return "DENY", "AC-2 risk too high for any access", r, why
    if level == 3 and (r >= 30 or not sig["device_compliant"]):
        return "DENY", "AC-3 restricted data needs compliant device and low risk", r, why
    if level >= 2 and r >= 40:
        return "ALLOW READ-ONLY", "AC-4 medium risk: no edits or downloads", r, why
    if level >= 1 and (r >= 20 or level >= 2):
        return "ALLOW WITH MFA", "AC-5 step-up authentication", r, why
    return "ALLOW", "AC-6 public data or low risk", r, why


BASE = {"device_compliant": True, "network": "campus", "country": "PK", "hour": 10, "uba_score": 5}
REQUESTS = [
    ("REQ-01", "Ms. Sana (faculty)", "Grades database", dict(BASE, role="faculty", allowed_roles={"faculty", "registrar"})),
    ("REQ-02", "Ms. Sana (faculty)", "Grades database", dict(BASE, role="faculty", allowed_roles={"faculty", "registrar"},
                                                             network="public_wifi", hour=23)),
    ("REQ-03", "Bilal (student)", "Course portal", dict(BASE, role="student", allowed_roles={"student", "faculty"},
                                                        network="public_wifi")),
    ("REQ-04", "Bilal (student)", "Grades database", dict(BASE, role="student", allowed_roles={"faculty", "registrar"})),
    ("REQ-05", "Mr. Omer (HR)", "HR payroll", dict(BASE, role="hr", allowed_roles={"hr"}, country="AE", uba_score=50)),
    ("REQ-06", "Mr. Omer (HR)", "HR payroll", dict(BASE, role="hr", allowed_roles={"hr"}, device_compliant=False,
                                                   country="DE", hour=3, uba_score=80)),
    ("REQ-07", "Visitor", "Library catalogue", dict(BASE, role="guest", allowed_roles={"guest", "student", "faculty"},
                                                   device_compliant=False, network="public_wifi")),
]

print(f"{'Req':<7}{'User':<20}{'Resource':<18}{'Risk':>5}  Decision")
audit = []
for rid, user, res, sig in REQUESTS:
    decision, rule, r, why = decide(sig, res)
    print(f"{rid:<7}{user:<20}{res:<18}{r:>5}  {decision}")
    audit.append(f"{rid} | {rule} | factors: {'; '.join(why) if why else 'none'}")

print("\nAudit log (kept for compliance review):")
for line in audit:
    print("  " + line)
print("\nHuman oversight: users who are denied can raise a ticket; an analyst can override,")
print("and every override is logged with the analyst's name and reason.")
