"""Session 13 - A first-match packet-filter (ACL / firewall rule) evaluator.

Rules are checked top-down; the first rule that matches decides. If nothing
matches, the implicit "deny any" at the end applies (as on Cisco ACLs).
Run:  python session-13_firewall_acl.py
"""
import ipaddress

RULES = [  # action, protocol, source, destination, destination port (None = any), note
    ("permit", "tcp", "any",          "10.1.5.20/32", 443,  "public web server HTTPS"),
    ("permit", "tcp", "any",          "10.1.5.20/32", 80,   "HTTP (redirects to HTTPS)"),
    ("permit", "tcp", "10.1.9.0/24",  "10.1.5.0/24",  22,   "admin subnet SSH"),
    ("deny",   "tcp", "any",          "any",          3389, "no RDP from anywhere"),
    ("permit", "udp", "10.1.0.0/16",  "10.1.0.53/32", 53,   "internal DNS"),
    ("permit", "icmp", "10.1.0.0/16", "any",          None, "internal ping"),
]


def match(net, ip):
    return net == "any" or ipaddress.ip_address(ip) in ipaddress.ip_network(net)


def evaluate(proto, src, dst, port):
    for i, (act, p, s, d, dp, note) in enumerate(RULES, 1):
        if p == proto and match(s, src) and match(d, dst) and (dp is None or dp == port):
            return act.upper(), f"rule {i}: {note}"
    return "DENY", "implicit deny (no rule matched)"


if __name__ == "__main__":
    packets = [
        ("tcp", "198.51.100.7", "10.1.5.20", 443),
        ("tcp", "198.51.100.7", "10.1.5.20", 22),
        ("tcp", "10.1.9.15",    "10.1.5.20", 22),
        ("tcp", "10.1.9.15",    "10.1.5.30", 3389),
        ("udp", "10.1.7.7",     "10.1.0.53", 53),
        ("udp", "198.51.100.7", "10.1.0.53", 53),
        ("icmp", "10.1.7.7",    "8.8.8.8",   None),
        ("tcp", "10.1.7.7",     "10.1.5.20", 8080),
    ]
    for proto, s, d, p in packets:
        verdict, why = evaluate(proto, s, d, p)
        print(f"{proto:<4} {s:>14} -> {d:<10}:{str(p or '-'):<5} {verdict:<7} {why}")
