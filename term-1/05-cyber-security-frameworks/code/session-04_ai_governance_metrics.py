"""Session 4 - Governing an AI security model: accuracy, fairness and drift.

A security policy that relies on AI must say how the AI itself is checked. This script
plays the role of the monthly "model review" for a fictional login-anomaly model at
Clifton Institute of Technology (Karachi) and reports against written thresholds:

  1. Accuracy  - accuracy, precision, recall and false-positive rate (FPR)
  2. Fairness  - do two user groups (staff, students) get the same treatment?
                 FPR gap and flag-rate ratio (the "four-fifths" or 80% rule of thumb)
  3. Drift     - has the data changed since training? Population Stability Index (PSI)
                 plus the weekly accuracy trend
  4. Scorecard - PASS / FAIL against the AI governance policy, with actions

All numbers are fictional and chosen for teaching.
Run:  python session-04_ai_governance_metrics.py
"""
import math

# ---------- Fictional evaluation set: 200 labelled login events ----------
# Built from confusion counts so the result is fully reproducible.
COUNTS = {  # group: (TP, FN, FP, TN)   positive = "malicious login"
    "staff":   (18, 2, 3, 77),
    "student": (17, 3, 12, 68),
}
records = []  # (group, actual, predicted)
for g, (tp, fn, fp, tn) in COUNTS.items():
    records += [(g, 1, 1)] * tp + [(g, 1, 0)] * fn + [(g, 0, 1)] * fp + [(g, 0, 0)] * tn


def metrics(rows):
    tp = sum(1 for _, a, p in rows if a == 1 and p == 1)
    fn = sum(1 for _, a, p in rows if a == 1 and p == 0)
    fp = sum(1 for _, a, p in rows if a == 0 and p == 1)
    tn = sum(1 for _, a, p in rows if a == 0 and p == 0)
    n = len(rows)
    return {"n": n, "accuracy": (tp + tn) / n, "precision": tp / (tp + fp),
            "recall": tp / (tp + fn), "fpr": fp / (fp + tn), "flag_rate": (tp + fp) / n}


overall = metrics(records)
by_group = {g: metrics([r for r in records if r[0] == g]) for g in COUNTS}

print("[1] Accuracy on 200 labelled events")
print(f"  {'group':<8}{'n':>4}{'acc':>7}{'prec':>7}{'recall':>8}{'FPR':>7}{'flagged':>9}")
for name, m in [("ALL", overall)] + list(by_group.items()):
    print(f"  {name:<8}{m['n']:>4}{m['accuracy']:>7.2f}{m['precision']:>7.2f}"
          f"{m['recall']:>8.2f}{m['fpr']:>7.2f}{m['flag_rate']:>9.2f}")

# ---------- 2. Fairness ----------
fpr_gap = abs(by_group["student"]["fpr"] - by_group["staff"]["fpr"])
rates = [by_group[g]["flag_rate"] for g in COUNTS]
flag_ratio = min(rates) / max(rates)
print("\n[2] Fairness")
print(f"  FPR gap (student - staff): {fpr_gap:.3f}  -> innocent students are flagged "
      f"{by_group['student']['fpr'] / by_group['staff']['fpr']:.1f}x as often")
print(f"  Flag-rate ratio: {flag_ratio:.2f}  (below 0.80 suggests unequal treatment)")

# ---------- 3. Drift ----------
BINS = ["00-06", "06-12", "12-18", "18-24"]
train_share = [0.05, 0.45, 0.35, 0.15]   # login hours when the model was trained
now_share = [0.08, 0.30, 0.32, 0.30]     # this month: evening classes added


def psi(expected, actual):
    return sum((a - e) * math.log(a / e) for e, a in zip(expected, actual))


drift = psi(train_share, now_share)
print("\n[3] Drift in login-hour distribution")
for b, e, a in zip(BINS, train_share, now_share):
    print(f"  {b}  train {e:4.0%}  now {a:4.0%}  {'#' * round(a * 40)}")
print(f"  PSI = {drift:.3f}  (<0.10 stable, 0.10-0.25 monitor, >0.25 retrain)")

WEEKLY = [(186, 200), (184, 200), (182, 200), (176, 200), (170, 200), (164, 200)]
trend = [c / t for c, t in WEEKLY]
print("  Weekly accuracy:", " ".join(f"W{i + 1}={a:.2f}" for i, a in enumerate(trend)))

# ---------- 4. Scorecard against the governance policy ----------
POLICY = [  # (check, value, passes?, action if it fails)
    ("Accuracy >= 0.85", overall["accuracy"], overall["accuracy"] >= 0.85, "retrain / tune"),
    ("Recall >= 0.80", overall["recall"], overall["recall"] >= 0.80, "lower alert threshold"),
    ("Precision >= 0.70", overall["precision"], overall["precision"] >= 0.70, "reduce false alarms"),
    ("FPR gap <= 0.05", fpr_gap, fpr_gap <= 0.05, "add group-aware baselines, review features"),
    ("Flag-rate ratio >= 0.80", flag_ratio, flag_ratio >= 0.80, "bias review before next release"),
    ("PSI < 0.10", drift, drift < 0.10, "monitor weekly; retrain if PSI > 0.25"),
    ("Latest weekly accuracy >= 0.85", trend[-1], trend[-1] >= 0.85, "retrain on recent data"),
]
print("\n[4] Governance scorecard")
fails = 0
for check, value, ok, action in POLICY:
    fails += not ok
    print(f"  {'PASS' if ok else 'FAIL'}  {check:<31} value {value:.3f}" + ("" if ok else f"  -> {action}"))
verdict = "APPROVED" if fails == 0 else "APPROVED WITH CONDITIONS" if fails <= 2 else "NOT APPROVED"
print(f"\n  {fails} of {len(POLICY)} checks failed -> model status: {verdict}")
print("  Decision owner: CISO with the AI governance committee (human sign-off).")
