"""Session 10 - DHCP snooping: stop rogue DHCP servers and build the binding table.

Ports are UNTRUSTED by default. Server messages (OFFER, ACK) are allowed only
from TRUSTED ports (the uplink towards the real DHCP server). Every ACK that
passes creates a binding (MAC, IP, VLAN, port) that Dynamic ARP Inspection
and IP Source Guard later use to drop spoofed traffic. A rate limit on
untrusted ports slows DHCP starvation floods.
Run:  python session-10_dhcp_snooping.py
"""

TRUSTED = {"Gi0/1"}                 # uplink to the legitimate server
RATE_LIMIT = 10                     # packets per second allowed on untrusted ports


def snoop(events):
    bindings, log, counters = [], [], {}
    for t, port, msg, mac, ip in events:
        counters[(t, port)] = counters.get((t, port), 0) + 1
        if port not in TRUSTED and counters[(t, port)] > RATE_LIMIT:
            log.append(f"t={t} {port}: rate limit exceeded -> port err-disabled")
            continue
        if msg in ("OFFER", "ACK") and port not in TRUSTED:
            log.append(f"t={t} {port}: DROPPED {msg} from {mac} (server message on untrusted port)")
            continue
        log.append(f"t={t} {port}: forwarded {msg} {mac} {ip or ''}".rstrip())
        if msg == "ACK":
            bindings.append((mac, ip, 10, "Fa0/3"))      # client port learned from the DISCOVER
    return bindings, log


def dai_check(bindings, port, mac, ip):
    ok = any(b[0] == mac and b[1] == ip and b[3] == port for b in bindings)
    return "permit" if ok else "DROP (no matching binding)"


if __name__ == "__main__":
    events = [
        (0, "Fa0/3", "DISCOVER", "aaaa.0000.0003", None),
        (0, "Fa0/7", "OFFER", "dead.beef.0007", "10.99.99.50"),     # rogue server on a user port
        (0, "Gi0/1", "OFFER", "0011.2233.4455", "192.168.10.21"),
        (0, "Fa0/3", "REQUEST", "aaaa.0000.0003", "192.168.10.21"),
        (0, "Gi0/1", "ACK", "aaaa.0000.0003", "192.168.10.21"),
    ] + [(1, "Fa0/9", "DISCOVER", f"0bad.0000.{i:04x}", None) for i in range(15)]   # starvation flood
    bindings, log = snoop(events)
    seen = set()
    for line in log:
        if "0bad" in line and "forwarded" in line:
            if "flood" in seen: continue
            seen.add("flood"); line += "   (... more DISCOVERs with random MACs)"
        if "rate limit" in line and "rl" in seen: continue
        if "rate limit" in line: seen.add("rl")
        print(line)
    print("\nshow ip dhcp snooping binding")
    print("MacAddress       IpAddress        Lease  Type           VLAN  Interface")
    for mac, ip_, vlan, port in bindings:
        print(f"{mac:16} {ip_:16} 86400  dhcp-snooping  {vlan:<5} {port}")
    print("\nDynamic ARP Inspection uses the table:")
    print("  ARP from Fa0/3 aaaa.0000.0003 claims 192.168.10.21 ->", dai_check(bindings, "Fa0/3", "aaaa.0000.0003", "192.168.10.21"))
    print("  ARP from Fa0/7 dead.beef.0007 claims 192.168.10.1  ->", dai_check(bindings, "Fa0/7", "dead.beef.0007", "192.168.10.1"))
