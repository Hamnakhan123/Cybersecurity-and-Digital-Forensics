"""Session 1 - The 72-hour breach clock and the two tiers of GDPR fines.

Part A: a controller must notify the supervisory authority "without undue delay and,
where feasible, not later than 72 hours after having become aware" of a personal-data
breach (Article 33), unless the breach is unlikely to result in a risk to people.
High-risk breaches must ALSO be communicated to the affected people (Article 34).
Times are handled with real time zones, because the lead authority may be in a
different country from the team that finds the breach.

Part B: fines (Article 83) have two ceilings, whichever is HIGHER:
  lower tier: EUR 10 million or 2% of worldwide annual turnover of the previous year
  upper tier: EUR 20 million or 4% of worldwide annual turnover of the previous year
The ceiling is a maximum, not a price list: authorities weigh many factors.
Run:  python session-01_breach_and_fines.py
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

KHI, DUB = ZoneInfo("Asia/Karachi"), ZoneInfo("Europe/Dublin")


def breach_plan(name, aware_local, records, risk):
    deadline = aware_local + timedelta(hours=72)
    print(f"\n{name}")
    print(f"  Became aware : {aware_local:%a %d %b %Y %H:%M} Karachi")
    if risk == "none":
        print("  Risk to people unlikely -> record it in the internal breach register; no notification")
        return
    print(f"  Notify DPA by: {deadline:%a %d %b %Y %H:%M} Karachi  = "
          f"{deadline.astimezone(DUB):%a %d %b %H:%M} Dublin time")
    if risk == "high":
        print(f"  High risk to {records:,} people -> ALSO tell the affected people without undue delay")


def fine_ceiling(turnover_eur, tier):
    fixed, pct = (10_000_000, 0.02) if tier == "lower" else (20_000_000, 0.04)
    return max(fixed, pct * turnover_eur)


def main():
    print("PART A - Breach notification clock")
    breach_plan("Case 1: laptop with encrypted disk stolen (key not stolen)",
                datetime(2026, 10, 23, 16, 30, tzinfo=KHI), 4_000, "none")
    breach_plan("Case 2: misconfigured cloud bucket exposed order history",
                datetime(2026, 10, 23, 16, 30, tzinfo=KHI), 12_500, "medium")
    breach_plan("Case 3: ransomware encrypted and leaked passport scans",
                datetime(2026, 10, 30, 22, 0, tzinfo=KHI), 48_000, "high")

    print("\nPART B - Maximum fine (whichever is higher)")
    print(f"  {'Company':<26}{'Turnover (EUR)':>18}{'Lower tier max':>18}{'Upper tier max':>18}")
    for name, t in [("Small online shop", 2_000_000), ("Regional bank", 900_000_000),
                    ("Global platform", 120_000_000_000)]:
        lo, hi = fine_ceiling(t, "lower"), fine_ceiling(t, "upper")
        print(f"  {name:<26}{t:>18,.0f}{lo:>18,.0f}{hi:>18,.0f}")
    print("\n  Break-even: 4% beats the EUR 20m floor when turnover > EUR "
          f"{20_000_000 / 0.04:,.0f}")


if __name__ == "__main__":
    main()
