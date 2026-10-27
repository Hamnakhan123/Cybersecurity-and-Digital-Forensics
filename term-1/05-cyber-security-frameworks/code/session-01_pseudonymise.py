"""Session 1 - Masking, hashing, keyed pseudonymisation and k-anonymity.

GDPR encourages "pseudonymisation": replacing identifiers so data can no longer be
linked to a person WITHOUT extra information that is kept separately and securely.
Pseudonymised data is STILL personal data. Truly anonymous data is not.

This script compares four techniques on fictional student records and shows why a
plain unsalted hash of a phone number is weak (it can be reversed by trying every
possible number), while a keyed HMAC with a secret key is much stronger.
Run:  python session-01_pseudonymise.py
"""
import hashlib
import hmac
import secrets
from collections import Counter

RECORDS = [  # fictional
    {"name": "Ayesha Raza", "phone": "03001234567", "age": 21, "city": "Karachi", "grade": "A"},
    {"name": "Hamza Ali",   "phone": "03001234568", "age": 22, "city": "Karachi", "grade": "B"},
    {"name": "Zara Shah",   "phone": "03111234569", "age": 21, "city": "Karachi", "grade": "A"},
    {"name": "Omar Siddiqui", "phone": "03211234570", "age": 34, "city": "Quetta", "grade": "C"},
    {"name": "Fatima Noor", "phone": "03001234571", "age": 23, "city": "Karachi", "grade": "B"},
]


def mask(phone):
    return phone[:4] + "*****" + phone[-2:]


def plain_hash(phone):
    return hashlib.sha256(phone.encode()).hexdigest()[:16]


def keyed(phone, key):
    return hmac.new(key, phone.encode(), hashlib.sha256).hexdigest()[:16]


def brute_force_plain(target, prefix="0300123", digits=4):
    """Try every number with a known prefix - shows why unsalted hashes of phones are weak."""
    for n in range(10 ** digits):
        guess = f"{prefix}{n:0{digits}d}"
        if plain_hash(guess) == target:
            return guess, n + 1
    return None, 10 ** digits


def generalise(r):
    """Coarsen quasi-identifiers: exact age -> age band, keep city."""
    lo = r["age"] // 10 * 10
    return (f"{lo}-{lo + 9}", r["city"])


def main():
    # TEACHING ONLY: a fixed key so the output is repeatable. In real life generate it with
    # secrets.token_bytes(32) and keep it in a key vault, away from the pseudonymised data.
    key = b"demo-key-0123456789abcdef-0123456"
    print(f"{'Name':<15}{'Masked':<14}{'SHA-256 (plain)':<18}{'HMAC (keyed)':<18}")
    for r in RECORDS:
        print(f"{r['name']:<15}{mask(r['phone']):<14}{plain_hash(r['phone']):<18}{keyed(r['phone'], key):<18}")
    same = keyed(RECORDS[0]["phone"], key) == keyed(RECORDS[0]["phone"], key)
    print(f"\nHMAC is consistent with the same key (records can still be joined): {same}")
    print("HMAC with a different key gives a different pseudonym:",
          keyed(RECORDS[0]["phone"], key) != keyed(RECORDS[0]["phone"], secrets.token_bytes(32)))

    target = plain_hash(RECORDS[4]["phone"])
    found, tries = brute_force_plain(target)
    print(f"\nAttack on the plain hash {target}: recovered {found} after {tries:,} guesses")
    print("Same attack on the HMAC is not possible without the secret key.")

    print("\nk-anonymity after generalising (age band, city):")
    groups = Counter(generalise(r) for r in RECORDS)
    for g, k in sorted(groups.items()):
        flag = "  <- unique: person can be singled out" if k == 1 else ""
        print(f"   {g[0]:<7} {g[1]:<8} k={k}{flag}")
    print(f"Dataset k = {min(groups.values())}  (want k >= 2, ideally much higher, before sharing)")


if __name__ == "__main__":
    main()
