"""Session 5 - How a Layer 2 switch learns, floods, forwards and filters, per VLAN.

The switch keeps one MAC address table. Each entry is (VLAN, MAC) -> port.
- Learn: record the SOURCE MAC of every frame against the port it arrived on.
- Forward: if the DESTINATION is known in that VLAN, send it out that one port.
- Filter: if the destination is on the same port it came from, drop it.
- Flood: unknown unicast and broadcast go out every other port IN THE SAME VLAN.
Run:  python session-05_switch_sim.py
"""

PORTS = {"Fa0/1": 10, "Fa0/2": 10, "Fa0/3": 20, "Fa0/4": 20, "Fa0/5": 10}   # access ports
HOSTS = {"PC-A": ("aaaa.aaaa.0001", "Fa0/1"), "PC-B": ("bbbb.bbbb.0002", "Fa0/2"),
         "PC-C": ("cccc.cccc.0003", "Fa0/3"), "PC-D": ("dddd.dddd.0004", "Fa0/4"),
         "PRN-E": ("eeee.eeee.0005", "Fa0/5")}
BROADCAST = "ffff.ffff.ffff"


class Switch:
    def __init__(self, ports):
        self.ports = ports
        self.table = {}

    def receive(self, in_port, src, dst):
        vlan = self.ports[in_port]
        learned = (vlan, src) not in self.table
        self.table[(vlan, src)] = in_port
        if dst == BROADCAST or (vlan, dst) not in self.table:
            out = [p for p, v in self.ports.items() if v == vlan and p != in_port]
            action = "FLOOD" if dst != BROADCAST else "BROADCAST"
        elif self.table[(vlan, dst)] == in_port:
            out, action = [], "FILTER"
        else:
            out, action = [self.table[(vlan, dst)]], "FORWARD"
        return vlan, learned, action, out

    def show_mac_table(self):
        print("          Mac Address Table")
        print("Vlan    Mac Address       Type        Ports")
        print("----    -----------       --------    -----")
        for (vlan, mac), port in sorted(self.table.items()):
            print(f"{vlan:<7} {mac:17} DYNAMIC     {port}")


if __name__ == "__main__":
    sw = Switch(PORTS)
    events = [("PC-A", "PC-B"), ("PC-B", "PC-A"), ("PC-C", "BCAST"), ("PC-A", "PRN-E"),
              ("PRN-E", "PC-A"), ("PC-A", "PC-C"), ("PC-D", "PC-C")]
    for s, d in events:
        smac, sport = HOSTS[s]
        dmac = BROADCAST if d == "BCAST" else HOSTS[d][0]
        vlan, learned, action, out = sw.receive(sport, smac, dmac)
        note = " (learned new MAC)" if learned else ""
        print(f"{s:5} -> {d:5} in {sport} VLAN {vlan}: {action:9} out {', '.join(out) or '-'}{note}")
    print()
    sw.show_mac_table()
    print("\nPC-A -> PC-C never reaches VLAN 20: VLANs are separate broadcast domains.")
    print("They need a router or Layer 3 switch (Session 12) to talk.")
