"""Session 11 - Audit a switch/router configuration against a hardening policy.

Reads a saved configuration (session-11_router.cfg, a made-up lab device) and
checks it against the organisation's baseline. This is what configuration
compliance tools do every night.
Run:  python session-11_policy_audit.py
"""
import re

CHECKS = [  # (id, description, regex that MUST be present or must be absent, must_exist)
    ("H1", "Passwords stored with strong secret (not 'enable password')", r"^enable (algorithm-type \S+ )?secret", True),
    ("H2", "No plain 'enable password' line", r"^enable password", False),
    ("H3", "Password encryption service on", r"^service password-encryption", True),
    ("H4", "SSH version 2 only", r"^ip ssh version 2", True),
    ("H5", "Telnet not allowed on VTY lines", r"transport input .*telnet", False),
    ("H6", "Login banner present", r"^banner (motd|login)", True),
    ("H7", "HTTP server disabled", r"^no ip http server", True),
    ("H8", "SNMP default community 'public' not used", r"^snmp-server community public", False),
    ("H9", "Logging to a central syslog server", r"^logging host \S+", True),
    ("H10", "NTP configured", r"^ntp server \S+", True),
    ("H11", "Idle sessions time out (exec-timeout not 0 0)", r"exec-timeout 0 0", False),
    ("H12", "Unused interfaces shut down", None, True),
]


def unused_up(cfg):
    """Interfaces described as UNUSED that are not shut down."""
    bad = []
    for block in re.split(r"\n(?=interface )", cfg):
        if block.startswith("interface") and "UNUSED" in block and "shutdown" not in block:
            bad.append(block.splitlines()[0].split()[1])
    return bad


def audit(cfg):
    results = []
    for cid, desc, rx, must in CHECKS:
        if cid == "H12":
            bad = unused_up(cfg)
            results.append((cid, desc, not bad, ", ".join(bad)))
            continue
        found = re.search(rx, cfg, re.M) is not None
        results.append((cid, desc, found == must, ""))
    return results


if __name__ == "__main__":
    try:
        cfg = open("session-11_router.cfg").read()
    except FileNotFoundError:          # e.g. running on Colab: fetch the sample from the repo
        import urllib.request
        url = ("https://raw.githubusercontent.com/Hamnakhan123/Cybersecurity-and-Digital-Forensics/"
               "main/term-1/03-computer-networks/code/session-11_router.cfg")
        cfg = urllib.request.urlopen(url).read().decode()
    res = audit(cfg)
    for cid, desc, ok, extra in res:
        print(f"{'PASS' if ok else 'FAIL'}  {cid:<4} {desc}{'  -> ' + extra if extra else ''}")
    score = sum(r[2] for r in res)
    print(f"\nCompliance: {score}/{len(res)} = {score / len(res):.0%}")
