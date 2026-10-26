"""Session 4 - Read a Cisco IOS running-config and audit it like an engineer.

Parses hostname, interfaces (address, status, description) and line settings
from a saved configuration file, then flags common security and hygiene
problems with the IOS command that fixes each one. Works on text only; it
never connects to a device.
Run:  python session-04_config_audit.py
"""
import re

def load_text(name):
    """Read a data file next to this script; on Colab, fetch it from the course repo."""
    try:
        return open(name).read()
    except FileNotFoundError:
        import urllib.request
        url = ("https://raw.githubusercontent.com/Hamnakhan123/Cybersecurity-and-Digital-Forensics/"
               "main/term-1/04-configuring-network-infrastructure/code/" + name)
        return urllib.request.urlopen(url).read().decode()


def parse(text):
    cfg = {"hostname": None, "interfaces": {}, "lines": {}, "globals": []}
    section = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.startswith("!"):
            section = None if line.startswith("!") else section
            continue
        if not line.startswith(" "):                  # a new top-level command
            section = None
            if line.startswith("hostname "):
                cfg["hostname"] = line.split()[1]
            elif line.startswith("interface "):
                section = ("if", line.split()[1])
                cfg["interfaces"][section[1]] = {"ip": None, "shutdown": False, "description": ""}
            elif line.startswith("line "):
                section = ("line", " ".join(line.split()[1:]))
                cfg["lines"][section[1]] = []
            else:
                cfg["globals"].append(line)
        elif section and section[0] == "if":
            sub = line.strip(); intf = cfg["interfaces"][section[1]]
            if sub.startswith("ip address "):
                intf["ip"] = " ".join(sub.split()[2:4])
            elif sub == "shutdown":
                intf["shutdown"] = True
            elif sub.startswith("description "):
                intf["description"] = sub[12:]
        elif section and section[0] == "line":
            cfg["lines"][section[1]].append(line.strip())
    return cfg


def audit(cfg):
    g = cfg["globals"]
    findings = []
    if any(x.startswith("enable password") for x in g) and not any(x.startswith("enable secret") for x in g):
        findings.append(("HIGH", "enable password stored weakly", "enable secret <strong-password>"))
    if "ip http server" in g:
        findings.append(("MEDIUM", "HTTP management server is on", "no ip http server"))
    if not any(x.startswith("banner") for x in g):
        findings.append(("LOW", "no login banner", "banner motd # Authorised access only #"))
    if "service password-encryption" not in g:
        findings.append(("LOW", "line passwords visible in clear text", "service password-encryption"))
    for name, cmds in cfg["lines"].items():
        if any("telnet" in c for c in cmds if c.startswith("transport input")):
            findings.append(("HIGH", f"line {name} accepts Telnet (clear text)", "transport input ssh"))
        if any(c.startswith("password cisco") for c in cmds):
            findings.append(("HIGH", f"line {name} uses a default password", "username admin secret ... + login local"))
        if not any(c.startswith("exec-timeout") for c in cmds):
            findings.append(("LOW", f"line {name} has no idle timeout", "exec-timeout 10 0"))
    for name, i in cfg["interfaces"].items():
        if not i["description"]:
            findings.append(("LOW", f"{name} has no description", "description <purpose>"))
    return findings


if __name__ == "__main__":
    cfg = parse(load_text("session-04_running-config.txt"))
    print(f"Device: {cfg['hostname']}")
    print(f"{'Interface':22} {'IP address / mask':32} {'Status':22} Description")
    for name, i in cfg["interfaces"].items():
        status = "administratively down" if i["shutdown"] else "enabled"
        print(f"{name:22} {i['ip'] or 'unassigned':32} {status:22} {i['description']}")
    findings = audit(cfg)
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    print(f"\n{len(findings)} findings")
    for sev, what, fix in sorted(findings, key=lambda f: order[f[0]]):
        print(f"  [{sev:6}] {what:42} fix: {fix}")
