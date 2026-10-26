"""Module 4 mini project - Campus network builder: from intent to device configs.

Input: what the campus needs (departments, host counts, which ones are guests).
Output, all generated and checked automatically:
  1. A VLSM address plan with VLAN IDs, gateways and DHCP ranges.
  2. Two distribution switches (DIST-1, DIST-2) with SVIs and HSRP, where the
     HSRP Active router and the STP root are the SAME switch for each VLAN
     (odd VLANs on DIST-1, even VLANs on DIST-2) so load is shared.
  3. DHCP pools, a guest-isolation ACL, and DHCP snooping/edge-port settings.
  4. A pre-deployment audit (overlaps, gateway inside subnet, sizing headroom).
Run:  python mini_project_campus_builder.py
"""
import ipaddress
import math

CAMPUS_BLOCK = "10.60.0.0/21"
DNS = None                # set by plan(): 4th address of the SERVERS subnet
INTENT = [  # name, expected hosts, guest network?
    ("LECTURERS", 120, False),
    ("STUDENT-LAB", 300, False),
    ("ADMIN", 40, False),
    ("GUEST-WIFI", 200, True),
    ("PRINTERS-IOT", 20, False),
    ("SERVERS", 12, False),
]
GROWTH = 1.25            # leave 25% room for growth


def plan(block, intent):
    free = [ipaddress.ip_network(block)]
    rows = []
    for i, (name, hosts, guest) in enumerate(sorted(intent, key=lambda x: -x[1])):
        need = math.ceil(hosts * GROWTH) + 3          # + gateway, DIST-1, DIST-2
        prefix = 32 - math.ceil(math.log2(need + 2))
        cand = sorted((f for f in free if f.prefixlen <= prefix), key=lambda n: int(n.network_address))
        if not cand:
            raise SystemExit(f"Address block too small for {name}")
        parent = cand[0]
        net = next(parent.subnets(new_prefix=prefix))
        free.remove(parent); free.extend(parent.address_exclude(net))
        rows.append({"name": name, "hosts": hosts, "guest": guest, "net": net})
    for vid, r in zip(range(10, 10 * (len(rows) + 1), 10), sorted(rows, key=lambda r: int(r["net"].network_address))):
        r["vlan"] = vid
        h = list(r["net"].hosts())
        r["vip"], r["d1"], r["d2"] = h[0], h[1], h[2]
        r["dhcp_from"], r["dhcp_to"] = h[3], h[-1]
        if r["name"] == "SERVERS":                    # first 10 server addresses stay static (DNS = first)
            global DNS
            DNS = h[3]
            r["dhcp_from"] = h[13]
    return sorted(rows, key=lambda r: r["vlan"]), sorted(free, key=lambda n: int(n.network_address))


def dist_config(rows, me):
    out = [f"hostname DIST-{me}", "ip routing", "spanning-tree mode rapid-pvst"]
    mine = [r["vlan"] for r in rows if (r["vlan"] // 10) % 2 == (1 if me == 1 else 0)]
    other = [r["vlan"] for r in rows if r["vlan"] not in mine]
    out.append(f"spanning-tree vlan {','.join(map(str, mine))} root primary")
    out.append(f"spanning-tree vlan {','.join(map(str, other))} root secondary")
    for r in rows:
        active = r["vlan"] in mine
        out += [f"vlan {r['vlan']}", f" name {r['name']}",
                f"interface Vlan{r['vlan']}",
                f" ip address {r['d1'] if me == 1 else r['d2']} {r['net'].netmask}",
                " standby version 2",
                f" standby {r['vlan']} ip {r['vip']}",
                f" standby {r['vlan']} priority {110 if active else 100}",
                f" standby {r['vlan']} preempt"]
        if r["guest"]:
            out.append(" ip access-group GUEST-IN in")
        out.append(" no shutdown")
    return out


def services(rows):
    out = []
    for r in rows:
        out += [f"ip dhcp excluded-address {r['net'].network_address + 1} {r['dhcp_from'] - 1}",
                f"ip dhcp pool {r['name']}", f" network {r['net'].network_address} {r['net'].netmask}",
                f" default-router {r['vip']}", f" dns-server {DNS}"]
    internal = [r for r in rows if not r["guest"]]
    guest = next(r for r in rows if r["guest"])
    gw = guest["net"].hostmask
    out += ["ip access-list extended GUEST-IN",
            f" permit udp {guest['net'].network_address} {gw} host {DNS} eq 53"]
    out += [f" deny ip {guest['net'].network_address} {gw} {r['net'].network_address} {r['net'].hostmask}" for r in internal]
    out += [f" permit ip {guest['net'].network_address} {gw} any",
            "! access switches", f"ip dhcp snooping vlan {','.join(str(r['vlan']) for r in rows)}",
            "interface range Gi1/0/1 - 46", " switchport mode access", " switchport nonegotiate",
            " spanning-tree portfast", " spanning-tree bpduguard enable", " ip dhcp snooping limit rate 15",
            "interface range Gi1/0/47 - 48", " ip dhcp snooping trust"]
    return out


def audit(rows):
    issues = []
    nets = [r["net"] for r in rows]
    for i, a in enumerate(nets):
        issues += [f"overlap {a} {b}" for b in nets[i + 1:] if a.overlaps(b)]
    for r in rows:
        if r["vip"] not in r["net"]:
            issues.append(f"{r['name']}: gateway outside subnet")
        usable = r["net"].num_addresses - 2 - 3
        if usable < r["hosts"] * GROWTH:
            issues.append(f"{r['name']}: not enough room for growth")
    return issues


if __name__ == "__main__":
    rows, free = plan(CAMPUS_BLOCK, INTENT)
    print(f"Campus block {CAMPUS_BLOCK}  (growth allowance {int((GROWTH - 1) * 100)}%)\n")
    print(f"{'VLAN':>4}  {'Name':13} {'Hosts':>5}  {'Subnet':16} {'Gateway (VIP)':14} {'DHCP range':29} Active")
    for r in rows:
        act = "DIST-1" if (r["vlan"] // 10) % 2 == 1 else "DIST-2"
        print(f"{r['vlan']:>4}  {r['name']:13} {r['hosts']:>5}  {str(r['net']):16} {str(r['vip']):14} "
              f"{str(r['dhcp_from']) + ' - ' + str(r['dhcp_to']):29} {act}")
    print("Spare space:", ", ".join(map(str, free)) or "none")
    print("\nAudit:", audit(rows) or "PASS - no overlaps, gateways valid, growth room OK")
    d1 = dist_config(rows, 1)
    print(f"\nDIST-1 configuration ({len(d1)} lines), first VLAN shown:")
    print("\n".join("  " + l for l in d1[:13]))
    svc = services(rows)
    print(f"\nShared services ({len(svc)} lines), guest ACL shown:")
    start = svc.index("ip access-list extended GUEST-IN")
    print("\n".join("  " + l for l in svc[start:start + 8]))
