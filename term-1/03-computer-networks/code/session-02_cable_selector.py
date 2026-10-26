"""Session 2 - Choose a cable type for a link from distance, speed and environment.

The table holds typical *standard* limits (not vendor marketing maximums).
Run:  python session-02_cable_selector.py
"""

# name, max metres, max Gbps, immune to EMI?, relative cost (1 = cheapest)
CABLES = [
    ("Cat5e UTP",              100,   1, False, 1),
    ("Cat6 UTP",               100,  10, False, 2),   # 10G only up to ~55 m
    ("Cat6a STP",              100,  10, False, 3),
    ("Cat8 STP",                30,  40, False, 5),
    ("Multimode fibre OM3",    300,  10, True,  4),
    ("Multimode fibre OM4",    400,  10, True,  5),
    ("Single-mode fibre OS2", 10000, 100, True,  6),
]


def choose(distance_m: float, speed_gbps: float, high_emi: bool) -> list[str]:
    """Return suitable cables, cheapest first, with a reason for each rejection."""
    ok = []
    for name, max_m, max_g, emi_immune, cost in CABLES:
        limit_m = max_m
        if name == "Cat6 UTP" and speed_gbps > 1:
            limit_m = 55                                  # Cat6 at 10G
        if distance_m > limit_m or speed_gbps > max_g:
            continue
        if high_emi and not emi_immune and "STP" not in name:
            continue                                      # unshielded copper near motors = errors
        ok.append((cost, name))
    return [n for _, n in sorted(ok)]


if __name__ == "__main__":
    jobs = [
        ("Office desk to wall jack", 40, 1, False),
        ("Server rack to rack, 10G", 25, 10, False),
        ("Floor 1 to floor 5 riser, 10G", 180, 10, False),
        ("Factory floor next to motors", 70, 1, True),
        ("Campus building A to B", 2200, 10, False),
        ("Desk to switch 140 m away", 140, 1, False),
    ]
    for desc, d, s, emi in jobs:
        picks = choose(d, s, emi)
        best = picks[0] if picks else "NO single cable: add a switch or use fibre"
        print(f"{desc:<32} {d:>5} m {s:>3} Gbps EMI={'yes' if emi else 'no ':<3} -> {best}")
