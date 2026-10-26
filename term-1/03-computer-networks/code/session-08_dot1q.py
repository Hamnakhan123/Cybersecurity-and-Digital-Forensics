"""Session 8 - Build and read an IEEE 802.1Q (VLAN) tagged Ethernet header.

A trunk link carries frames for many VLANs. The 4-byte tag sits between the
source MAC and the EtherType: TPID 0x8100 + 3-bit priority + 1-bit DEI + 12-bit VLAN ID.
Only bytes in memory are built here; nothing is sent.
Run:  python session-08_dot1q.py
"""
import struct


def mac_bytes(mac):
    return bytes(int(x, 16) for x in mac.split(":"))


def build_frame(dst, src, vlan=None, prio=0, ethertype=0x0800, payload=b"IPv4..."):
    hdr = mac_bytes(dst) + mac_bytes(src)
    if vlan is not None:
        if not 1 <= vlan <= 4094:
            raise ValueError("VLAN ID must be 1-4094 (0 and 4095 are reserved)")
        tci = (prio << 13) | (0 << 12) | vlan
        hdr += struct.pack("!HH", 0x8100, tci)
    return hdr + struct.pack("!H", ethertype) + payload


def parse(frame):
    dst = ":".join(f"{b:02x}" for b in frame[0:6])
    src = ":".join(f"{b:02x}" for b in frame[6:12])
    (tpid,) = struct.unpack("!H", frame[12:14])
    if tpid == 0x8100:
        (tci,) = struct.unpack("!H", frame[14:16])
        (etype,) = struct.unpack("!H", frame[16:18])
        return dict(dst=dst, src=src, tagged=True, prio=tci >> 13, vlan=tci & 0x0FFF, etype=hex(etype))
    return dict(dst=dst, src=src, tagged=False, vlan="native/access", etype=hex(tpid))


if __name__ == "__main__":
    pc = "aa:bb:cc:00:00:10"; gw = "aa:bb:cc:00:00:01"
    untagged = build_frame(gw, pc)
    voice = build_frame(gw, pc, vlan=20, prio=5)
    data = build_frame(gw, pc, vlan=10)
    for name, f in [("access port (untagged)", untagged), ("trunk, VLAN 10 data", data),
                    ("trunk, VLAN 20 voice", voice)]:
        print(f"{name:<24} {len(f):>2} bytes  hex: {f[:18].hex(' ')}")
        print(f"{'':<24} parsed -> {parse(f)}")
    print("\nTag adds", len(data) - len(untagged), "bytes; 12-bit VLAN ID gives", 2 ** 12 - 2, "usable VLANs")
    try:
        build_frame(gw, pc, vlan=5000)
    except ValueError as e:
        print("Rejected:", e)
