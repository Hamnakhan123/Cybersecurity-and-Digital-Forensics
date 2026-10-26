"""Session 6 - Spanning Tree Protocol: root bridge, root ports and blocked ports.

Bridge ID = priority (default 32768 + VLAN number) followed by the MAC address.
1. Lowest Bridge ID becomes ROOT; all its ports are designated (forwarding).
2. Every other switch picks one ROOT PORT: lowest cost to the root, then
   lowest sender Bridge ID, then lowest sender port ID.
3. On each segment, the switch with the lowest cost to root owns the
   DESIGNATED port. Every port that is neither root nor designated BLOCKS.
Port costs (short method): 10 Mbps 100, 100 Mbps 19, 1 Gbps 4, 10 Gbps 2.
Run:  python session-06_stp_election.py
"""
import heapq

COST = {10: 100, 100: 19, 1000: 4, 10000: 2}


def bid(sw):
    return (sw["priority"], sw["mac"])


def run_stp(switches, links):
    root = min(switches, key=lambda s: bid(switches[s]))
    # Dijkstra on path cost, ties broken by sender bridge ID then port name
    best = {root: (0, (), "")}          # switch -> (cost, sender_bid, local_port)
    pq = [(0, bid(switches[root]), root)]
    adj = {}
    for a, pa, b, pb, speed in links:
        adj.setdefault(a, []).append((b, pa, pb, COST[speed]))
        adj.setdefault(b, []).append((a, pb, pa, COST[speed]))
    done = set()
    while pq:
        c, _, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        for v, port_u, port_v, w in adj[u]:
            cand = (c + w, bid(switches[u]), port_v)
            if v not in best or cand < best[v]:
                best[v] = cand
                heapq.heappush(pq, (c + w, bid(switches[u]), v))
    roles = {}
    for a, pa, b, pb, speed in links:
        for sw, port in ((a, pa), (b, pb)):
            if sw != root and best[sw][2] == port:
                roles[(sw, port)] = "ROOT port       FWD"
        # designated port: side with lower root cost, then lower bridge ID
        side_a = (best[a][0], bid(switches[a])); side_b = (best[b][0], bid(switches[b]))
        des, dport, other, oport = (a, pa, b, pb) if side_a < side_b else (b, pb, a, pa)
        roles[(des, dport)] = "DESIGNATED port FWD"
        roles.setdefault((other, oport), "ALTERNATE port  BLOCKED")
    return root, best, roles


if __name__ == "__main__":
    switches = {"SW1": {"priority": 32769, "mac": "0011.1111.1111"},
                "SW2": {"priority": 32769, "mac": "0011.2222.2222"},
                "SW3": {"priority": 32769, "mac": "0011.0000.3333"}}
    links = [("SW1", "Gi0/1", "SW2", "Gi0/1", 1000),
             ("SW1", "Gi0/2", "SW3", "Gi0/1", 1000),
             ("SW2", "Gi0/2", "SW3", "Gi0/2", 1000)]
    for label in ("Default priorities (the oldest MAC wins - often a poor choice)",
                  "After 'spanning-tree vlan 1 root primary' on SW1 (priority 24577)"):
        root, best, roles = run_stp(switches, links)
        print(label)
        print(f"  Root bridge: {root}  (priority {switches[root]['priority']}, MAC {switches[root]['mac']})")
        for sw in sorted(switches):
            print(f"  {sw}: cost to root {best[sw][0]}")
            for (s, p), r in sorted(roles.items()):
                if s == sw:
                    print(f"     {p:6} {r}")
        print()
        switches["SW1"]["priority"] = 24577
