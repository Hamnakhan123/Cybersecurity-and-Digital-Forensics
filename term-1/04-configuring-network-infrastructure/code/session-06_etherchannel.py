"""Session 6 - EtherChannel: which modes form a bundle, and how traffic is shared.

PAgP (Cisco):  desirable + desirable/auto form a channel; auto + auto does not.
LACP (802.3ad): active + active/passive form a channel; passive + passive does not.
'on' forms only with 'on' (no negotiation at all).
Traffic is NOT split packet by packet: a hash of addresses chooses one member
link per flow, so a single flow never goes faster than one link.
Run:  python session-06_etherchannel.py
"""
import hashlib
from collections import Counter

FORMS = {
    ("desirable", "desirable"): "PAgP channel", ("desirable", "auto"): "PAgP channel",
    ("auto", "auto"): "no channel (both wait)",
    ("active", "active"): "LACP channel", ("active", "passive"): "LACP channel",
    ("passive", "passive"): "no channel (both wait)",
    ("on", "on"): "static channel",
}


def negotiate(a, b):
    return FORMS.get((a, b)) or FORMS.get((b, a)) or "no channel (modes do not match)"


def member_for(src_ip, dst_ip, links=4):
    """Simplified src-dst-ip hash: same pair of addresses -> same physical link."""
    h = hashlib.sha256(f"{src_ip}-{dst_ip}".encode()).digest()[0]
    return h % links


if __name__ == "__main__":
    print("Mode compatibility")
    for a, b in [("desirable", "auto"), ("auto", "auto"), ("active", "passive"),
                 ("passive", "passive"), ("on", "active"), ("on", "on")]:
        print(f"  {a:9} + {b:9} -> {negotiate(a, b)}")

    print("\nLoad sharing over a 4 x 1 Gbps Port-channel (src-dst-ip hash)")
    flows = [(f"10.1.10.{h}", "10.1.99.10") for h in range(1, 41)]
    use = Counter(member_for(s, d) for s, d in flows)
    for link in range(4):
        print(f"  Gi1/0/{link+1}: {use[link]:2} flows  " + "#" * use[link])
    print("  One backup flow 10.1.10.7 -> 10.1.99.10 always uses Gi1/0/"
          f"{member_for('10.1.10.7', '10.1.99.10') + 1} (max 1 Gbps for that flow)")
    print("\nBundled bandwidth seen by STP: 4 Gbps as ONE logical port, so no port blocks.")
