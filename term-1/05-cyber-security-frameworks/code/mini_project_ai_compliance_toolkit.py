"""Module 5 mini project - AI security compliance toolkit.

Before an organisation lets AI enforce its security policies, it should keep a
REGISTER of every AI system and check each one against a set of controls. This toolkit:

  1. assigns a risk tier to each system (simplified from the EU AI Act idea of
     minimal / limited / high risk; education and employment uses are high risk),
  2. scores each system against 11 controls mapped to the NIST AI RMF functions
     (GOVERN, MAP, MEASURE, MANAGE) and to GDPR / EU AI Act / ISO/IEC 42001 ideas,
  3. prints a compliance percentage, a RAG rating and a prioritised action plan.

Status codes: Y = done, P = partly done, N = not done, - = not applicable.
High-risk systems must have every weight-3 control at Y to be "READY".
Teaching simplification, not legal advice. All systems are fictional.
Run:  python mini_project_ai_compliance_toolkit.py
"""

CONTROLS = [  # (id, control, NIST AI RMF function, reference, weight 1-3)
    ("C01", "Owner, purpose and scope documented", "GOVERN", "ISO/IEC 42001 roles and AI policy", 2),
    ("C02", "Impact assessment / DPIA completed", "MAP", "GDPR Art 35; AI Act risk management", 3),
    ("C03", "Training data checked for quality and bias", "MAP", "AI Act Art 10 data governance", 3),
    ("C04", "Accuracy and fairness tested before release", "MEASURE", "AI Act Art 15; NIST MEASURE", 3),
    ("C05", "Drift monitored in production", "MEASURE", "NIST MEASURE; ISO/IEC 42001 monitoring", 2),
    ("C06", "Human review of high-impact decisions", "MANAGE", "GDPR Art 22; AI Act Art 14", 3),
    ("C07", "Decisions explainable and logged", "MANAGE", "AI Act Art 12; GDPR accountability", 2),
    ("C08", "Adversarial / prompt-injection testing", "MEASURE", "AI Act Art 15; MITRE ATLAS; OWASP LLM Top 10", 2),
    ("C09", "People told when AI is used", "GOVERN", "AI Act Art 50; GDPR Art 13-14", 1),
    ("C10", "Data minimised, retention period set", "MAP", "GDPR Art 5", 2),
    ("C11", "AI incident response and rollback plan", "MANAGE", "ISO/IEC 42001; NIST MANAGE", 2),
]

SYSTEMS = {  # name: (use, interacts with public?, decides about people in education/jobs?, statuses C01..C11)
    "UBA login model": ("flags risky logins, forces MFA", False, False,
                        "Y Y P P P Y Y N P Y P"),
    "Email phishing filter": ("quarantines suspicious email", False, False,
                              "Y P Y Y Y P Y P - Y Y"),
    "Exam proctoring AI": ("flags possible cheating in online exams", True, True,
                           "Y N N P N P P N Y P N"),
    "IT helpdesk chatbot": ("answers password and VPN questions", True, False,
                            "Y Y P Y P - P P N Y Y"),
}
VALUE = {"Y": 1.0, "P": 0.5, "N": 0.0}


def tier(public, high_impact):
    if high_impact:
        return "HIGH"
    return "LIMITED (transparency duties)" if public else "MINIMAL"


def assess(statuses, risk_tier):
    got = possible = 0
    gaps = []
    for (cid, name, fn, ref, w), s in zip(CONTROLS, statuses.split()):
        if s == "-":
            continue
        possible += w
        got += w * VALUE[s]
        if s != "Y":
            priority = w + (2 if risk_tier == "HIGH" else 0) + (1 if s == "N" else 0)
            gaps.append((priority, cid, name, fn, ref, s))
    pct = 100 * got / possible
    weight3 = {c[0] for c in CONTROLS if c[4] == 3}
    blocked = risk_tier == "HIGH" and any(g[1] in weight3 for g in gaps)
    rag = "GREEN" if pct >= 85 else "AMBER" if pct >= 60 else "RED"
    return pct, rag, blocked, sorted(gaps, reverse=True)


print("AI SYSTEM REGISTER - Clifton Institute of Technology (fictional)\n")
print(f"{'System':<23}{'Tier':<31}{'Score':>6}  Rating")
results = {}
for name, (use, public, high, statuses) in SYSTEMS.items():
    t = tier(public, high)
    pct, rag, blocked, gaps = assess(statuses, t)
    results[name] = (t, gaps, blocked)
    status = "NOT READY" if blocked else rag
    print(f"{name:<23}{t:<31}{pct:5.0f}%  {status}")

print("\nCoverage by NIST AI RMF function (share of controls fully done, all systems):")
for fn in ("GOVERN", "MAP", "MEASURE", "MANAGE"):
    idx = [i for i, c in enumerate(CONTROLS) if c[2] == fn]
    cells = [SYSTEMS[s][3].split()[i] for s in SYSTEMS for i in idx]
    applicable = [c for c in cells if c != "-"]
    done = sum(c == "Y" for c in applicable)
    print(f"  {fn:<8} {done:>2}/{len(applicable):<2} {'#' * done}")

print("\nTop actions (highest priority first):")
plan = [(p, name, cid, ctl, ref, s) for name, (t, gaps, _) in results.items()
        for p, cid, ctl, fn, ref, s in gaps]
for p, name, cid, ctl, ref, s in sorted(plan, reverse=True)[:8]:
    print(f"  P{p} {name:<22} {cid} {ctl} [{s}] ({ref})")

print("\nRule: a HIGH-risk system marked NOT READY must not make decisions on its own;")
print("its flags go to a trained human reviewer until every weight-3 control is done.")
