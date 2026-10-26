"""Session 14 - Audit WLAN profiles and estimate signal strength at a desk.

Part 1 grades each SSID's security settings the way a wireless engineer would
(WEP and TKIP are broken, WPA2-AES is acceptable, WPA3 with PMF is best,
Enterprise 802.1X beats a shared password for staff).
Part 2 is an RF link budget: received signal = transmit power + antenna
gains - free-space path loss - wall losses, compared with what a client needs.
Run:  python session-14_wlan_audit.py
"""
import math

PROFILES = [
    {"ssid": "Campus-Staff", "security": "WPA3-Enterprise", "cipher": "AES-GCMP", "pmf": "required",
     "auth": "802.1X/RADIUS", "psk_len": 0, "band": "5 GHz", "vlan": 10},
    {"ssid": "Campus-Students", "security": "WPA2-Personal", "cipher": "AES-CCMP", "pmf": "optional",
     "auth": "PSK", "psk_len": 16, "band": "2.4+5 GHz", "vlan": 20},
    {"ssid": "Old-Lab-AP", "security": "WEP", "cipher": "RC4", "pmf": "off",
     "auth": "shared key", "psk_len": 10, "band": "2.4 GHz", "vlan": 1},
    {"ssid": "Cafe-Guest", "security": "WPA/WPA2-Mixed", "cipher": "TKIP+AES", "pmf": "off",
     "auth": "PSK", "psk_len": 8, "band": "2.4 GHz", "vlan": 1},
]


def grade(p):
    issues = []
    if p["security"] == "WEP":
        issues.append("WEP is broken (key recoverable in minutes) - replace with WPA2/WPA3")
    if "TKIP" in p["cipher"]:
        issues.append("TKIP allowed - use AES (CCMP/GCMP) only")
    if p["auth"] == "PSK" and p["psk_len"] < 12:
        issues.append(f"PSK only {p['psk_len']} chars - offline guessing is easy; use 16+ random chars")
    if p["pmf"] == "off":
        issues.append("PMF (802.11w) off - deauthentication frames can be spoofed")
    if p["vlan"] == 1:
        issues.append("mapped to VLAN 1 - put each SSID in its own VLAN")
    score = max(0, 100 - 25 * len(issues))
    return score, issues


def fspl_db(distance_m, freq_mhz):
    """Free-space path loss: 20log10(d km) + 20log10(f MHz) + 32.44"""
    return 20 * math.log10(distance_m / 1000) + 20 * math.log10(freq_mhz) + 32.44


def rx_dbm(tx_dbm, gain_tx, gain_rx, distance_m, freq_mhz, walls_db):
    return tx_dbm + gain_tx + gain_rx - fspl_db(distance_m, freq_mhz) - walls_db


if __name__ == "__main__":
    print("Part 1: WLAN security audit")
    for p in PROFILES:
        score, issues = grade(p)
        print(f"  {p['ssid']:16} {p['security']:16} score {score:3}/100")
        for i in issues:
            print(f"      - {i}")
    print("\nPart 2: signal at a classroom desk 25 m from the AP through 2 brick walls (2 x 6 dB)")
    for band, f in (("2.4 GHz ch 6", 2437), ("5 GHz ch 36", 5180)):
        r = rx_dbm(tx_dbm=17, gain_tx=4, gain_rx=0, distance_m=25, freq_mhz=f, walls_db=12)
        verdict = "good for video calls" if r >= -67 else ("usable for web" if r >= -75 else "too weak")
        print(f"  {band:13} path loss {fspl_db(25, f):5.1f} dB -> received {r:6.1f} dBm ({verdict})")
    print("  Rule of thumb: design for -67 dBm or better and at least 25 dB above the noise floor.")
