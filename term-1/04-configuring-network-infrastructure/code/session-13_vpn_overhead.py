"""Session 13 - VPN tunnels cost bytes: overhead, MTU and TCP MSS.

Every tunnel wraps the original packet in new headers. If the result is
bigger than the link MTU (1500 on Ethernet) it must be fragmented or dropped,
which is the classic "VPN is up but some websites hang" problem. The fix is
to lower the tunnel MTU and clamp the TCP MSS. Header sizes below are typical
values for the listed options.
Run:  python session-13_vpn_overhead.py
"""

TUNNELS = {
    # name: list of (header, bytes)
    "GRE over IPv4": [("new IPv4 header", 20), ("GRE header", 4)],
    "IPsec ESP tunnel, AES-CBC + SHA-256": [("new IPv4 header", 20), ("ESP header (SPI+seq)", 8),
                                            ("IV", 16), ("padding (worst case)", 15),
                                            ("pad length + next header", 2), ("ICV (integrity tag)", 16)],
    "IPsec ESP tunnel, AES-GCM": [("new IPv4 header", 20), ("ESP header", 8), ("IV", 8),
                                  ("padding (worst case)", 3), ("pad length + next header", 2),
                                  ("ICV", 16)],
    "GRE inside IPsec (transport mode), AES-GCM": [("IPv4 header", 20), ("ESP header", 8), ("IV", 8),
                                                   ("padding", 3), ("pad length + next header", 2),
                                                   ("ICV", 16), ("GRE", 4)],
    "IPsec NAT-T (UDP 4500), AES-GCM": [("new IPv4 header", 20), ("UDP header", 8), ("ESP header", 8),
                                        ("IV", 8), ("padding", 3), ("pad length + next header", 2),
                                        ("ICV", 16)],
}

if __name__ == "__main__":
    LINK_MTU = 1500
    print(f"Link MTU {LINK_MTU} bytes. Inner TCP/IPv4 headers = 40 bytes.\n")
    print(f"{'Tunnel type':45} {'Overhead':>8} {'Tunnel MTU':>11} {'TCP MSS':>8}")
    for name, hdrs in TUNNELS.items():
        ovh = sum(b for _, b in hdrs)
        mtu = LINK_MTU - ovh
        print(f"{name:45} {ovh:>7}B {mtu:>10}B {mtu - 40:>7}B")
    print("\nWhat happens to a full-size 1500-byte packet in an AES-GCM ESP tunnel:")
    size = 1500 + sum(b for _, b in TUNNELS["IPsec ESP tunnel, AES-GCM"])
    print(f"  encrypted size {size} B > {LINK_MTU} B -> fragmented (slow) or dropped if DF bit is set")
    print("  Fix on the tunnel interface:  ip mtu 1400   and   ip tcp adjust-mss 1360")
    print("\nEfficiency for small VoIP packets (60 bytes) vs large file packets (1400 bytes):")
    for payload in (60, 1400):
        ovh = sum(b for _, b in TUNNELS["IPsec ESP tunnel, AES-GCM"])
        print(f"  {payload:>5} B payload: {payload / (payload + ovh) * 100:5.1f}% of the bytes on the wire are useful")
