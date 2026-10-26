"""Session 10 - Evaluate Cisco-style ACLs exactly as a router does.

- Lines are checked top-down; the FIRST match decides (permit or deny).
- Every ACL ends with an invisible "deny any" (implicit deny).
- Wildcard masks: 0 bit = must match, 1 bit = ignore. "host x" = x 0.0.0.0, "any" = 0.0.0.0 255.255.255.255.
- Standard ACLs (1-99) check only the source; extended ACLs (100-199) check
  protocol, source, destination and port.
Run:  python session-10_acl_engine.py
"""
import ipaddress


def ip(x): return int(ipaddress.ip_address(x))


def match_addr(addr, base, wildcard):
    return (ip(addr) & ~ip(wildcard) & 0xFFFFFFFF) == (ip(base) & ~ip(wildcard) & 0xFFFFFFFF)


def parse_addr(tokens):
    """Consume 'any' | 'host A' | 'A W' and return ((base, wildcard), remaining tokens)."""
    if tokens[0] == "any":
        return ("0.0.0.0", "255.255.255.255"), tokens[1:]
    if tokens[0] == "host":
        return (tokens[1], "0.0.0.0"), tokens[2:]
    return (tokens[0], tokens[1]), tokens[2:]


def parse_line(line):
    t = line.split()
    action, rest = t[0], t[1:]
    proto = None
    if rest[0] in ("ip", "tcp", "udp", "icmp"):
        proto, rest = rest[0], rest[1:]
    src, rest = parse_addr(rest)
    dst, port = None, None
    if proto:
        dst, rest = parse_addr(rest)
        if rest[:1] == ["eq"]:
            port = int(rest[1])
    return {"text": line, "action": action, "proto": proto, "src": src, "dst": dst, "port": port}


def evaluate(acl, pkt):
    for n, rule in enumerate(acl, 1):
        if rule["proto"] not in (None, "ip") and rule["proto"] != pkt["proto"]:
            continue
        if not match_addr(pkt["src"], *rule["src"]):
            continue
        if rule["dst"] and not match_addr(pkt["dst"], *rule["dst"]):
            continue
        if rule["port"] is not None and rule["port"] != pkt.get("port"):
            continue
        return rule["action"].upper(), f"line {n}: {rule['text']}"
    return "DENY", "implicit deny any (end of list)"


STANDARD_10 = ["permit 192.168.99.0 0.0.0.255", "deny any"]            # VTY: only the management VLAN
EXTENDED_110 = [
    "permit tcp 192.168.20.0 0.0.0.255 host 192.168.30.10 eq 443",     # students -> LMS over HTTPS
    "permit udp 192.168.20.0 0.0.0.255 host 192.168.30.53 eq 53",      # students -> DNS
    "deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255",            # students -/-> lecturers VLAN
    "permit icmp 192.168.20.0 0.0.0.255 any",                           # ping for troubleshooting
    "permit tcp 192.168.20.0 0.0.0.255 any eq 443",                     # web browsing
]

if __name__ == "__main__":
    std = [parse_line(x) for x in STANDARD_10]
    print("Standard ACL 10 applied to 'line vty 0 4' (who may SSH to the switch):")
    for src in ["192.168.99.25", "192.168.20.14"]:
        print(f"  SSH from {src:15} -> {evaluate(std, {'src': src})}")

    ext = [parse_line(x) for x in EXTENDED_110]
    print("\nExtended ACL 110 inbound on the STUDENTS VLAN interface:")
    tests = [
        {"proto": "tcp", "src": "192.168.20.14", "dst": "192.168.30.10", "port": 443},
        {"proto": "tcp", "src": "192.168.20.14", "dst": "192.168.30.10", "port": 22},
        {"proto": "udp", "src": "192.168.20.14", "dst": "192.168.30.53", "port": 53},
        {"proto": "tcp", "src": "192.168.20.14", "dst": "192.168.10.50", "port": 445},
        {"proto": "icmp", "src": "192.168.20.14", "dst": "8.8.8.8"},
        {"proto": "tcp", "src": "192.168.20.14", "dst": "142.250.1.1", "port": 443},
        {"proto": "tcp", "src": "192.168.20.14", "dst": "142.250.1.1", "port": 80},
    ]
    for p in tests:
        verdict, why = evaluate(ext, p)
        desc = f"{p['proto']} {p['src']} -> {p['dst']}" + (f":{p['port']}" if 'port' in p else "")
        print(f"  {desc:42} {verdict:6} ({why})")
    print("\nWildcard check: 10.1.0.0 0.0.255.255 matches 10.1.200.7?",
          match_addr("10.1.200.7", "10.1.0.0", "0.0.255.255"))
