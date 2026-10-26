"""Session 10 - Network performance metrics from ping-style samples:
latency, jitter, packet loss, throughput/utilisation and the meaning of "nines".

The RTT samples are a recorded lab capture (None = lost packet).
Run:  python session-10_metrics.py
"""
import statistics

SAMPLES = {
    "LAN to file server":  [0.6, 0.5, 0.7, 0.6, 0.5, 0.6, 0.8, 0.6, 0.5, 0.6],
    "Branch over VPN":     [38, 41, 39, 120, 40, 42, None, 39, 41, 40],
    "Congested Wi-Fi":     [12, 85, 30, None, 140, 22, None, 95, 18, None],
}


def metrics(rtts):
    got = [r for r in rtts if r is not None]
    loss = 100 * (len(rtts) - len(got)) / len(rtts)
    jitter = statistics.mean(abs(a - b) for a, b in zip(got, got[1:]))   # mean delay variation
    return statistics.mean(got), min(got), max(got), jitter, loss


def voip_ok(avg, jitter, loss):
    return avg < 150 and jitter < 30 and loss < 1


if __name__ == "__main__":
    print(f"{'Link':<20}{'avg ms':>8}{'min':>6}{'max':>6}{'jitter':>8}{'loss':>7}  VoIP?")
    for name, s in SAMPLES.items():
        avg, lo, hi, j, loss = metrics(s)
        print(f"{name:<20}{avg:>8.1f}{lo:>6}{hi:>6}{j:>8.1f}{loss:>6.0f}%  {'yes' if voip_ok(avg, j, loss) else 'no'}")

    print("\nUtilisation of a 1 Gbps uplink from interface counters (5-minute interval):")
    bytes_before, bytes_after, secs = 8_250_000_000, 39_750_000_000, 300
    bps = (bytes_after - bytes_before) * 8 / secs
    print(f"  {bps / 1e6:,.0f} Mbps = {bps / 1e9:.0%} utilisation (alert threshold 70%)")

    print("\nAvailability 'nines' -> allowed downtime per year:")
    for a in (99, 99.9, 99.99, 99.999):
        mins = (1 - a / 100) * 365 * 24 * 60
        print(f"  {a:>7}%  {mins / 60:>7.2f} hours  ({mins:,.1f} minutes)")
