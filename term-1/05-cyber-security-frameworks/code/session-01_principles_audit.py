"""Session 1 - Audit a record of processing activities against the GDPR principles.

A "record of processing activities" (ROPA) is the list every organisation keeps of
WHAT personal data it processes, WHY, on WHICH lawful basis, for HOW LONG and HOW it
is protected. This script checks each activity against the seven principles of
Article 5 and the six lawful bases of Article 6, then prints a findings report.

All organisations, people and data below are fictional teaching examples.
Run:  python session-01_principles_audit.py
"""

LAWFUL_BASES = {"consent", "contract", "legal_obligation",
                "vital_interests", "public_task", "legitimate_interests"}

# Each activity is one row of the ROPA of a fictional online bookshop.
ROPA = [
    {"name": "Order fulfilment", "purpose": "deliver books to customers",
     "basis": "contract", "fields": ["name", "address", "phone", "email"],
     "needed": ["name", "address", "phone", "email"],
     "retention_days": 2190, "retention_reason": "tax law requires 6 years",
     "encrypted": True, "access_roles": ["warehouse", "support"],
     "privacy_notice": True, "last_accuracy_check_days": 30, "dpia_done": True},
    {"name": "Marketing newsletter", "purpose": "send offers by email",
     "basis": "consent", "consent_recorded": False, "fields": ["email", "name", "date_of_birth"],
     "needed": ["email", "name"], "retention_days": None, "retention_reason": "",
     "encrypted": True, "access_roles": ["marketing"],
     "privacy_notice": True, "last_accuracy_check_days": 400, "dpia_done": False},
    {"name": "CCTV in warehouse", "purpose": "prevent theft",
     "basis": "legitimate_interests", "lia_done": True, "fields": ["video_image"],
     "needed": ["video_image"], "retention_days": 30, "retention_reason": "investigate incidents",
     "encrypted": False, "access_roles": ["security", "everyone"],
     "privacy_notice": False, "last_accuracy_check_days": 0, "dpia_done": True},
    {"name": "Customer profiling", "purpose": "",
     "basis": "unknown", "fields": ["browsing_history", "location", "email", "religion"],
     "needed": ["browsing_history"], "retention_days": 3650, "retention_reason": "might be useful",
     "encrypted": False, "access_roles": ["analytics"],
     "privacy_notice": False, "last_accuracy_check_days": 90, "dpia_done": False},
]

SPECIAL_CATEGORY = {"religion", "health", "ethnicity", "biometric", "sexual_orientation",
                    "political_opinion", "trade_union", "genetic"}


def audit(act):
    """Return a list of (principle, finding) tuples for one activity."""
    f = []
    # 1. Lawfulness, fairness and transparency
    if act["basis"] not in LAWFUL_BASES:
        f.append(("Lawfulness", "no valid Article 6 lawful basis recorded"))
    if act["basis"] == "consent" and not act.get("consent_recorded"):
        f.append(("Lawfulness", "consent is the basis but no proof of consent is stored"))
    if act["basis"] == "legitimate_interests" and not act.get("lia_done"):
        f.append(("Lawfulness", "legitimate interests used without a balancing test (LIA)"))
    if not act["privacy_notice"]:
        f.append(("Transparency", "people are not told about this processing"))
    # 2. Purpose limitation
    if not act["purpose"].strip():
        f.append(("Purpose limitation", "purpose is blank or vague"))
    # 3. Data minimisation
    extra = sorted(set(act["fields"]) - set(act["needed"]))
    if extra:
        f.append(("Data minimisation", "collects fields not needed: " + ", ".join(extra)))
    special = sorted(set(act["fields"]) & SPECIAL_CATEGORY)
    if special:
        f.append(("Lawfulness", "special-category data (" + ", ".join(special) + ") needs an Article 9 condition"))
    # 4. Accuracy
    if act["last_accuracy_check_days"] > 365:
        f.append(("Accuracy", f"data not reviewed for {act['last_accuracy_check_days']} days"))
    # 5. Storage limitation
    if act["retention_days"] is None:
        f.append(("Storage limitation", "no retention period defined"))
    elif "might" in act["retention_reason"] or not act["retention_reason"]:
        f.append(("Storage limitation", f"{act['retention_days']} days kept without a real reason"))
    # 6. Integrity and confidentiality (security)
    if not act["encrypted"]:
        f.append(("Integrity & confidentiality", "data is not encrypted at rest"))
    if "everyone" in act["access_roles"]:
        f.append(("Integrity & confidentiality", "access not restricted (role 'everyone')"))
    # 7. Accountability
    if not act["dpia_done"] and (special or "profiling" in act["name"].lower()):
        f.append(("Accountability", "high-risk processing without a DPIA"))
    return f


def main():
    total = 0
    print("GDPR principles audit - fictional online bookshop")
    print("=" * 62)
    for act in ROPA:
        findings = audit(act)
        total += len(findings)
        status = "PASS" if not findings else f"{len(findings)} issue(s)"
        print(f"\n[{status}] {act['name']}  (basis: {act['basis']})")
        for principle, text in findings:
            print(f"   - {principle:<28} {text}")
    print("\n" + "=" * 62)
    by_principle = {}
    for act in ROPA:
        for p, _ in audit(act):
            by_principle[p] = by_principle.get(p, 0) + 1
    print(f"Total findings: {total}")
    for p, n in sorted(by_principle.items(), key=lambda x: (-x[1], x[0])):
        print(f"   {p:<28} {'#' * n} {n}")


if __name__ == "__main__":
    main()
