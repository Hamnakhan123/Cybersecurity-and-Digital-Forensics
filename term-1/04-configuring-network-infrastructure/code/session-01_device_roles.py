"""Session 1 - Pick the right device for each networking job.

Each device works at a different layer and makes decisions with a different
address. Given a list of requirements, this script recommends a device and
explains why, then checks a small office design against the criteria of a
good network (performance, reliability, scalability, security, manageability).
Run:  python session-01_device_roles.py
"""

DEVICES = {
    "hub":          {"layer": 1, "uses": "nothing (repeats bits to every port)"},
    "switch":       {"layer": 2, "uses": "MAC addresses (MAC address table)"},
    "router":       {"layer": 3, "uses": "IP addresses (routing table)"},
    "multilayer switch": {"layer": 3, "uses": "MAC and IP addresses in hardware"},
    "firewall":     {"layer": 4, "uses": "IPs, ports and connection state (rules)"},
    "access point": {"layer": 2, "uses": "MAC addresses (bridges Wi-Fi to Ethernet)"},
    "wireless LAN controller": {"layer": 2, "uses": "AP inventory and policies (manages many APs centrally)"},
}

NEEDS = [
    ("Connect 24 PCs in one lab so they can share files", "switch"),
    ("Join the lab network to the internet", "router"),
    ("Route between 10 VLANs at wire speed in the server room", "multilayer switch"),
    ("Allow only HTTPS from the internet to the web server", "firewall"),
    ("Give laptops Wi-Fi in the library", "access point"),
    ("Manage 60 access points from one dashboard", "wireless LAN controller"),
]


def score_design(design):
    """Return (criterion, ok, reason) tuples for a simple design dictionary."""
    checks = [
        ("Performance", design["uplink_gbps"] >= 1, f"uplink {design['uplink_gbps']} Gbps"),
        ("Reliability", design["redundant_uplinks"] >= 2, f"{design['redundant_uplinks']} uplink(s)"),
        ("Scalability", design["free_ports_pct"] >= 20, f"{design['free_ports_pct']}% ports free"),
        ("Security", design["guest_isolated"] and not design["telnet_enabled"],
         f"guest isolated={design['guest_isolated']}, telnet={design['telnet_enabled']}"),
        ("Manageability", design["central_logging"], f"central logging={design['central_logging']}"),
    ]
    return checks


if __name__ == "__main__":
    print("Requirement -> recommended device")
    for need, dev in NEEDS:
        d = DEVICES[dev]
        print(f" - {need}\n     => {dev} (layer {d['layer']}, decides using {d['uses']})")

    for name, design in [
        ("Version 1 (first draft)", dict(uplink_gbps=0.1, redundant_uplinks=1, free_ports_pct=5,
                                         guest_isolated=False, telnet_enabled=True, central_logging=False)),
        ("Version 2 (improved)", dict(uplink_gbps=10, redundant_uplinks=2, free_ports_pct=30,
                                      guest_isolated=True, telnet_enabled=False, central_logging=True)),
    ]:
        checks = score_design(design)
        passed = sum(ok for _, ok, _ in checks)
        print(f"\n{name}: {passed}/{len(checks)} criteria met")
        for crit, ok, why in checks:
            print(f"   [{'PASS' if ok else 'FAIL'}] {crit:13} {why}")
