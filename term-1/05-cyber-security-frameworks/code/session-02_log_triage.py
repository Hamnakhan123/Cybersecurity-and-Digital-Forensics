"""Session 2 - Threat detection from authentication logs (a tiny SIEM rule engine).

Incident responders start from logs. This script parses fictional VPN/web login
events and applies three classic detection rules:
  R1 brute force      : >= 5 failed logins for one account from one IP within 10 minutes
  R2 password spraying: one IP fails against >= 4 different accounts within 10 minutes
  R3 impossible travel: the same user logs in successfully from two countries
                        faster than a plane could fly between them (> 900 km/h)
It then prints alerts and a merged timeline - the first artefact of any investigation.
IP addresses are from the documentation ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24).
Run:  python session-02_log_triage.py
"""
import math
from collections import defaultdict
from datetime import datetime, timedelta

LOG = """\
2026-10-20T08:58:10 SUCCESS user=asad ip=192.0.2.10 geo=Karachi,PK
2026-10-20T09:01:02 FAIL user=finance ip=203.0.113.66 geo=Unknown,XX
2026-10-20T09:01:20 FAIL user=finance ip=203.0.113.66 geo=Unknown,XX
2026-10-20T09:01:41 FAIL user=finance ip=203.0.113.66 geo=Unknown,XX
2026-10-20T09:02:05 FAIL user=finance ip=203.0.113.66 geo=Unknown,XX
2026-10-20T09:02:30 FAIL user=finance ip=203.0.113.66 geo=Unknown,XX
2026-10-20T09:02:58 SUCCESS user=finance ip=203.0.113.66 geo=Unknown,XX
2026-10-20T09:10:00 FAIL user=hr ip=198.51.100.23 geo=Frankfurt,DE
2026-10-20T09:10:04 FAIL user=it-admin ip=198.51.100.23 geo=Frankfurt,DE
2026-10-20T09:10:09 FAIL user=sana ip=198.51.100.23 geo=Frankfurt,DE
2026-10-20T09:10:13 FAIL user=asad ip=198.51.100.23 geo=Frankfurt,DE
2026-10-20T09:10:18 FAIL user=reception ip=198.51.100.23 geo=Frankfurt,DE
2026-10-20T09:40:00 SUCCESS user=asad ip=198.51.100.99 geo=London,GB
2026-10-20T10:15:00 FAIL user=sana ip=192.0.2.11 geo=Karachi,PK
2026-10-20T10:15:20 SUCCESS user=sana ip=192.0.2.11 geo=Karachi,PK
"""
CITY = {"Karachi": (24.86, 67.01), "Frankfurt": (50.11, 8.68), "London": (51.51, -0.13)}
WINDOW = timedelta(minutes=10)


def parse(line):
    ts, result, *kv = line.split()
    d = dict(x.split("=", 1) for x in kv)
    d["time"], d["result"] = datetime.fromisoformat(ts), result
    d["city"] = d["geo"].split(",")[0]
    return d


def km(a, b):
    """Great-circle distance (haversine)."""
    (la1, lo1), (la2, lo2) = [tuple(map(math.radians, p)) for p in (a, b)]
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def detect(events):
    alerts = []
    fails = [e for e in events if e["result"] == "FAIL"]
    by_pair = defaultdict(list)
    for e in fails:
        by_pair[(e["user"], e["ip"])].append(e["time"])
    for (user, ip), times in by_pair.items():
        for i in range(len(times)):
            if len([t for t in times[i:] if t - times[i] <= WINDOW]) >= 5:
                ok = [e for e in events if e["user"] == user and e["ip"] == ip and e["result"] == "SUCCESS"]
                sev = "CRITICAL (followed by a successful login!)" if ok else "HIGH"
                alerts.append((times[i], "R1 brute force", f"{user} from {ip}", sev))
                break
    by_ip = defaultdict(list)
    for e in fails:
        by_ip[e["ip"]].append(e)
    for ip, evs in by_ip.items():
        users = {e["user"] for e in evs if e["time"] - evs[0]["time"] <= WINDOW}
        if len(users) >= 4:
            alerts.append((evs[0]["time"], "R2 password spraying", f"{ip} tried {len(users)} accounts", "HIGH"))
    last = {}
    for e in [e for e in events if e["result"] == "SUCCESS"]:
        prev = last.get(e["user"])
        if prev and prev["city"] in CITY and e["city"] in CITY and prev["city"] != e["city"]:
            dist = km(CITY[prev["city"]], CITY[e["city"]])
            hours = (e["time"] - prev["time"]).total_seconds() / 3600
            speed = dist / hours
            if speed > 900:
                alerts.append((e["time"], "R3 impossible travel",
                               f"{e['user']}: {prev['city']} -> {e['city']} {dist:,.0f} km in {hours*60:.0f} min "
                               f"= {speed:,.0f} km/h", "HIGH"))
        last[e["user"]] = e
    return sorted(alerts)


def main():
    events = [parse(l) for l in LOG.strip().splitlines()]
    print(f"Parsed {len(events)} events, {sum(e['result']=='FAIL' for e in events)} failures\n")
    print("ALERTS")
    for t, rule, what, sev in detect(events):
        print(f"  {t:%H:%M:%S}  {rule:<22} {what:<58} {sev}")
    print("\nTIMELINE for the compromised 'finance' account")
    for e in events:
        if e["user"] == "finance":
            print(f"  {e['time']:%H:%M:%S}  {e['result']:<8} {e['ip']:<15} {e['geo']}")
    print("\nNext steps for the responder: disable 'finance', reset password, enforce MFA,")
    print("block 203.0.113.66 and 198.51.100.23, check what 'finance' accessed after 09:02:58,")
    print("and confirm with Asad whether the London login was really him (VPN? travel?).")


if __name__ == "__main__":
    main()
