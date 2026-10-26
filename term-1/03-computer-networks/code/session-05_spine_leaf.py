"""Session 5 - Size a data-centre network: three-tier vs spine-leaf.

Computes link counts, hop counts between servers and the oversubscription
ratio (server-facing bandwidth : uplink bandwidth) on each leaf switch.
Run:  python session-05_spine_leaf.py
"""


def spine_leaf(spines, leaves, servers_per_leaf, server_gbps, uplink_gbps):
    links = spines * leaves                      # every leaf connects to every spine
    down = servers_per_leaf * server_gbps        # traffic the servers can push into a leaf
    up = spines * uplink_gbps                    # capacity from that leaf to the fabric
    return {
        "servers": leaves * servers_per_leaf,
        "fabric_links": links,
        "max_hops": "leaf -> spine -> leaf (always 2 switch hops)",
        "oversub": down / up,
    }


def three_tier(core, aggregation, access, servers_per_access):
    # access -> 2 aggregation, aggregation -> every core
    links = access * 2 + aggregation * core
    return {"servers": access * servers_per_access, "links": links,
            "max_hops": "access -> agg -> core -> agg -> access (up to 4 switch hops)"}


if __name__ == "__main__":
    print("Spine-leaf designs (servers at 25 Gbps, uplinks at 100 Gbps):")
    print(f"{'spines':>6} {'leaves':>6} {'servers':>8} {'links':>6} {'oversub':>8}  verdict")
    for spines, leaves, per_leaf in [(2, 8, 48), (4, 8, 48), (4, 16, 32), (6, 20, 24)]:
        r = spine_leaf(spines, leaves, per_leaf, 25, 100)
        ratio = r["oversub"]
        verdict = "non-blocking" if ratio <= 1 else "ok for most apps" if ratio <= 3 else "too oversubscribed"
        print(f"{spines:>6} {leaves:>6} {r['servers']:>8} {r['fabric_links']:>6} {ratio:>7.1f}:1  {verdict}")
    print("\nPath length:", spine_leaf(4, 8, 48, 25, 100)["max_hops"])

    t = three_tier(core=2, aggregation=4, access=16, servers_per_access=24)
    print(f"\nThree-tier: {t['servers']} servers, {t['links']} uplinks, {t['max_hops']}")
    print("Add capacity: spine-leaf -> add a spine (all leaves gain bandwidth); "
          "three-tier -> bigger core boxes")
