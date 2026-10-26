"""Session 6 - Why switches replaced hubs: simulate MAC-address learning.

A hub repeats every frame out of every port. A switch learns which MAC lives on
which port from the SOURCE address of each frame, then forwards only to the
right port (flooding only while it does not know the destination yet).
Run:  python session-06_switch_vs_hub.py
"""

BROADCAST = "ff:ff:ff:ff:ff:ff"


class Hub:
    def __init__(self, ports): self.ports = ports
    def receive(self, in_port, src, dst):
        return [p for p in range(1, self.ports + 1) if p != in_port]


class Switch:
    def __init__(self, ports):
        self.ports = ports
        self.cam = {}                       # MAC address table: mac -> port

    def receive(self, in_port, src, dst):
        self.cam[src] = in_port             # 1. learn from the source address
        if dst != BROADCAST and dst in self.cam:
            out = self.cam[dst]             # 2. known unicast -> one port
            return [] if out == in_port else [out]
        return [p for p in range(1, self.ports + 1) if p != in_port]   # 3. flood


if __name__ == "__main__":
    pcs = {"A": ("aa:00:00:00:00:0a", 1), "B": ("aa:00:00:00:00:0b", 2),
           "C": ("aa:00:00:00:00:0c", 3), "D": ("aa:00:00:00:00:0d", 4)}
    traffic = [("A", "B"), ("B", "A"), ("C", "A"), ("A", "C"), ("D", "BCAST"), ("A", "B")]
    for dev in (Hub(4), Switch(4)):
        total = 0
        print(f"\n{type(dev).__name__}:")
        for s, d in traffic:
            src, port = pcs[s]
            dst = BROADCAST if d == "BCAST" else pcs[d][0]
            outs = dev.receive(port, src, dst)
            total += len(outs)
            print(f"  {s} -> {d:<5} in port {port}  sent out ports {outs}")
        print(f"  frames copied onto cables: {total}")
        if isinstance(dev, Switch):
            print("  learned MAC table:", {m[-2:]: p for m, p in dev.cam.items()})
