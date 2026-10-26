"""Session 8 - First Hop Redundancy: HSRP election, failover and GLBP load sharing.

Hosts keep ONE default gateway address. HSRP/VRRP/GLBP make two or more
routers share a VIRTUAL IP and virtual MAC so the gateway survives a failure.
HSRP: highest priority (default 100) becomes Active, ties -> highest interface IP.
Preemption lets a higher-priority router take the role back when it returns.
Run:  python session-08_fhrp_sim.py
"""
import ipaddress


def hsrp_vmac(group, version=1):
    return f"0000.0c07.ac{group:02x}" if version == 1 else f"0000.0c9f.f{group:03x}"


def vrrp_vmac(group):
    return f"0000.5e00.01{group:02x}"


def elect(routers):
    alive = [r for r in routers if r["up"]]
    ranked = sorted(alive, key=lambda r: (r["priority"], ipaddress.ip_address(r["ip"])), reverse=True)
    return ranked[0]["name"] if ranked else None, ranked[1]["name"] if len(ranked) > 1 else None


def timeline(routers, preempt):
    active, standby = elect(routers)
    print(f"  t=0s   Active {active}, Standby {standby}")
    routers[0]["up"] = False
    active, standby = elect(routers)
    print(f"  t=5s   {routers[0]['name']} fails -> hello timer 3 s, hold timer 10 s")
    print(f"  t=15s  hold timer expires: Active {active}, Standby {standby}")
    routers[0]["up"] = True
    if preempt:
        a, s = elect(routers)
        print(f"  t=60s  {routers[0]['name']} returns with preempt -> Active {a}, Standby {s}")
    else:
        print(f"  t=60s  {routers[0]['name']} returns without preempt -> stays Standby; Active {active}")


def glbp_assign(hosts, forwarders):
    """The AVG answers each host's ARP with the next forwarder's virtual MAC (round robin)."""
    return {h: forwarders[i % len(forwarders)] for i, h in enumerate(hosts)}


if __name__ == "__main__":
    print("Virtual MAC addresses (group 10)")
    print(f"  HSRPv1 {hsrp_vmac(10)}   HSRPv2 {hsrp_vmac(10, 2)}   VRRP {vrrp_vmac(10)}")
    print("\nHSRP group 10, virtual IP 192.168.10.1")
    for preempt in (False, True):
        routers = [{"name": "R1", "ip": "192.168.10.2", "priority": 110, "up": True},
                   {"name": "R2", "ip": "192.168.10.3", "priority": 100, "up": True}]
        print(f" preempt {'ON' if preempt else 'OFF'}:")
        timeline(routers, preempt)
    print("\nInterface tracking: R1 priority 110, uplink fails, track decrement 20 -> 90 < R2 100")
    r = [{"name": "R1", "ip": "192.168.10.2", "priority": 90, "up": True},
         {"name": "R2", "ip": "192.168.10.3", "priority": 100, "up": True}]
    print(f"  with preempt on R2, Active becomes {elect(r)[0]} (traffic avoids the dead uplink)")

    print("\nGLBP: one virtual IP, several virtual MACs -> every router forwards")
    hosts = [f"PC{i}" for i in range(1, 9)]
    avf = {"R1": "0007.b400.0a01", "R2": "0007.b400.0a02", "R3": "0007.b400.0a03"}
    plan = glbp_assign(hosts, list(avf))
    for h, r in plan.items():
        print(f"  {h}: gateway 192.168.10.1 -> MAC {avf[r]} ({r})")
