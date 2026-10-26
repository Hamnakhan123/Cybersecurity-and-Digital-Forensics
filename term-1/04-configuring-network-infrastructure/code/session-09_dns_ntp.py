"""Session 9 - Look inside DNS, NTP and TFTP messages (built and parsed offline).

1. Build a real DNS query for an A record and parse a sample answer.
2. Compute NTP clock offset and delay from the four timestamps.
3. Build TFTP read-request and data packets (how a router backs up its config).
Nothing is sent on the network.
Run:  python session-09_dns_ntp.py
"""
import struct


def dns_query(name, qtype=1, ident=0x1A2B):
    header = struct.pack("!HHHHHH", ident, 0x0100, 1, 0, 0, 0)   # RD flag set, 1 question
    qname = b"".join(len(p).to_bytes(1, "big") + p.encode() for p in name.split(".")) + b"\0"
    return header + qname + struct.pack("!HH", qtype, 1)          # type A, class IN


def dns_answer_for(query, ip, ttl=300):
    ident = struct.unpack("!H", query[:2])[0]
    header = struct.pack("!HHHHHH", ident, 0x8180, 1, 1, 0, 0)    # response, RD+RA, no error
    answer = b"\xc0\x0c" + struct.pack("!HHIH", 1, 1, ttl, 4) + bytes(map(int, ip.split(".")))
    return header + query[12:] + answer                             # c00c = pointer to the name


def parse_answer(msg):
    ident, flags, qd, an, _, _ = struct.unpack("!HHHHHH", msg[:12])
    i, labels = 12, []
    while msg[i]:
        labels.append(msg[i + 1:i + 1 + msg[i]].decode()); i += msg[i] + 1
    i += 5                                                          # zero byte + qtype + qclass
    _, rtype, _, ttl, rdlen = struct.unpack("!HHHIH", msg[i:i + 12])
    ip = ".".join(map(str, msg[i + 12:i + 12 + rdlen]))
    rcode = flags & 0xF
    return {"id": hex(ident), "name": ".".join(labels), "answers": an, "type": rtype, "ttl": ttl,
            "ip": ip, "rcode": rcode}


def ntp_offset(t1, t2, t3, t4):
    """t1 client send, t2 server receive, t3 server send, t4 client receive."""
    return ((t2 - t1) + (t3 - t4)) / 2, (t4 - t1) - (t3 - t2)


def tftp_request(opcode, filename, mode="octet"):
    """opcode 1 = RRQ (read/download), 2 = WRQ (write/upload)."""
    return struct.pack("!H", opcode) + filename.encode() + b"\0" + mode.encode() + b"\0"


def tftp_data(block, data):
    return struct.pack("!HH", 3, block) + data


if __name__ == "__main__":
    q = dns_query("portal.lab.local")
    print(f"DNS query ({len(q)} bytes, UDP 53): {q.hex(' ')}")
    a = dns_answer_for(q, "10.20.30.40")
    print(f"DNS answer ({len(a)} bytes) parsed: {parse_answer(a)}")

    print("\nNTP: client clock is behind the server")
    t1, t2, t3, t4 = 1000.000, 1002.530, 1002.531, 1000.061
    off, delay = ntp_offset(t1, t2, t3, t4)
    print(f"  t1={t1} t2={t2} t3={t3} t4={t4}")
    print(f"  offset = {off:+.4f} s (client must move forward), round-trip delay = {delay:.4f} s")
    for stratum, src in [(0, "atomic clock / GPS"), (1, "server attached to stratum 0"),
                         (2, "core router syncing from stratum 1"), (3, "access switches syncing from the core")]:
        print(f"  stratum {stratum}: {src}")

    print("\nTFTP (UDP 69): router backs up its config to a TFTP server")
    wrq = tftp_request(2, "R1-confg")
    print(f"  WRQ  opcode 2 (upload/backup): {wrq}")
    print(f"  RRQ  opcode 1 (download/restore) would be: {tftp_request(1, 'R1-confg')}")
    config = b"hostname R1\n!\ninterface g0/0\n ip address 192.168.10.1 255.255.255.0\n"
    blocks = [config[i:i + 512] for i in range(0, len(config), 512)]
    for n, b in enumerate(blocks, 1):
        print(f"  DATA opcode 3 block {n}: {len(b)} bytes (< 512 means last block) -> ACK {n}")
    print("  No login and no encryption: use TFTP only on a trusted management network.")
