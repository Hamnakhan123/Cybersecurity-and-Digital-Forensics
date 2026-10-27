"""Session 2 - Triage incident reports into cybercrime categories.

A cybercrime desk (police cyber unit, bank fraud team or company SOC) receives dozens
of reports a day written in plain language. This script uses a transparent keyword
scoring method to suggest a category, a target type (computer as TARGET or as TOOL),
and a priority, so a human analyst can review the queue faster.
It is deliberately simple and explainable: every decision shows the words that drove it.
All reports are fictional.
Run:  python session-02_crime_classifier.py
"""
import re

CATEGORIES = {
    # category: (keywords, computer is "target" or "tool", base priority 1-5)
    "Phishing / credential theft": (["link", "login", "password", "verify", "otp", "fake page"], "tool", 3),
    "Ransomware / malware":        (["encrypted", "ransom", "bitcoin", "files locked", "virus", "malware"], "target", 5),
    "Online financial fraud":      (["transferred", "jazzcash", "easypaisa", "card", "refund", "investment", "scheme"], "tool", 4),
    "Business email compromise":   (["invoice", "ceo", "bank details changed", "urgent payment", "supplier"], "tool", 5),
    "Identity theft":              (["cnic", "sim issued", "account opened", "my name", "impersonat"], "tool", 4),
    "Cyberstalking / harassment":  (["threat", "messages", "stalk", "harass", "blackmail", "photos"], "tool", 4),
    "Denial of service":           (["website down", "traffic flood", "ddos", "unavailable", "requests per second"], "target", 4),
    "Unauthorised access / hacking": (["hacked", "unknown login", "admin account", "accessed", "brute"], "target", 4),
    "Insider data theft":          (["employee", "usb", "copied", "resigned", "download"], "target", 4),
}

REPORTS = [
    "Received SMS saying my bank account is blocked, clicked the link and entered password and OTP on a fake page.",
    "All files on the accounts PC are encrypted and a note demands bitcoin as ransom.",
    "Our supplier emailed that their bank details changed; we paid the invoice of PKR 2.1 million to the new account.",
    "Someone opened a mobile wallet account using my CNIC and a SIM issued in my name.",
    "Our online store website is down, hosting says a traffic flood of 40,000 requests per second.",
    "An employee who resigned last week copied the customer database to a USB before leaving.",
    "A stranger keeps sending threat messages and says he will post my photos unless I pay.",
    "Lost my phone at the market.",
]


def classify(text):
    t = text.lower()
    scores = {}
    for cat, (words, _, _) in CATEGORIES.items():
        hits = [w for w in words if re.search(r"\b" + re.escape(w), t)]
        if hits:
            scores[cat] = hits
    if not scores:
        return None, [], "-", 1
    best = max(scores, key=lambda c: (len(scores[c]), CATEGORIES[c][2]))
    _, role, prio = CATEGORIES[best]
    money = re.search(r"(pkr|rs\.?)\s*[\d.,]+\s*(million|lakh)?", t)
    if money:
        prio = min(5, prio + 1)
    return best, scores[best], role, prio


def main():
    print(f"{'#':<3}{'Suggested category':<32}{'Computer as':<12}{'Prio':<6}Evidence words")
    print("-" * 92)
    queue = []
    for i, r in enumerate(REPORTS, 1):
        cat, hits, role, prio = classify(r)
        queue.append((prio, i, cat))
        print(f"{i:<3}{(cat or 'Not a cybercrime / refer'):<32}{role:<12}{prio:<6}{', '.join(hits)}")
    print("\nWork queue (highest priority first, human analyst confirms each one):")
    for prio, i, cat in sorted(queue, key=lambda x: (-x[0], x[1])):
        print(f"   P{prio}  report {i}: {cat or 'refer to general helpline'}")


if __name__ == "__main__":
    main()
