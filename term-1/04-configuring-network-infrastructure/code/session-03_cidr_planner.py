"""Session 3 - Subnetting, VLSM and CIDR summarisation with the ipaddress module.

1. Fixed-length subnetting: split a /24 into equal subnets.
2. VLSM: give each department the smallest subnet that fits, largest first.
3. CIDR: summarise contiguous routes into one supernet (route aggregation).
Run:  python session-03_cidr_planner.py
"""
import ipaddress
import math


def fixed_subnets(block, count):
    net = ipaddress.ip_network(block)
    extra_bits = math.ceil(math.log2(count))
    return list(net.subnets(prefixlen_diff=extra_bits))


def prefix_for(hosts):
    """Smallest prefix whose usable hosts (2^h - 2) fit the requirement."""
    h = math.ceil(math.log2(hosts + 2))
    return 32 - h


def vlsm(block, needs):
    """Allocate largest requirement first from the lowest free block that fits."""
    free = [ipaddress.ip_network(block)]
    plan = []
    for name, hosts in sorted(needs, key=lambda x: -x[1]):
        p = prefix_for(hosts)
        candidates = sorted((f for f in free if f.prefixlen <= p), key=lambda n: int(n.network_address))
        if not candidates:
            raise ValueError(f"no space left for {name}")
        block_ = candidates[0]
        chosen = next(block_.subnets(new_prefix=p))          # first subnet of that size
        free.remove(block_)
        free.extend(block_.address_exclude(chosen))          # give the rest back
        plan.append((name, hosts, chosen))
    return plan, sorted(free, key=lambda n: int(n.network_address))


if __name__ == "__main__":
    print("1) 192.168.50.0/24 split into 6 equal subnets (needs 3 borrowed bits -> 8 subnets)")
    for s in fixed_subnets("192.168.50.0/24", 6):
        h = list(s.hosts())
        print(f"   {str(s):18} hosts {h[0]} - {h[-1]}  broadcast {s.broadcast_address}  ({len(h)} usable)")

    print("\n2) VLSM plan for 172.16.0.0/22")
    needs = [("Lecturers", 200), ("Students lab", 400), ("Admin office", 50),
             ("Printers", 10), ("R1-R2 link", 2), ("R1-R3 link", 2)]
    plan, free = vlsm("172.16.0.0/22", needs)
    print(f"   {'Segment':14} {'Need':>5}  {'Subnet':18} {'Mask':16} {'Usable':>6}  Gateway")
    for name, hosts, net in plan:
        print(f"   {name:14} {hosts:>5}  {str(net):18} {str(net.netmask):16} {net.num_addresses - 2:>6}  {net.network_address + 1}")
    print("   Unused blocks:", ", ".join(map(str, free)))

    print("\n3) CIDR summarisation (what a router can advertise as one route)")
    routes = [ipaddress.ip_network(f"10.20.{i}.0/24") for i in range(8, 16)]
    print("   Branch routes:", ", ".join(str(r) for r in routes[:3]), "...", routes[-1])
    print("   Summary      :", ", ".join(str(n) for n in ipaddress.collapse_addresses(routes)))
    odd = [ipaddress.ip_network(n) for n in ("10.20.8.0/24", "10.20.9.0/24", "10.20.11.0/24")]
    print("   Non-contiguous", [str(n) for n in odd], "->", [str(n) for n in ipaddress.collapse_addresses(odd)])
    print("   Classful view of 172.16.0.0/22: a class B /16 would waste",
          65_534 - 1_022, "addresses compared with CIDR /22")
