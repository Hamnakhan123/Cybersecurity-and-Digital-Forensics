"""Session 12 - Inter-VLAN routing on a Layer 3 switch, and how CEF forwards fast.

A host sends to another subnet by framing the packet to its GATEWAY's MAC
(the SVI of its VLAN). The multilayer switch looks the destination up in its
FIB (forwarding information base, built from the routing table) and takes the
new Layer 2 header from the ADJACENCY table (built from ARP), then rewrites
the frame: new source/destination MAC, TTL - 1, and sends it into the other VLAN.
Run:  python session-12_intervlan_cef.py
"""
import ipaddress

SVIS = {10: ("192.168.10.1", 24, "0011.5c00.0010"),
        20: ("192.168.20.1", 24, "0011.5c00.0010"),
        30: ("192.168.30.1", 24, "0011.5c00.0010")}
ARP = {"192.168.10.11": ("aaaa.0000.0011", 10, "Gi1/0/1"),
       "192.168.20.22": ("bbbb.0000.0022", 20, "Gi1/0/5"),
       "192.168.30.10": ("cccc.0000.0010", 30, "Gi1/0/24")}


def build_fib():
    fib = []
    for vlan, (ip, plen, _) in SVIS.items():
        fib.append((ipaddress.ip_network(f"{ip}/{plen}", strict=False), f"Vlan{vlan}", "attached"))
    fib.append((ipaddress.ip_network("0.0.0.0/0"), "Gi1/0/48", "10.0.0.1"))
    return fib


def adjacency():
    return {ip: {"vlan": v, "port": p, "rewrite": mac} for ip, (mac, v, p) in ARP.items()}


def forward(src_ip, src_mac, dst_ip, ttl=64):
    src_vlan = next(v for v, (gw, plen, _) in SVIS.items()
                    if ipaddress.ip_address(src_ip) in ipaddress.ip_network(f"{gw}/{plen}", strict=False))
    gw_ip, _, gw_mac = SVIS[src_vlan]
    same = ipaddress.ip_address(dst_ip) in ipaddress.ip_network(f"{gw_ip}/24", strict=False)
    print(f"{src_ip} -> {dst_ip}")
    if same:
        print("  same VLAN: switched at Layer 2, no routing needed")
        return
    print(f"  host frames packet to its gateway: dst MAC {gw_mac} (SVI Vlan{src_vlan} {gw_ip})")
    fib = build_fib()
    prefix, iface, nh = max((e for e in fib if ipaddress.ip_address(dst_ip) in e[0]),
                            key=lambda e: e[0].prefixlen)
    print(f"  FIB lookup: {prefix} via {iface} ({nh})")
    adj = adjacency().get(dst_ip)
    if adj:
        print(f"  adjacency : rewrite dst MAC {adj['rewrite']}, src MAC {gw_mac}, VLAN {adj['vlan']}, out {adj['port']}")
        print(f"  TTL {ttl} -> {ttl - 1}; forwarded in hardware, CPU not involved")
    else:
        print("  no adjacency yet -> packet punted to CPU, switch ARPs for the next hop (glean)")


if __name__ == "__main__":
    print("FIB (show ip cef):")
    for p, i, nh in build_fib():
        print(f"  {str(p):18} {nh:10} {i}")
    print("\nAdjacency table (show adjacency detail):")
    for ip, a in adjacency().items():
        print(f"  {ip:15} Vlan{a['vlan']:<3} {a['port']:9} rewrite to {a['rewrite']}")
    print()
    forward("192.168.10.11", "aaaa.0000.0011", "192.168.20.22")
    forward("192.168.10.11", "aaaa.0000.0011", "192.168.30.10")
    forward("192.168.10.11", "aaaa.0000.0011", "192.168.10.40")
    forward("192.168.20.22", "bbbb.0000.0022", "192.168.30.99")
    print("\nCompare: router-on-a-stick = every inter-VLAN packet crosses ONE trunk twice;")
    print("a Layer 3 switch routes between SVIs internally at line rate.")
