"""Session 1 - Measure what makes a network "good": delay, throughput and availability.

A file transfer is slowed by four delays: transmission (pushing bits onto the
wire), propagation (the signal travelling), processing and queuing.
This script calculates them for real link types so you can compare designs.
Run:  python session-01_delay_calc.py
"""

SPEED_OF_LIGHT_FIBRE = 2e8      # metres per second (about 2/3 of c in glass or copper)


def transmission_delay(size_bytes, bandwidth_bps):
    """Seconds needed to put every bit of the message onto the link."""
    return size_bytes * 8 / bandwidth_bps


def propagation_delay(distance_m, speed=SPEED_OF_LIGHT_FIBRE):
    """Seconds the first bit needs to travel the distance."""
    return distance_m / speed


def total_delay(size_bytes, bandwidth_bps, distance_m, processing_s=0.0001, queuing_s=0.0):
    t = transmission_delay(size_bytes, bandwidth_bps)
    p = propagation_delay(distance_m)
    return t, p, t + p + processing_s + queuing_s


def availability(mtbf_h, mttr_h):
    """Fraction of time a component works: MTBF / (MTBF + MTTR)."""
    return mtbf_h / (mtbf_h + mttr_h)


def downtime_per_year(avail):
    return (1 - avail) * 365 * 24 * 60   # minutes


if __name__ == "__main__":
    FILE = 50 * 1024 * 1024   # a 50 MB lecture video
    links = [
        ("Office LAN, Fast Ethernet, 50 m", 100e6, 50),
        ("Office LAN, Gigabit, 50 m", 1e9, 50),
        ("Campus fibre, 10 Gbps, 2 km", 10e9, 2_000),
        ("Karachi -> Lahore WAN, 100 Mbps, 1 200 km", 100e6, 1_200_000),
        ("Karachi -> London WAN, 100 Mbps, 6 300 km", 100e6, 6_300_000),
    ]
    print("Sending a 50 MB file over different links")
    print(f"{'Link':45} {'Transmit':>10} {'Propagate':>11} {'Total':>9}")
    for name, bw, dist in links:
        t, p, tot = total_delay(FILE, bw, dist)
        print(f"{name:45} {t:9.3f}s {p*1000:9.3f}ms {tot:8.3f}s")

    print("\nA small 1 500-byte packet (one Ethernet frame) on the same links")
    for name, bw, dist in links:
        t, p, tot = total_delay(1500, bw, dist)
        print(f"{name:45} transmit {t*1e6:8.1f} us   propagate {p*1000:7.3f} ms")

    print("\nReliability: availability and yearly downtime")
    for name, mtbf, mttr in [("Single access switch", 50_000, 8),
                             ("Consumer router", 10_000, 24),
                             ("Core switch with 4 h support", 200_000, 4)]:
        a = availability(mtbf, mttr)
        print(f"{name:32} A = {a*100:.4f}%   downtime = {downtime_per_year(a):7.1f} min/year")
    # two switches in parallel: down only if both are down
    a = availability(50_000, 8)
    pair = 1 - (1 - a) ** 2
    print(f"{'Two access switches in parallel':32} A = {pair*100:.6f}%   downtime = {downtime_per_year(pair)*60:7.3f} s/year")
