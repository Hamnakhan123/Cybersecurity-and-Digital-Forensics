"""Session 8 - ARP cache behaviour and a defensive ARP-spoofing detector.

ARP maps an IPv4 address to a MAC address on the local network. Because ARP
has no authentication, an attacker on the LAN can send fake replies. A monitor
(like the classic `arpwatch` tool) flags when an IP suddenly changes MAC.
The events below are a recorded lab capture, not live traffic.
Run:  python session-08_arp_watch.py
"""

EVENTS = [  # (time, type, sender IP, sender MAC)
    ("10:00:01", "reply",  "192.168.1.1",  "00:11:22:33:44:01"),   # gateway
    ("10:00:03", "reply",  "192.168.1.20", "00:11:22:33:44:20"),
    ("10:00:09", "reply",  "192.168.1.30", "00:11:22:33:44:30"),
    ("10:05:00", "garp",   "192.168.1.20", "00:11:22:33:44:20"),   # normal refresh
    ("10:07:12", "reply",  "192.168.1.1",  "de:ad:be:ef:00:66"),   # gateway IP, new MAC!
    ("10:07:13", "reply",  "192.168.1.30", "de:ad:be:ef:00:66"),   # same MAC claims a 2nd IP
    ("10:07:14", "reply",  "192.168.1.1",  "de:ad:be:ef:00:66"),
]
CRITICAL = {"192.168.1.1": "default gateway"}


def watch(events):
    table, alerts, mac_to_ips, seen = {}, [], {}, set()
    for t, kind, ip, mac in events:
        old = table.get(ip)
        if old and old != mac:
            sev = "CRITICAL" if ip in CRITICAL else "WARNING"
            alerts.append(f"{t} {sev}: {ip} changed {old} -> {mac}")
        table[ip] = mac
        mac_to_ips.setdefault(mac, set()).add(ip)
        key = (mac, frozenset(mac_to_ips[mac]))
        if len(mac_to_ips[mac]) > 1 and key not in seen:
            seen.add(key)
            alerts.append(f"{t} WARNING: MAC {mac} now claims {sorted(mac_to_ips[mac])}")
    return table, alerts


if __name__ == "__main__":
    table, alerts = watch(EVENTS)
    print("Final ARP cache (what victims now believe):")
    for ip, mac in table.items():
        print(f"  {ip:<14} -> {mac}")
    print("\nAlerts:")
    for a in alerts:
        print(" ", a)
    print("\nDefences: Dynamic ARP Inspection + DHCP snooping on switches, "
          "static ARP for the gateway on critical hosts, encrypt traffic (TLS/VPN).")
