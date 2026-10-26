"""Session 10 - A tiny syslog collector on localhost plus a log analyser.

1. Starts a UDP syslog listener on 127.0.0.1 (random high port, not 514,
   so no admin rights are needed).
2. "Devices" send RFC 3164-style messages: <PRI>timestamp host message,
   where PRI = facility * 8 + severity.
3. The collector decodes facility/severity and summarises what needs attention.
Run:  python session-10_syslog_monitor.py
"""
import re
import socket
import threading
import time
from collections import Counter

SEVERITY = ["Emergency", "Alert", "Critical", "Error", "Warning", "Notice", "Informational", "Debug"]
FACILITY = {0: "kern", 1: "user", 4: "auth", 10: "authpriv", 16: "local0", 23: "local7"}

MESSAGES = [  # (facility, severity, host, text)
    (23, 5, "core-sw1", "%LINK-5-CHANGED: Interface Gi1/0/24, changed state to up"),
    (23, 3, "core-sw1", "%LINK-3-UPDOWN: Interface Gi1/0/7, changed state to down"),
    (4, 4, "fw1", "Deny tcp src outside:198.51.100.7/51022 dst inside:10.1.5.20/3389"),
    (4, 4, "fw1", "Deny tcp src outside:198.51.100.7/51023 dst inside:10.1.5.21/3389"),
    (10, 5, "web01", "sshd: Failed password for admin from 10.1.9.50"),
    (10, 5, "web01", "sshd: Failed password for admin from 10.1.9.50"),
    (10, 6, "web01", "sshd: Accepted publickey for deploy from 10.1.9.10"),
    (23, 2, "edge-r1", "%SYS-2-MALLOCFAIL: Memory allocation failed"),
    (16, 6, "app01", "health check OK in 42 ms"),
]

received = []


def collector(sock, expected):
    while len(received) < expected:
        data, _ = sock.recvfrom(2048)
        received.append(data.decode())


def parse(line):
    m = re.match(r"<(\d+)>(\w{3} +\d+ [\d:]+) (\S+) (.*)", line)
    pri = int(m.group(1))
    return {"facility": FACILITY.get(pri // 8, pri // 8), "severity": pri % 8,
            "time": m.group(2), "host": m.group(3), "msg": m.group(4)}


if __name__ == "__main__":
    srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    srv.bind(("127.0.0.1", 0))
    port = srv.getsockname()[1]
    th = threading.Thread(target=collector, args=(srv, len(MESSAGES)), daemon=True)
    th.start()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dev:
        for i, (fac, sev, host, text) in enumerate(MESSAGES):
            line = f"<{fac * 8 + sev}>Oct 26 09:{10 + i:02d}:00 {host} {text}"
            dev.sendto(line.encode(), ("127.0.0.1", port))
            time.sleep(0.01)
    th.join(timeout=2)

    events = [parse(l) for l in received]
    print(f"Collected {len(events)} messages. First raw line: {received[0]}")
    print("\nBy severity:")
    for sev, n in sorted(Counter(e["severity"] for e in events).items()):
        print(f"  {sev} {SEVERITY[sev]:<14} {'#' * n} {n}")
    print("\nNeeds attention now (severity 0-3):")
    for e in events:
        if e["severity"] <= 3:
            print(f"  {e['time']} {e['host']:<8} {SEVERITY[e['severity']]:<9} {e['msg']}")
    fails = Counter(re.search(r"from (\S+)", e["msg"]).group(1) for e in events if "Failed password" in e["msg"])
    denies = Counter(re.search(r"outside:([\d.]+)", e["msg"]).group(1) for e in events if e["msg"].startswith("Deny"))
    print("\nSecurity patterns:", dict(fails), "failed SSH;", dict(denies), "blocked RDP attempts")
