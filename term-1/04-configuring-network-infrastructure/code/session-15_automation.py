"""Session 15 - Network automation with JSON, templates and configuration drift checks.

1. Load the "source of truth" (session-15_inventory.json) and validate it.
2. Generate each switch's configuration from one template (no copy-paste errors).
3. Compare an intended config with what is running and report drift.
4. Convert data between JSON and Python to show why APIs use JSON.
Run:  python session-15_automation.py
"""
import difflib
import ipaddress
import json


def load_text(name):
    """Read a data file next to this script; on Colab, fetch it from the course repo."""
    try:
        return open(name).read()
    except FileNotFoundError:
        import urllib.request
        url = ("https://raw.githubusercontent.com/Hamnakhan123/Cybersecurity-and-Digital-Forensics/"
               "main/term-1/04-configuring-network-infrastructure/code/" + name)
        return urllib.request.urlopen(url).read().decode()


INV = json.loads(load_text("session-15_inventory.json"))


def validate(inv):
    errors = []
    ids = [v["id"] for v in inv["vlans"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate VLAN id")
    nets = [ipaddress.ip_network(v["subnet"]) for v in inv["vlans"]]
    for i, a in enumerate(nets):
        for b in nets[i + 1:]:
            if a.overlaps(b):
                errors.append(f"{a} overlaps {b}")
    for sw in inv["switches"]:
        for vid in sw["access"]:
            if int(vid) not in ids:
                errors.append(f"{sw['hostname']} uses undefined VLAN {vid}")
    return errors


def render(inv, sw):
    lines = [f"hostname {sw['hostname']}", f"ntp server {inv['ntp']}", f"logging host {inv['syslog']}"]
    for v in inv["vlans"]:
        lines += [f"vlan {v['id']}", f" name {v['name']}"]
    for vid, ports in sw["access"].items():
        prefix, rng = ports.split("/")
        lines += [f"interface range {prefix}/{rng.replace('-', ' - ')}",
                  " switchport mode access", f" switchport access vlan {vid}",
                  " switchport nonegotiate", " spanning-tree portfast"]
    lines += ["interface vlan 99", f" ip address {sw['mgmt_ip']} 255.255.255.0"]
    return lines


if __name__ == "__main__":
    print(f"Source of truth for {INV['site']}: {len(INV['vlans'])} VLANs, {len(INV['switches'])} switches")
    print("Validation:", validate(INV) or "OK")

    configs = {sw["hostname"]: render(INV, sw) for sw in INV["switches"]}
    print("\nGenerated config for ACC-SW1:")
    print("\n".join("  " + l for l in configs["ACC-SW1"]))

    running = configs["ACC-SW2"].copy()
    running[1] = "ntp server 10.0.0.1"                         # someone changed it by hand
    running.insert(5, " name TEMP-TEST")                       # and added an untracked name
    print("\nDrift check on ACC-SW2 (intended vs running):")
    diff = list(difflib.unified_diff(configs["ACC-SW2"], running, "intended", "running", lineterm="", n=0))
    print("\n".join("  " + d for d in diff))

    bad = json.loads(json.dumps(INV))
    bad["vlans"].append({"id": 30, "name": "LAB", "subnet": "192.168.21.0/24"})
    bad["switches"][1]["access"]["40"] = "Fa0/20-24"
    print("\nValidation of a bad change request:", validate(bad))
    print("\nJSON is just text: first 80 characters of the inventory ->", json.dumps(INV)[:80] + "...")
