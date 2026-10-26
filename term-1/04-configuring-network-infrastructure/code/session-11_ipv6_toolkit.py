"""Session 11 - IPv6 toolkit: notation, address types, SLAAC and NDP multicast.

- Expand and compress addresses (one "::" per address, leading zeros dropped).
- Classify global unicast, unique local, link-local, multicast and loopback.
- Build a SLAAC address from a /64 prefix + modified EUI-64 interface ID.
- Work out the solicited-node multicast address that NDP uses instead of ARP.
- Compare IPv4 and IPv6 address space.
Run:  python session-11_ipv6_toolkit.py
"""
import ipaddress


def kind(a):
    a = ipaddress.IPv6Address(a)
    if a.is_loopback: return "loopback ::1"
    if a.is_link_local: return "link-local fe80::/10 (never routed)"
    if a.is_multicast:
        names = {"ff02::1": "all nodes", "ff02::2": "all routers", "ff02::5": "all OSPFv3 routers",
                 "ff02::1:2": "all DHCPv6 agents"}
        return f"multicast ff00::/8 ({names.get(str(a), 'group')})"
    if a in ipaddress.IPv6Network("fc00::/7"): return "unique local fc00::/7 (private)"
    if a in ipaddress.IPv6Network("2001:db8::/32"): return "documentation 2001:db8::/32"
    if a in ipaddress.IPv6Network("2000::/3"): return "global unicast 2000::/3"
    return "other / reserved"


def eui64_id(mac):
    b = bytearray(int(x, 16) for x in mac.replace(".", ":").replace("-", ":").split(":"))
    b[0] ^= 0x02
    return bytes(b[:3]) + b"\xff\xfe" + bytes(b[3:])


def slaac(prefix, mac):
    net = ipaddress.IPv6Network(prefix)
    assert net.prefixlen == 64, "SLAAC needs a /64"
    return ipaddress.IPv6Address(int(net.network_address) | int.from_bytes(eui64_id(mac), "big"))


def solicited_node(addr):
    last24 = int(ipaddress.IPv6Address(addr)) & 0xFFFFFF
    return ipaddress.IPv6Address(int(ipaddress.IPv6Address("ff02::1:ff00:0")) | last24)


if __name__ == "__main__":
    print("Expand / compress")
    for a in ["2001:0db8:0000:0000:0000:ff00:0042:8329", "fe80::1", "2001:db8:0:0:1:0:0:1"]:
        x = ipaddress.IPv6Address(a)
        print(f"  {a:42} full {x.exploded}\n  {'':42} short {x.compressed}")
    print("\nAddress types")
    for a in ["2001:db8:acad:10::1", "2400:cb00::1", "fd12:3456:789a:1::10", "fe80::21a:2bff:fe3c:4d5e",
              "ff02::1", "ff02::2", "ff02::5", "::1"]:
        print(f"  {a:28} {kind(a)}")
    print("\nSLAAC: router advertises 2001:db8:acad:10::/64, host MAC 00:1a:2b:3c:4d:5e")
    g = slaac("2001:db8:acad:10::/64", "00:1a:2b:3c:4d:5e")
    ll = slaac("fe80::/64", "00:1a:2b:3c:4d:5e")
    print(f"  global address     {g}\n  link-local address {ll}")
    print(f"  solicited-node multicast for NDP: {solicited_node(g)}")
    print("  (NS goes to that group instead of a broadcast; only hosts with the same last 24 bits listen)")
    print("\nAddress space")
    print(f"  IPv4: 2^32  = {2**32:,}")
    print(f"  IPv6: 2^128 = {2**128:,}")
    print(f"  One /64 subnet holds 2^64 = {2**64:,} interface IDs")
    site = ipaddress.IPv6Network("2001:db8:acad::/48")
    subs = list(site.subnets(new_prefix=64))[:3]
    print(f"  A /48 site has {2**16:,} /64 subnets, e.g. {', '.join(map(str, subs))} ...")
