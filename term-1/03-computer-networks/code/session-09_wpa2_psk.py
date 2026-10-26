"""Session 9 - Why WPA2-Personal needs a long passphrase.

WPA2-PSK turns the passphrase into a 256-bit Pairwise Master Key with
PBKDF2-HMAC-SHA1(passphrase, SSID, 4096 iterations, 32 bytes).
The SSID is the salt, so the same password on a different network gives a
different key. Anyone who records a handshake can try guesses OFFLINE, so the
only defence for PSK networks is a long, random passphrase (or WPA3-SAE).
Run:  python session-09_wpa2_psk.py
"""
import hashlib


def pmk(passphrase: str, ssid: str) -> bytes:
    return hashlib.pbkdf2_hmac("sha1", passphrase.encode(), ssid.encode(), 4096, 32)


if __name__ == "__main__":
    print("PMK for 'CampusLab2026!' on SSID 'LAB-WIFI':")
    print(" ", pmk("CampusLab2026!", "LAB-WIFI").hex())
    print("Same passphrase, SSID 'HOME-WIFI':")
    print(" ", pmk("CampusLab2026!", "HOME-WIFI").hex(), "(different: SSID is the salt)")

    # Each guess costs 4096 x 2 SHA-1 operations. Assume an attacker's GPU manages
    # about one million guesses per second (order-of-magnitude teaching figure).
    gpu = 1_000_000
    print()
    print(f"{'passphrase style':<34}{'combinations':>14}  worst-case time on 1 GPU")
    styles = [("8 lowercase letters", 26 ** 8), ("8 chars, upper+lower+digits", 62 ** 8),
              ("10 chars, 94 printable symbols", 94 ** 10), ("4 random dictionary words (7776)", 7776 ** 4),
              ("6 random dictionary words", 7776 ** 6)]
    for name, space in styles:
        secs = space / gpu
        if secs < 86400: t = f"{secs / 3600:,.1f} hours"
        elif secs < 3.15e7: t = f"{secs / 86400:,.1f} days"
        elif secs < 3.15e7 * 1000: t = f"{secs / 3.15e7:,.1f} years"
        else: t = f"{secs / 3.15e7:.1e} years"
        print(f"{name:<34}{space:>14.2e}  {t}")
