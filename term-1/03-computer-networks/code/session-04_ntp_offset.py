"""Session 4 - How NTP works out the clock offset and the round-trip delay
from four timestamps, and why log timestamps go wrong when clocks drift.

t1 = client sends request    (client clock)
t2 = server receives it      (server clock)
t3 = server sends reply      (server clock)
t4 = client receives reply   (client clock)
offset = ((t2 - t1) + (t3 - t4)) / 2
delay  = (t4 - t1) - (t3 - t2)
Run:  python session-04_ntp_offset.py
"""


def ntp(t1, t2, t3, t4):
    offset = ((t2 - t1) + (t3 - t4)) / 2
    delay = (t4 - t1) - (t3 - t2)
    return offset, delay


if __name__ == "__main__":
    # Times in milliseconds. The client clock is really 250 ms BEHIND the server.
    samples = [
        ("LAN server",        1000.0, 1255.0, 1256.0, 1012.0),
        ("Internet server",   2000.0, 2290.0, 2291.0, 2081.0),
        ("Asymmetric path",   3000.0, 3310.0, 3311.0, 3071.0),
    ]
    print(f"{'Source':<18}{'offset ms':>10}{'delay ms':>10}")
    for name, t1, t2, t3, t4 in samples:
        o, d = ntp(t1, t2, t3, t4)
        print(f"{name:<18}{o:>10.1f}{d:>10.1f}")
    print("\nStratum: 0 = atomic/GPS clock, 1 = server wired to it, 2 = syncs from stratum 1 ...")

    # Why it matters: two devices log the same attack, one clock is 4 minutes slow.
    print("\nCorrelating firewall and server logs (server clock 240 s slow):")
    fw = [("09:15:02", "firewall: allowed 198.51.100.7 -> web01:443")]
    srv = [("09:11:05", "web01: admin login from 198.51.100.7")]
    def sec(t): h, m, s = map(int, t.split(":")); return h * 3600 + m * 60 + s
    for t, msg in fw + srv:
        print(f"  raw {t}  {msg}")
    corrected = sec(srv[0][0]) + 240
    print(f"  corrected server time = {corrected // 3600:02d}:{corrected % 3600 // 60:02d}:{corrected % 60:02d}"
          f" -> login happened 3 s AFTER the firewall allowed the connection")
