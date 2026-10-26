"""Session 13 - Simple intrusion-detection rules over a connection log.

Detects three classic patterns in a recorded lab log:
  * port scan    : one source touches many different ports in a short time
  * brute force  : many failed logins for one account
  * data exfil   : unusually large outbound transfer
Run:  python session-13_ids_detect.py
"""
from collections import defaultdict

LOG = """\
09:00:01 10.1.7.7 10.1.5.20 443 ok 12000
09:00:02 10.1.7.8 10.1.5.20 443 ok 9000
09:01:10 10.1.66.6 10.1.5.30 21 refused 0
09:01:10 10.1.66.6 10.1.5.30 22 refused 0
09:01:11 10.1.66.6 10.1.5.30 23 refused 0
09:01:11 10.1.66.6 10.1.5.30 25 refused 0
09:01:11 10.1.66.6 10.1.5.30 80 ok 0
09:01:12 10.1.66.6 10.1.5.30 139 refused 0
09:01:12 10.1.66.6 10.1.5.30 445 refused 0
09:01:12 10.1.66.6 10.1.5.30 3389 refused 0
09:05:00 10.1.8.4 10.1.5.20 22 authfail 0
09:05:03 10.1.8.4 10.1.5.20 22 authfail 0
09:05:06 10.1.8.4 10.1.5.20 22 authfail 0
09:05:09 10.1.8.4 10.1.5.20 22 authfail 0
09:05:12 10.1.8.4 10.1.5.20 22 authfail 0
09:05:15 10.1.8.4 10.1.5.20 22 authfail 0
09:20:00 10.1.5.44 203.0.113.99 443 ok 2400000000
"""

SCAN_PORTS, SCAN_WINDOW = 5, 10        # >= 5 distinct ports within 10 s
BRUTE_FAILS = 5
EXFIL_BYTES = 500_000_000


def sec(t):
    h, m, s = map(int, t.split(":")); return h * 3600 + m * 60 + s


if __name__ == "__main__":
    ports = defaultdict(list); fails = defaultdict(int); alerts = []
    for line in LOG.strip().splitlines():
        t, src, dst, port, status, nbytes = line.split()
        ports[(src, dst)].append((sec(t), int(port)))
        recent = {p for ts, p in ports[(src, dst)] if sec(t) - ts <= SCAN_WINDOW}
        if len(recent) == SCAN_PORTS:
            alerts.append(f"{t} PORT SCAN   {src} -> {dst}: {sorted(recent)}")
        if status == "authfail":
            fails[(src, dst)] += 1
            if fails[(src, dst)] == BRUTE_FAILS:
                alerts.append(f"{t} BRUTE FORCE {src} -> {dst}:{port} {BRUTE_FAILS} failures")
        if int(nbytes) > EXFIL_BYTES:
            alerts.append(f"{t} LARGE UPLOAD {src} -> {dst}: {int(nbytes) / 1e9:.1f} GB")
    for a in alerts:
        print(a)
    print(f"\n{len(alerts)} alerts from {len(LOG.splitlines())} log lines")
