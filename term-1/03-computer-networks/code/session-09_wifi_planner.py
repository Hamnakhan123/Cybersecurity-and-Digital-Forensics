"""Session 9 - Wi-Fi planning maths: 2.4 GHz channel overlap, free-space path
loss and a simple link budget for an access point.

FSPL(dB) = 20 log10(d_km) + 20 log10(f_MHz) + 32.44
Received power = Tx power + Tx antenna gain + Rx antenna gain - FSPL - wall losses
Run:  python session-09_wifi_planner.py
"""
import math


def channel_centre_24(ch):           # 2.4 GHz channels are 5 MHz apart
    return 2407 + 5 * ch


def overlaps(c1, c2, width=22):        # classic 802.11b/g channel is 22 MHz wide
    return abs(channel_centre_24(c1) - channel_centre_24(c2)) < width


def fspl(d_m, f_mhz):
    return 20 * math.log10(d_m / 1000) + 20 * math.log10(f_mhz) + 32.44


def rssi(d_m, f_mhz, tx_dbm=20, gain_tx=3, gain_rx=0, walls=0, wall_db=5):
    return tx_dbm + gain_tx + gain_rx - fspl(d_m, f_mhz) - walls * wall_db


def quality(dbm):
    if dbm >= -60: return "excellent"
    if dbm >= -67: return "good (VoIP OK)"
    if dbm >= -75: return "fair (browsing)"
    return "poor"


if __name__ == "__main__":
    print("2.4 GHz channels that do NOT overlap with channel 1:",
          [c for c in range(1, 14) if not overlaps(1, c)][:3], "-> use 1, 6, 11")
    print("Channel 3 overlaps channel 1?", overlaps(1, 3), "| channel 6?", overlaps(1, 6))

    print("\nSignal at distance from a 20 dBm AP with a 3 dBi antenna:")
    print(f"{'distance':>8} {'walls':>5} {'2.4 GHz':>9} {'5 GHz':>9}  5 GHz quality")
    for d, w in [(5, 0), (15, 1), (25, 2), (40, 2), (60, 3)]:
        a, b = rssi(d, 2437, walls=w), rssi(d, 5500, walls=w)
        print(f"{d:>6} m {w:>5} {a:>7.1f}dBm {b:>7.1f}dBm  {quality(b)}")
    print("\n5 GHz loses about", round(fspl(10, 5500) - fspl(10, 2437), 1),
          "dB more than 2.4 GHz at the same distance (shorter range, more channels).")
