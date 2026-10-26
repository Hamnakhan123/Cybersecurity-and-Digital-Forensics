"""Session 6 - How a router picks a route: longest-prefix match, then
administrative distance, then metric.

Run:  python session-06_routing_table.py
"""
import ipaddress

# (prefix, next hop / interface, source, administrative distance, metric)
TABLE = [
    ("0.0.0.0/0",      "203.0.113.1 (ISP)",  "static", 1,   0),
    ("10.0.0.0/8",     "10.255.0.2",         "OSPF",   110, 30),
    ("10.1.0.0/16",    "10.255.0.6",         "OSPF",   110, 20),
    ("10.1.5.0/24",    "Gi0/1 (connected)",  "connected", 0, 0),
    ("10.1.5.0/24",    "10.255.0.9",         "RIP",    120, 2),
    ("172.16.0.0/12",  "10.255.0.2",         "EIGRP",  90,  28160),
    ("172.16.8.0/22",  "10.255.0.6",         "RIP",    120, 3),
]


def lookup(dst: str):
    ip = ipaddress.ip_address(dst)
    matches = [r for r in TABLE if ip in ipaddress.ip_network(r[0])]
    longest = max(ipaddress.ip_network(r[0]).prefixlen for r in matches)
    candidates = [r for r in matches if ipaddress.ip_network(r[0]).prefixlen == longest]
    best = min(candidates, key=lambda r: (r[3], r[4]))      # lower AD, then lower metric
    return best, matches


if __name__ == "__main__":
    print("Routing table:")
    for p, nh, src, ad, m in TABLE:
        print(f"  {p:<16} via {nh:<20} {src:<9} [AD {ad}/metric {m}]")
    for dst in ["10.1.5.20", "10.1.9.9", "10.200.1.1", "172.16.9.4", "172.20.1.1", "8.8.8.8"]:
        best, matches = lookup(dst)
        print(f"\n{dst}: {len(matches)} matching routes -> use {best[0]} via {best[1]} [{best[2]}]")
