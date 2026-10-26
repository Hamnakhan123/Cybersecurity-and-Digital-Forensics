"""Module 3 mini project - "Campus Branch Network Planner".

Given a branch office's departments and head-counts, the planner:
  1. allocates VLSM subnets from one private block (largest first, no overlap),
  2. assigns VLAN IDs and gateway addresses,
  3. estimates switch ports and PoE access points,
  4. writes an inter-VLAN ACL policy (guest isolated, servers protected),
  5. prints a documentation table (the deliverable a network admin hands over).
Run:  python mini_project_netplan.py
"""
import ipaddress
import math

BLOCK = ipaddress.ip_network("10.20.0.0/22")
DEPARTMENTS = [  # name, hosts needed today, growth %, wired?
    ("Staff",        110, 20, True),
    ("Students-Lab",  60, 10, True),
    ("Guest-WiFi",    90, 30, False),
    ("Servers",       12, 50, True),
    ("Management",     6, 50, True),
]
P2P_LINKS = 2          # router-to-firewall and router-to-ISP style links (/30)


def needed_prefix(hosts):
    """Smallest prefix with enough usable addresses (hosts + gateway)."""
    return 32 - math.ceil(math.log2(hosts + 1 + 2))


def allocate():
    plan, free = [], [BLOCK]
    reqs = []
    for name, h, growth, wired in DEPARTMENTS:
        future = math.ceil(h * (1 + growth / 100))
        reqs.append((name, h, future, wired))
    reqs.sort(key=lambda r: -r[2])                       # VLSM: biggest first
    reqs += [(f"P2P-{i + 1}", 2, 2, True) for i in range(P2P_LINKS)]
    for i, (name, h, future, wired) in enumerate(reqs):
        prefix = 30 if name.startswith("P2P") else needed_prefix(future)
        free.sort(key=lambda n: (n.network_address))
        for blk in free:
            if blk.prefixlen <= prefix:
                sub = next(blk.subnets(new_prefix=prefix))
                free.remove(blk)
                free += list(blk.address_exclude(sub))
                plan.append((name, h, future, wired, sub))
                break
        else:
            raise SystemExit(f"Block {BLOCK} is too small for {name}")
    return plan, free


if __name__ == "__main__":
    plan, free = allocate()
    print(f"Address block {BLOCK} ({BLOCK.num_addresses} addresses)\n")
    print(f"{'VLAN':<5}{'Segment':<14}{'need':>5}{'+grow':>6}  {'subnet':<17}{'gateway':<14}{'usable':>7}{'spare':>6}")
    vlan = 10
    for name, h, future, wired, sub in plan:
        usable = sub.num_addresses - 2
        gw = next(sub.hosts())
        vid = "-" if name.startswith("P2P") else str(vlan)
        print(f"{vid:<5}{name:<14}{h:>5}{future:>6}  {str(sub):<17}{str(gw):<14}{usable:>7}{usable - future - (0 if name.startswith('P2P') else 1):>6}")
        if not name.startswith("P2P"):
            vlan += 10
    used = sum(s.num_addresses for *_, s in plan)
    print(f"\nUsed {used}/{BLOCK.num_addresses} addresses ({used / BLOCK.num_addresses:.0%}); "
          f"free blocks: {', '.join(str(f) for f in sorted(free, key=lambda n: n.network_address))}")

    wired_hosts = sum(f for n, h, f, w, s in plan if w and not n.startswith("P2P"))
    ports = wired_hosts + 4                       # + uplinks/APs/printers margin
    switches = math.ceil(ports / 48)
    aps = math.ceil(sum(f for n, h, f, w, s in plan if not w) / 30)   # ~30 clients per AP
    print(f"\nHardware: {wired_hosts} wired devices -> {switches} x 48-port switches; "
          f"{aps} PoE access points for wireless clients")

    subnets = {n: s for n, *_, s in plan}
    print("\nInter-VLAN ACL policy (applied on the router, first match wins):")
    rules = [
        ("deny", "Guest-WiFi", "any internal", "guests reach the internet only"),
        ("permit", "Management", "any", "admins manage everything"),
        ("permit", "Staff", "Servers tcp 443,445", "staff use file and web apps"),
        ("permit", "Students-Lab", "Servers tcp 443", "lab uses the web portal only"),
        ("deny", "any", "Management", "nobody else touches device management"),
        ("permit", "any", "internet", "everything else may browse"),
    ]
    for i, (act, src, dst, why) in enumerate(rules, 1):
        s = subnets.get(src, src)
        print(f"  {i}. {act:<6} {src:<12} ({str(s):<15}) -> {dst:<22} # {why}")
