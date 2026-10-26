"""Session 1 - Compare network topologies by cable count and fault tolerance.

For each topology we build the list of links between N devices, then ask:
  * how many cables / links are needed?
  * if any ONE device fails, do the remaining devices stay connected?
That second question finds the single points of failure (SPOF).
Run:  python session-01_topology.py
"""
from itertools import combinations


def build(topology: str, n: int) -> set[tuple[int, int]]:
    """Return the set of links (a, b) for n devices numbered 0..n-1."""
    if topology == "star":            # device 0 is the central switch
        return {(0, i) for i in range(1, n)}
    if topology == "ring":
        return {tuple(sorted((i, (i + 1) % n))) for i in range(n)}
    if topology == "full mesh":
        return set(combinations(range(n), 2))
    if topology == "bus":             # model the shared cable as node 0 (backbone)
        return {(0, i) for i in range(1, n)}
    if topology == "tree":            # binary tree: parent of i is (i-1)//2
        return {((i - 1) // 2, i) for i in range(1, n)}
    raise ValueError(topology)


def connected(nodes: set[int], links: set[tuple[int, int]]) -> bool:
    """Breadth-first search: can every node reach every other node?"""
    if not nodes:
        return True
    start = next(iter(nodes))
    seen, queue = {start}, [start]
    while queue:
        cur = queue.pop(0)
        for a, b in links:
            for x, y in ((a, b), (b, a)):
                if x == cur and y in nodes and y not in seen:
                    seen.add(y)
                    queue.append(y)
    return seen == nodes


def single_points_of_failure(n: int, links) -> list[int]:
    """Nodes whose failure splits the rest of the network."""
    spof = []
    for victim in range(n):
        rest = set(range(n)) - {victim}
        rest_links = {l for l in links if victim not in l}
        if not connected(rest, rest_links):
            spof.append(victim)
    return spof


if __name__ == "__main__":
    N = 6
    print(f"{'Topology':<10} {'Links':>5}  {'Formula':<12} Single points of failure")
    formulas = {"star": "n-1", "ring": "n", "full mesh": "n(n-1)/2",
                "bus": "1 backbone", "tree": "n-1"}
    for topo in ["bus", "star", "ring", "tree", "full mesh"]:
        links = build(topo, N)
        spof = single_points_of_failure(N, links)
        label = "none" if not spof else ", ".join(f"node {s}" for s in spof)
        print(f"{topo:<10} {len(links):>5}  {formulas[topo]:<12} {label}")

    print("\nFull-mesh cost grows fast:")
    for n in (4, 10, 50, 100):
        print(f"  {n:>3} sites -> {n * (n - 1) // 2:>5} links")
