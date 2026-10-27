"""Session 4 - User Behaviour Analytics: spotting unusual logins and enforcing policy.

An AI-driven security tool does not start with a list of "bad" events. It first LEARNS
what is normal for each user (a baseline), then scores how far a new event is from that
normal, and finally applies the organisation's POLICY to the score. This script shows
the three steps with plain statistics, so every alert can be explained:

  1. Baseline  - per user: usual login hours (mean and spread), cities, devices, data volume.
  2. Score     - add points for each unusual feature; keep the reason for each point.
  3. Enforce   - the policy turns the score into ALLOW, STEP-UP MFA or BLOCK + ALERT.

All users, cities and devices are fictional (Clifton Institute of Technology, Karachi).
Run:  python session-04_login_anomaly.py
"""
import random
from statistics import mean, pstdev

rng = random.Random(42)  # fixed seed: the same "history" every run

# ---------- 1. Fictional 30-day login history -> baseline ----------
PROFILES = {  # user: (usual hour, hour spread, cities, devices, usual MB downloaded)
    "sana.faculty":  (9, 1.0, ["Karachi"], ["LAPTOP-SANA"], 40),
    "omer.registrar": (10, 1.5, ["Karachi"], ["PC-REG-02"], 25),
    "bilal.student": (21, 2.0, ["Karachi", "Hyderabad"], ["PHONE-BILAL", "LAB-WS-14"], 60),
}

history = []
for user, (hour, spread, cities, devices, mb) in PROFILES.items():
    for day in range(30):
        h = max(0, min(23, round(rng.gauss(hour, spread))))
        history.append({"user": user, "hour": h, "city": rng.choice(cities),
                        "device": rng.choice(devices), "mb": max(1, round(rng.gauss(mb, mb * 0.25)))})


def baseline(user):
    rows = [r for r in history if r["user"] == user]
    hours, mbs = [r["hour"] for r in rows], [r["mb"] for r in rows]
    return {"h_mean": mean(hours), "h_sd": max(pstdev(hours), 0.5),
            "mb_mean": mean(mbs), "mb_sd": max(pstdev(mbs), 1.0),
            "cities": {r["city"] for r in rows}, "devices": {r["device"] for r in rows}}


BASE = {u: baseline(u) for u in PROFILES}

# ---------- 2. Score new events (explainable points) ----------
POLICY = {"step_up_at": 30, "block_at": 60}   # thresholds set by the security policy


def score(event):
    b, pts, why = BASE[event["user"]], 0, []
    z_hour = abs(event["hour"] - b["h_mean"]) / b["h_sd"]
    if z_hour > 3:
        pts += 25; why.append(f"login hour {event['hour']:02d}:00 is {z_hour:.1f} SD from usual")
    if event["city"] not in b["cities"]:
        pts += 30; why.append(f"new location {event['city']}")
    if event["device"] not in b["devices"]:
        pts += 20; why.append(f"unknown device {event['device']}")
    z_mb = (event["mb"] - b["mb_mean"]) / b["mb_sd"]
    if z_mb > 3:
        pts += 25; why.append(f"downloaded {event['mb']} MB ({z_mb:.1f} SD above usual)")
    if event.get("failed_before", 0) >= 5:
        pts += 15; why.append(f"{event['failed_before']} failed attempts just before")
    return min(pts, 100), why


def enforce(pts):
    if pts >= POLICY["block_at"]:
        return "BLOCK + ALERT SOC"
    if pts >= POLICY["step_up_at"]:
        return "STEP-UP MFA"
    return "ALLOW"


NEW_EVENTS = [
    {"id": "E1", "user": "sana.faculty", "hour": 9, "city": "Karachi", "device": "LAPTOP-SANA", "mb": 45},
    {"id": "E2", "user": "omer.registrar", "hour": 23, "city": "Karachi", "device": "PC-REG-02", "mb": 30},
    {"id": "E3", "user": "bilal.student", "hour": 22, "city": "Lahore", "device": "PHONE-BILAL", "mb": 70},
    {"id": "E4", "user": "omer.registrar", "hour": 3, "city": "Frankfurt", "device": "UNKNOWN-VM",
     "mb": 900, "failed_before": 7},
    {"id": "E5", "user": "sana.faculty", "hour": 14, "city": "Karachi", "device": "TABLET-NEW", "mb": 38},
]

print("[1] Learned baselines (30 days of fictional history)")
for u, b in BASE.items():
    print(f"  {u:<15} usual hour {b['h_mean']:4.1f} +/- {b['h_sd']:.1f} | "
          f"~{b['mb_mean']:.0f} MB | cities {sorted(b['cities'])}")

print(f"\n[2] Scoring new logins (policy: step-up at {POLICY['step_up_at']}, block at {POLICY['block_at']})")
counts = {}
for e in NEW_EVENTS:
    pts, why = score(e)
    action = enforce(pts)
    counts[action] = counts.get(action, 0) + 1
    print(f"  {e['id']} {e['user']:<15} score {pts:3d} -> {action}")
    for w in why:
        print(f"       - {w}")

print("\n[3] Decision summary:", ", ".join(f"{k}: {v}" for k, v in counts.items()))
print("Note: a human analyst reviews every BLOCK; the score only recommends.")
