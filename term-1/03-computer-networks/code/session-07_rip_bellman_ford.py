"""Session 7 - Distance-vector routing (RIP) simulated with Bellman-Ford.

Each router only knows its neighbours. Every round, each router sends its
whole table to its neighbours and keeps any route that is shorter (hop count).
RIP: metric = hops, maximum 15, 16 = unreachable.
Run:  python session-07_rip_bellman_ford.py
"""

LINKS = {("R1", "R2"), ("R2", "R3"), ("R3", "R4"), ("R1", "R5"), ("R5", "R4")}
NETWORKS = {"R1": "10.1.0.0/24", "R2": "10.2.0.0/24", "R3": "10.3.0.0/24",
            "R4": "10.4.0.0/24", "R5": "10.5.0.0/24"}
INFINITY = 16


def neighbours(r, links):
    return [b if a == r else a for a, b in links if r in (a, b)]


def converge(links, tables=None, label=""):
    routers = sorted(NETWORKS)
    if tables is None:   # start: each router knows only its own network, 0 hops
        tables = {r: {NETWORKS[r]: (0, "connected")} for r in routers}
    for rnd in range(1, 20):
        changed = False
        snapshot = {r: dict(t) for r, t in tables.items()}      # updates sent at the same time
        for r in routers:
            for n in neighbours(r, links):
                for net, (hops, _) in snapshot[n].items():
                    new = min(hops + 1, INFINITY)
                    cur = tables[r].get(net, (INFINITY, None))
                    if new < cur[0] or (cur[1] == n and new != cur[0]):
                        tables[r][net] = (new, n)
                        changed = True
        if not changed:
            print(f"{label}converged after {rnd - 1} update round(s)")
            return tables
    return tables


def show(tables, router):
    for net, (hops, via) in sorted(tables[router].items()):
        state = "unreachable" if hops >= INFINITY else f"{hops} hop(s) via {via}"
        print(f"   {router}: {net:<13} {state}")


if __name__ == "__main__":
    t = converge(LINKS, label="Initial topology: ")
    show(t, "R1")
    print("\nLink R1-R5 fails. R1 forgets routes learned through R5, then reconverges:")
    t["R1"] = {n: v for n, v in t["R1"].items() if v[1] != "R5"}
    t["R5"] = {n: v for n, v in t["R5"].items() if v[1] != "R1"}
    t = converge(LINKS - {("R1", "R5")}, t, label="After failure: ")
    show(t, "R1")
