"""Session 3 - MAC address anatomy: OUI, unicast/multicast and local/universal bits.

Reads a MAC in any common notation (colon, hyphen, Cisco dotted), normalises it,
splits the OUI from the device part, decodes the I/G and U/L bits, and builds
the modified EUI-64 interface ID that IPv6 SLAAC can derive from it.
The small OUI table is a sample for teaching, not a full vendor database.
Run:  python session-03_mac_tool.py
"""
import re

SAMPLE_OUI = {"00:50:56": "VMware", "00:1A:2B": "Example vendor (lab)",
              "3C:5A:B4": "Google", "00:00:0C": "Cisco"}


def normalise(mac: str) -> str:
    hexdigits = re.sub(r"[^0-9a-fA-F]", "", mac)
    if len(hexdigits) != 12:
        raise ValueError(f"{mac!r} is not a 48-bit MAC address")
    return ":".join(hexdigits[i:i + 2] for i in range(0, 12, 2)).upper()


def cisco_format(mac: str) -> str:
    h = normalise(mac).replace(":", "").lower()
    return f"{h[0:4]}.{h[4:8]}.{h[8:12]}"


def describe(mac: str) -> dict:
    m = normalise(mac)
    first = int(m[:2], 16)
    kind = "broadcast" if m == "FF:FF:FF:FF:FF:FF" else ("multicast" if first & 1 else "unicast")
    return {"mac": m, "cisco": cisco_format(m), "oui": m[:8], "nic": m[9:],
            "vendor": SAMPLE_OUI.get(m[:8], "not in sample table"), "type": kind,
            "admin": "locally administered" if first & 2 else "universally administered (burned-in)"}


def eui64(mac: str) -> str:
    """Modified EUI-64: insert FFFE in the middle and flip the U/L bit (bit 7 of byte 1)."""
    b = bytearray(int(x, 16) for x in normalise(mac).split(":"))
    b[0] ^= 0x02
    full = bytes(b[:3]) + b"\xff\xfe" + bytes(b[3:])
    return ":".join(full[i:i + 2].hex() for i in range(0, 8, 2))


if __name__ == "__main__":
    for raw in ["00-50-56-c0-00-08", "0000.0c9f.f00a", "01:00:5E:00:00:05",
                "ff:ff:ff:ff:ff:ff", "3c:5a:b4:12:34:56", "02:42:ac:11:00:02"]:
        d = describe(raw)
        print(f"{raw:20} -> {d['mac']}  ({d['cisco']})")
        print(f"   OUI {d['oui']} [{d['vendor']}], NIC part {d['nic']}, {d['type']}, {d['admin']}")
    print("\nModified EUI-64 interface ID for SLAAC")
    for raw in ["00:1A:2B:3C:4D:5E", "3c:5a:b4:12:34:56"]:
        print(f"  {normalise(raw)} -> {eui64(raw)}  -> fe80::{eui64(raw).lstrip('0')}")
