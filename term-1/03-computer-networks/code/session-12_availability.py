"""Session 12 - High-availability maths: MTBF/MTTR, components in series
versus in parallel (redundancy), and RPO/RTO for backup strategies.

A = MTBF / (MTBF + MTTR)
Series   (all must work):      A = A1 * A2 * ...
Parallel (one is enough):      A = 1 - (1 - A1) * (1 - A2) * ...
Run:  python session-12_availability.py
"""
from functools import reduce


def avail(mtbf_h, mttr_h): return mtbf_h / (mtbf_h + mttr_h)
def series(*a): return reduce(lambda x, y: x * y, a)
def parallel(*a): return 1 - reduce(lambda x, y: x * y, [1 - v for v in a])
def downtime_min(a): return (1 - a) * 365 * 24 * 60


if __name__ == "__main__":
    router = avail(50_000, 4)
    switch = avail(80_000, 4)
    isp = avail(2_000, 6)
    power = avail(10_000, 2)
    print(f"Single router {router:.5f}, switch {switch:.5f}, ISP link {isp:.5f}, power {power:.5f}")

    single = series(power, isp, router, switch)
    redundant = series(parallel(power, power), parallel(isp, isp), parallel(router, router), parallel(switch, switch))
    for name, a in [("No redundancy", single), ("Everything doubled", redundant)]:
        print(f"{name:<20} A = {a:.6f}  -> {downtime_min(a):>8.1f} min down per year")

    print("\nBackup strategies for a file server changing 50 GB/day (full = 2 TB):")
    plans = [  # name, data loss window (RPO h), restore time (RTO h), weekly storage GB
        ("Weekly full only",                168, 6,  2000),
        ("Weekly full + daily incremental", 24,  9,  2000 + 6 * 50),
        ("Weekly full + daily differential", 24, 7,  2000 + sum(50 * d for d in range(1, 7))),
        ("Hourly snapshots + offsite copy", 1,   1,  2000 + 7 * 24 * 2),
    ]
    print(f"{'plan':<34}{'RPO':>6}{'RTO':>6}{'storage/week':>14}")
    for name, rpo, rto, gb in plans:
        print(f"{name:<34}{rpo:>5}h{rto:>5}h{gb:>11,} GB")
    print("\nRestore chain on Friday: incremental -> full + Mon..Fri (6 sets); differential -> full + Fri (2 sets)")
