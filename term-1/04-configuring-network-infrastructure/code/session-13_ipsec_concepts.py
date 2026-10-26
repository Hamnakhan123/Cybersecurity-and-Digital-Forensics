"""Session 13 - The security building blocks of a VPN, shown with real primitives.

1. Diffie-Hellman: two gateways agree on a shared secret over an open network
   (IKE does this with standard groups; here the 2048-bit RFC 3526 group 14).
2. Key derivation: turn the shared secret into separate keys (HKDF-style, HMAC-SHA256).
3. Integrity and authenticity: an HMAC tag proves a packet was not changed.
4. Anti-replay: a sequence-number window rejects copied packets.
Educational only: real VPNs use vetted implementations (IOS, strongSwan, WireGuard).
Run:  python session-13_ipsec_concepts.py
"""
import hashlib
import hmac
import secrets

P = int("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DD"
        "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
        "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
        "83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
        "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
        "15728E5A8AACAA68FFFFFFFFFFFFFFFF", 16)          # RFC 3526 MODP group 14 (2048-bit)
G = 2


def hkdf(secret: bytes, info: bytes, length=32) -> bytes:
    prk = hmac.new(b"lab-salt", secret, hashlib.sha256).digest()
    return hmac.new(prk, info + b"\x01", hashlib.sha256).digest()[:length]


class ReplayWindow:
    def __init__(self, size=64):
        self.size, self.highest, self.seen = size, 0, set()

    def accept(self, seq):
        if seq in self.seen or seq <= self.highest - self.size:
            return False
        self.seen.add(seq); self.highest = max(self.highest, seq)
        return True


if __name__ == "__main__":
    a_priv, b_priv = secrets.randbelow(P - 3) + 2, secrets.randbelow(P - 3) + 2
    a_pub, b_pub = pow(G, a_priv, P), pow(G, b_priv, P)
    print("1) Diffie-Hellman over an untrusted network (group 14, 2048-bit)")
    print(f"   Karachi gateway sends public value ({a_pub.bit_length()} bits)  {hex(a_pub)[:22]}...")
    print(f"   Lahore  gateway sends public value ({b_pub.bit_length()} bits)  {hex(b_pub)[:22]}...")
    s_a, s_b = pow(b_pub, a_priv, P), pow(a_pub, b_priv, P)
    print(f"   both computed the same secret: {s_a == s_b} (an eavesdropper saw only the public values)")

    shared = s_a.to_bytes(256, "big")
    k_enc, k_auth = hkdf(shared, b"encryption"), hkdf(shared, b"integrity")
    print("\n2) Separate keys derived from the shared secret")
    print(f"   encryption key length {len(k_enc) * 8} bits, integrity key length {len(k_auth) * 8} bits, "
          f"different: {k_enc != k_auth}")

    print("\n3) Integrity: HMAC-SHA256 tag on each packet")
    pkt = b"seq=1001|src=10.1.0.5|dst=10.2.0.9|payload=grade-sheet.xlsx"
    tag = hmac.new(k_auth, pkt, hashlib.sha256).digest()
    tampered = pkt.replace(b"10.2.0.9", b"10.66.6.6")
    for label, p in (("original", pkt), ("tampered in transit", tampered)):
        ok = hmac.compare_digest(tag, hmac.new(k_auth, p, hashlib.sha256).digest())
        print(f"   {label:20} -> {'ACCEPT' if ok else 'DROP (ICV mismatch)'}")

    print("\n4) Anti-replay window (64 packets)")
    w = ReplayWindow()
    for seq in (1001, 1002, 1004, 1003, 1002, 900):
        print(f"   seq {seq}: {'accept' if w.accept(seq) else 'REJECT (replayed or too old)'}")
