"""Session 5 - Storage and cloud maths: RAID usable capacity, SAN vs NAS vs DAS,
and a simple on-premises vs public-cloud cost comparison over 3 years.

All prices are made-up teaching numbers, not quotes from any provider.
Run:  python session-05_storage_cloud.py
"""


def raid_usable(level: str, disks: int, size_tb: float) -> tuple[float, str]:
    if level == "RAID 0":
        return disks * size_tb, "no failures tolerated"
    if level == "RAID 1":
        return size_tb, f"{disks - 1} disk(s) may fail (mirror)"
    if level == "RAID 5":
        return (disks - 1) * size_tb, "1 disk may fail (parity)"
    if level == "RAID 6":
        return (disks - 2) * size_tb, "2 disks may fail (double parity)"
    if level == "RAID 10":
        return disks / 2 * size_tb, "1 disk per mirror pair may fail"
    raise ValueError(level)


def three_year_cost(tb: float):
    # on-premises: buy hardware once + power/admin each month
    onprem = 18000 + 36 * (250 + 400)
    # cloud: pay per TB-month + a compute instance, no upfront cost
    cloud = 36 * (tb * 23 + 700)
    return onprem, cloud


if __name__ == "__main__":
    print("8 x 4 TB disks:")
    for lvl in ["RAID 0", "RAID 1", "RAID 5", "RAID 6", "RAID 10"]:
        disks = 2 if lvl == "RAID 1" else 8
        usable, tol = raid_usable(lvl, disks, 4)
        raw = disks * 4
        print(f"  {lvl:<8} disks={disks}  usable {usable:>5.1f} TB of {raw:>2} TB "
              f"({usable / raw:>4.0%})  {tol}")

    print("\nOn-prem vs cloud for a small analytics system (teaching numbers, USD):")
    for tb in (5, 20, 60):
        on, cl = three_year_cost(tb)
        cheaper = "cloud" if cl < on else "on-prem"
        print(f"  {tb:>3} TB: on-prem ${on:>7,}  cloud ${cl:>9,.0f}  -> {cheaper} is cheaper")
