"""Session 7 - Link-state routing (OSPF) simulated with Dijkstra's algorithm.

OSPF cost = reference bandwidth / interface bandwidth (default reference 100 Mbps,
so set it higher on modern networks or every link >= 100 Mbps costs 1).
Every router has the full map (LSDB) and computes the shortest-path tree itself.
Run:  python session-07_ospf_dijkstra.py
"""
import heapq

# router A, router B, link bandwidth in Mbps
LINKS = [("R1", "R2", 1000), ("R2", "R4", 1000), ("R1", "R3", 100),
         ("R3", "R4", 100), ("R1", "R4", 100), ("R4", "R5", 10000)]


def cost(bw_mbps, ref_mbps):
    return max(1, ref_mbps // bw_mbps)


def graph(ref):
    g = {}
    for a, b, bw in LINKS:
        c = cost(bw, ref)
        g.setdefault(a, []).append((b, c))
        g.setdefault(b, []).append((a, c))
    return g


def dijkstra(g, src):
    dist, prev = {src: 0}, {}
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in g[u]:
            if d + w < dist.get(v, float("inf")):
                dist[v], prev[v] = d + w, u
                heapq.heappush(pq, (d + w, v))
    return dist, prev


def path(prev, src, dst):
    p = [dst]
    while p[-1] != src:
        p.append(prev[p[-1]])
    return " -> ".join(reversed(p))


if __name__ == "__main__":
    for ref in (100, 100000):
        g = graph(ref)
        print(f"\nReference bandwidth {ref} Mbps; link costs:")
        for a, b, bw in LINKS:
            print(f"   {a}-{b} {bw:>6} Mbps cost {cost(bw, ref)}")
        dist, prev = dijkstra(g, "R1")
        print("   Shortest paths from R1:")
        for r in sorted(dist):
            if r != "R1":
                print(f"     to {r}: cost {dist[r]:>4}  path {path(prev, 'R1', r)}")
