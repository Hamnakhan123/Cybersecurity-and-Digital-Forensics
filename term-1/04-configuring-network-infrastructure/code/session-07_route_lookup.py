"""Session 7 - How a router chooses a route: longest prefix, then AD, then metric.

1. Among routes that CONTAIN the destination, the longest prefix (most specific) wins.
2. If two sources offer the same prefix, the lower administrative distance is installed.
3. A floating static route has a deliberately high AD, so it is used only when
   the preferred dynamic route disappears.
Run:  python session-07_route_lookup.py
"""
import ipaddress

AD = {"connected": 0, "static": 1, "eBGP": 20, "EIGRP": 90, "OSPF": 110, "RIP": 120, "floating static": 130}

# candidate routes learned from different sources: (prefix, source, metric, next hop, AD override)
CANDIDATES = [
    ("10.0.0.0/8", "static", 0, "203.0.113.1", None),
    ("10.10.0.0/16", "OSPF", 20, "10.0.12.2", None),
    ("10.10.0.0/16", "RIP", 3, "10.0.13.2", None),
    ("10.10.5.0/24", "OSPF", 30, "10.0.14.2", None),
    ("0.0.0.0/0", "static", 0, "203.0.113.1", None),
    ("192.168.50.0/24", "OSPF", 65, "10.0.12.2", None),
    ("192.168.50.0/24", "floating static", 0, "10.0.99.2", 130),
]


def build_rib(candidates):
    """Install only the best source for each prefix (lowest AD, then lowest metric)."""
    rib = {}
    for prefix, src, metric, nh, ad in candidates:
        ad = ad if ad is not None else AD[src]
        cur = rib.get(prefix)
        if cur is None or (ad, metric) < (cur[1], cur[2]):
            rib[prefix] = (src, ad, metric, nh)
    return rib


def lookup(rib, dst):
    d = ipaddress.ip_address(dst)
    matches = [(ipaddress.ip_network(p), r) for p, r in rib.items() if d in ipaddress.ip_network(p)]
    net, (src, ad, metric, nh) = max(matches, key=lambda m: m[0].prefixlen)
    return net, src, ad, metric, nh


def show(rib):
    code = {"static": "S", "floating static": "S", "OSPF": "O", "RIP": "R", "connected": "C"}
    for p in sorted(rib, key=lambda x: (ipaddress.ip_network(x).prefixlen, x)):
        src, ad, m, nh = rib[p]
        print(f"   {code[src]:2} {p:18} [{ad}/{m}] via {nh}")


if __name__ == "__main__":
    rib = build_rib(CANDIDATES)
    print("Routing table (RIB) after choosing the best source per prefix:")
    show(rib)
    print("\nLookups:")
    for dst in ["10.10.5.9", "10.10.7.1", "10.200.1.1", "8.8.8.8", "192.168.50.20"]:
        net, src, ad, m, nh = lookup(rib, dst)
        print(f"   {dst:15} -> {str(net):16} via {nh:12} ({src}, AD {ad})")

    print("\nOSPF neighbour to 10.0.12.2 goes down: OSPF routes via it are withdrawn")
    remaining = [c for c in CANDIDATES if not (c[1] == "OSPF" and c[3] == "10.0.12.2")]
    rib2 = build_rib(remaining)
    for dst in ["10.10.7.1", "192.168.50.20"]:
        net, src, ad, m, nh = lookup(rib2, dst)
        print(f"   {dst:15} -> {str(net):16} via {nh:12} ({src}, AD {ad})")
