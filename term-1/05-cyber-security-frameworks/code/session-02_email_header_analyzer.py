"""Session 2 - Analyse a suspicious email's headers (phishing investigation and OSINT).

Email headers are a goldmine for investigators. This script parses a fictional
phishing email with Python's standard email library and checks:
  * the path the message took (Received headers, read bottom-up),
  * authentication results (SPF, DKIM, DMARC),
  * mismatches between From, Reply-To and Return-Path,
  * look-alike domains (typosquatting) compared with the real brand domain,
  * URLs in the body, printed in DEFANGED form (hxxps, [.]) so nobody clicks them.
Domains use the reserved example/test names; IPs are documentation ranges.
Run:  python session-02_email_header_analyzer.py
"""
import re
from email import message_from_string
from email.utils import parseaddr

RAW = """\
Received: from mail.corp-mailhost.example (mail.corp-mailhost.example [192.0.2.25])
\tby mx.university.example; Tue, 20 Oct 2026 10:02:11 +0500
Received: from unknown-host (unknown [203.0.113.45])
\tby mail.corp-mailhost.example; Tue, 20 Oct 2026 05:02:07 +0000
Authentication-Results: mx.university.example;
\tspf=fail smtp.mailfrom=bulk-sender.test;
\tdkim=none;
\tdmarc=fail header.from=metr0bank-secure.example
Return-Path: <bounce@bulk-sender.test>
From: "MetroBank Security" <security@metr0bank-secure.example>
Reply-To: helpdesk.verify@freemail.test
To: student@university.example
Subject: URGENT: Your account will be suspended in 24 hours
Date: Tue, 20 Oct 2026 05:02:05 +0000
Message-ID: <x81@unknown-host>
Content-Type: text/plain

Dear customer, we detected unusual activity. Verify now at
https://metr0bank-secure.example/login?id=88231 or your account will be closed.
Download the form: http://203.0.113.45/forms/verify.zip
"""
REAL_BRAND = "metrobank.example"
HOMOGLYPHS = str.maketrans({"1": "l", "0": "o", "3": "e", "5": "s"})  # digit -> letter it imitates


def defang(url):
    return url.replace("http", "hxxp").replace(".", "[.]")


def lookalike(domain, real):
    base = domain.split(".")[0].split("-")[0]
    return base.translate(HOMOGLYPHS) == real.split(".")[0] and domain != real


def main():
    msg = message_from_string(RAW)
    score, reasons = 0, []
    print("1) Delivery path (oldest hop at the bottom):")
    for i, hop in enumerate(reversed(msg.get_all("Received")), 1):
        hop = " ".join(hop.split())
        ip = re.search(r"\[([\d.]+)\]", hop)
        print(f"   hop {i}: {hop.split(';')[0][:70]}  ip={ip.group(1) if ip else '?'}")
    auth = " ".join(msg["Authentication-Results"].split())
    print("\n2) Authentication:")
    for mech in ("spf", "dkim", "dmarc"):
        res = re.search(mech + r"=(\w+)", auth).group(1)
        print(f"   {mech.upper():<6} {res}")
        if res != "pass":
            score += 2
            reasons.append(f"{mech.upper()} {res}")
    frm = parseaddr(msg["From"])[1].split("@")[1]
    rto = parseaddr(msg["Reply-To"])[1].split("@")[1]
    rpath = parseaddr(msg["Return-Path"])[1].split("@")[1]
    print(f"\n3) Domains: From={frm}  Reply-To={rto}  Return-Path={rpath}")
    if len({frm, rto, rpath}) > 1:
        score += 2
        reasons.append("From / Reply-To / Return-Path domains differ")
    if lookalike(frm, REAL_BRAND):
        score += 3
        reasons.append(f"look-alike of {REAL_BRAND} ('0' used instead of 'o')")
    body = msg.get_payload()
    urls = re.findall(r"https?://\S+", body)
    print("\n4) URLs in body (defanged):")
    for u in urls:
        print("   ", defang(u))
        if re.match(r"https?://\d+\.\d+\.\d+\.\d+", u):
            score += 2
            reasons.append("link to a raw IP address")
        if u.endswith((".zip", ".exe", ".js", ".iso")):
            score += 2
            reasons.append("link downloads an archive/executable")
    if re.search(r"urgent|suspend|24 hours|closed", (msg["Subject"] + body).lower()):
        score += 1
        reasons.append("pressure / urgency language")
    verdict = "PHISHING - block and report" if score >= 8 else "SUSPICIOUS" if score >= 4 else "Probably fine"
    print(f"\n5) Risk score {score}: {verdict}")
    for r in reasons:
        print("   -", r)
    print("\nIOCs to share with the SOC: 203.0.113.45, metr0bank-secure.example, bulk-sender.test,"
          " freemail.test reply address")


if __name__ == "__main__":
    main()
