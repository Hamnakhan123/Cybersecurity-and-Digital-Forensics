"""Session 2 - Encapsulation with real header bytes: Ethernet / IPv4 / TCP.

Builds an HTTP request the way a host's protocol stack does, layer by layer,
computes the real IPv4 header checksum, prints a hex dump, then
de-encapsulates it the way the receiver does. All addresses are lab addresses.
Run:  python session-02_encapsulate.py
"""
import struct


def checksum(data: bytes) -> int:
    """Internet checksum (RFC 1071): one's complement of the one's-complement sum."""
    if len(data) % 2:
        data += b"\0"
    s = sum(struct.unpack(f"!{len(data)//2}H", data))
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return ~s & 0xFFFF


def mac(s): return bytes(int(x, 16) for x in s.split(":"))
def ip(s): return bytes(int(x) for x in s.split("."))


# Layer 7: application data
payload = b"GET / HTTP/1.1\r\nHost: lab.local\r\n\r\n"

# Layer 4: TCP header (20 bytes, no options). Flags 0x18 = PSH + ACK
tcp = struct.pack("!HHIIBBHHH", 50123, 80, 1000, 2000, 5 << 4, 0x18, 64240, 0, 0)
segment = tcp + payload

# Layer 3: IPv4 header (20 bytes). Checksum computed over the header only
ver_ihl, tos, total_len = 0x45, 0, 20 + len(segment)
ident, flags_frag, ttl, proto = 0x1C46, 0x4000, 64, 6
hdr = struct.pack("!BBHHHBBH4s4s", ver_ihl, tos, total_len, ident, flags_frag, ttl, proto, 0,
                  ip("192.168.10.25"), ip("192.168.20.80"))
hdr = hdr[:10] + struct.pack("!H", checksum(hdr)) + hdr[12:]
packet = hdr + segment

# Layer 2: Ethernet II header (dst MAC, src MAC, EtherType 0x0800 = IPv4)
frame = mac("00:1a:2b:3c:4d:5e") + mac("00:50:56:aa:bb:cc") + b"\x08\x00" + packet


def hexdump(b, width=16):
    for i in range(0, len(b), width):
        chunk = b[i:i + width]
        text = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
        print(f"  {i:04x}  {chunk.hex(' '):<{width*3}} {text}")


if __name__ == "__main__":
    print(f"L7 data     {len(payload):3} bytes")
    print(f"L4 segment  {len(segment):3} bytes (+20 TCP header)")
    print(f"L3 packet   {len(packet):3} bytes (+20 IPv4 header)")
    print(f"L2 frame    {len(frame):3} bytes (+14 Ethernet header, FCS added by the NIC)\n")
    hexdump(frame)

    print("\nReceiver de-encapsulates:")
    dst, src, etype = frame[0:6], frame[6:12], struct.unpack("!H", frame[12:14])[0]
    print(f"  L2: dst {dst.hex(':')} src {src.hex(':')} type 0x{etype:04x} -> IPv4")
    ih = frame[14:34]
    v, _, tl, _, _, t, pr, cs, s, d = struct.unpack("!BBHHHBBH4s4s", ih)
    print(f"  L3: version {v >> 4}, length {tl}, TTL {t}, protocol {pr} (TCP), "
          f"{'.'.join(map(str, s))} -> {'.'.join(map(str, d))}")
    print(f"      header checksum 0x{cs:04x}; recomputed over header = 0x{checksum(ih):04x} (0 means valid)")
    sp, dp, seq, ack = struct.unpack("!HHII", frame[34:46])
    print(f"  L4: port {sp} -> {dp} (HTTP), seq {seq}, ack {ack}")
    first_line = frame[54:].split(b"\r\n")[0].decode()
    print(f"  L7: {first_line!r} (application data)")
