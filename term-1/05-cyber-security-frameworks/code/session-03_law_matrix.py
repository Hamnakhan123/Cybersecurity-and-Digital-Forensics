"""Session 3 - Which laws apply? A law-applicability matrix for fictional incidents.

Real incidents rarely involve one law. A breach at a Karachi company that serves
European customers can touch Pakistan's cybercrime law, its evidence law, the EU GDPR
and an industry standard all at once. This script describes each incident as a set of
facts ("tags"), keeps a small rule base of laws and the facts that trigger them, and
prints a matrix plus the reasons for every tick.

Teaching simplification only: the rule base is deliberately short and is NOT legal
advice. Laws are amended (Pakistan's PECA was amended in 2025, data-protection bills
change), so always check the current text and ask a lawyer.
Run:  python session-03_law_matrix.py
"""

# law code: (full name, kind, trigger tags (any one), what it gives the investigator)
# A cybercrime law only matters when a crime is suspected, so those laws also REQUIRE
# the tag "crime" (see REQUIRES). A purely accidental loss is a data-protection matter.
LAWS = {
    "PECA": ("Prevention of Electronic Crimes Act 2016 (Pakistan)", "cybercrime",
             {"offender_or_victim_pk", "system_in_pk"},
             "defines the offences (sections listed per incident below)"),
    "QSO+ETO": ("Qanun-e-Shahadat Order 1984 + Electronic Transactions Ordinance 2002 (Pakistan)",
                "evidence", {"court_in_pk"},
                "electronic documents and records are admissible; authenticity must be shown"),
    "GDPR": ("EU General Data Protection Regulation", "data protection",
             {"eu_personal_data"},
             "72-hour breach notice to the authority, data-subject rights, fines"),
    "CMA": ("Computer Misuse Act 1990 (UK)", "cybercrime", {"system_in_uk"},
            "unauthorised access and impairment offences"),
    "CFAA": ("Computer Fraud and Abuse Act (USA)", "cybercrime", {"system_in_us"},
             "unauthorised access to protected computers"),
    "HIPAA": ("Health Insurance Portability and Accountability Act (USA)", "sector privacy",
              {"us_health_data"}, "security and breach-notice duties for health data"),
    "PCI DSS": ("Payment Card Industry Data Security Standard", "contract standard",
                {"card_data"}, "not a law, but card brands and banks enforce it by contract"),
    "Budapest": ("Council of Europe Convention on Cybercrime (Budapest)", "treaty",
                 {"cross_border"},
                 "framework for cross-border evidence requests among parties; "
                 "check whether each country involved has joined"),
}

REQUIRES = {"PECA": {"crime"}, "CMA": {"crime"}, "CFAA": {"crime"}}

# Likely PECA sections per incident (teaching examples; a prosecutor decides the charge)
PECA_SECTIONS = {
    "A": "s3 unauthorised access, s4 unauthorised copying of data",
    "C": "s14 electronic fraud, s16 unauthorised use of identity information",
    "D": "s3 unauthorised access, s5 interference with data (the Pakistani firm's VPN was abused)",
    "E": "s16 identity misuse, s20 offences against dignity, s24 cyberstalking",
}

INCIDENTS = [
    ("A", "Ex-employee logs into a Karachi firm's ERP after leaving and copies the client list",
     {"crime", "offender_or_victim_pk", "system_in_pk", "court_in_pk"}),
    ("B", "Karachi call centre handling EU retail customers loses a laptop with their order history",
     {"system_in_pk", "eu_personal_data"}),
    ("C", "Phishing kit hosted in the UK steals card numbers from a Lahore online shop's customers",
     {"crime", "offender_or_victim_pk", "system_in_uk", "card_data", "cross_border", "court_in_pk"}),
    ("D", "Pakistani software house's US hospital client is hit by ransomware via a shared VPN",
     {"crime", "system_in_us", "us_health_data", "offender_or_victim_pk", "cross_border"}),
    ("E", "Student harasses a classmate with fake social-media profiles; case filed in Karachi",
     {"crime", "offender_or_victim_pk", "court_in_pk"}),
]


def applies(incident_tags, law_tags, code=None):
    if code and not REQUIRES.get(code, set()) <= incident_tags:
        return []
    return sorted(incident_tags & law_tags)


codes = list(LAWS)
print("Law applicability matrix (X = likely applies)\n")
print("Incident | " + " | ".join(f"{c:^8}" for c in codes))
print("-" * (11 + 11 * len(codes)))
for iid, _, tags in INCIDENTS:
    row = ["X" if applies(tags, LAWS[c][2], c) else "." for c in codes]
    print(f"   {iid}     | " + " | ".join(f"{r:^8}" for r in row))

print("\nWhy each tick:")
for iid, text, tags in INCIDENTS:
    print(f"\n{iid}. {text}")
    for c in codes:
        hit = applies(tags, LAWS[c][2], c)
        if hit:
            name, kind, _, gives = LAWS[c]
            if c == "PECA":
                gives = PECA_SECTIONS.get(iid, gives)
            print(f"   - {c} [{kind}] because {', '.join(hit)}: {gives}")

counts = {c: sum(1 for _, _, t in INCIDENTS if applies(t, LAWS[c][2], c)) for c in codes}
print("\nHow often each law was triggered:", ", ".join(f"{c}={n}" for c, n in counts.items()))
print("Lesson: one incident usually needs a cybercrime law (what is the offence?), an evidence")
print("law (will the court accept it?) and often a data-protection law (who must be told?).")
