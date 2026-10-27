"""Session 3 - A hash-chained chain-of-custody ledger.

Courts accept digital evidence only if the prosecution can show who held it, when,
why, and that it never changed. A paper custody form can be rewritten quietly; this
ledger cannot. Each entry stores the SHA-256 hash of the previous entry, so editing
any old line breaks every link after it (the same idea a blockchain uses).

All people, cases and evidence below are fictional. The script uses fixed times so
the output is the same on every run.
Run:  python session-03_custody_ledger.py
"""
import hashlib
import json

GENESIS = "0" * 64


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def entry_hash(entry):
    """Hash every field except the entry's own hash, in a fixed key order."""
    body = {k: v for k, v in entry.items() if k != "hash"}
    return sha256(json.dumps(body, sort_keys=True).encode())


class CustodyLedger:
    def __init__(self, case_id):
        self.case_id = case_id
        self.entries = []

    def add(self, time, item, action, from_person, to_person, purpose, item_sha256):
        prev = self.entries[-1]["hash"] if self.entries else GENESIS
        entry = {
            "seq": len(self.entries) + 1, "case": self.case_id, "time": time,
            "item": item, "action": action, "from": from_person, "to": to_person,
            "purpose": purpose, "item_sha256": item_sha256, "prev": prev,
        }
        entry["hash"] = entry_hash(entry)
        self.entries.append(entry)
        return entry

    def verify(self, current_item_hashes):
        """Return a list of problems; an empty list means the ledger is intact."""
        problems, prev = [], GENESIS
        first_hash = {}
        for e in self.entries:
            if e["prev"] != prev:
                problems.append(f"entry {e['seq']}: link to previous entry is broken")
            if entry_hash(e) != e["hash"]:
                problems.append(f"entry {e['seq']}: contents were edited after signing")
            first_hash.setdefault(e["item"], e["item_sha256"])
            if e["item_sha256"] != first_hash[e["item"]]:
                problems.append(f"entry {e['seq']}: {e['item']} hash differs from acquisition")
            prev = e["hash"]
        for item, h in current_item_hashes.items():
            if h != first_hash.get(item):
                problems.append(f"{item}: evidence today does not match the acquisition hash")
        return problems


# --- fictional evidence (bytes stand in for real disk/phone images) ---
laptop_img = b"EXHIBIT HZ-01 laptop image: invoices.xlsx, mail.pst, browser history"
phone_img = b"EXHIBIT HZ-02 phone extraction: chats, call log, photos"
H1, H2 = sha256(laptop_img), sha256(phone_img)

ledger = CustodyLedger("KHI-CC-2026-0147")
ledger.add("2026-10-20 09:40 PKT", "HZ-01 laptop", "SEIZED", "suspect desk, Office 3", "Insp. Rabia", "Search under warrant", H1)
ledger.add("2026-10-20 09:55 PKT", "HZ-02 phone", "SEIZED", "suspect pocket", "Insp. Rabia", "Search under warrant", H2)
ledger.add("2026-10-20 13:10 PKT", "HZ-01 laptop", "TRANSFER", "Insp. Rabia", "Evidence room (Clerk Danish)", "Secure storage, bag seal 55871", H1)
ledger.add("2026-10-21 10:05 PKT", "HZ-01 laptop", "TRANSFER", "Clerk Danish", "Analyst Omer (forensic lab)", "Imaging with write blocker", H1)
ledger.add("2026-10-21 16:30 PKT", "HZ-01 laptop", "RETURN", "Analyst Omer", "Clerk Danish", "Imaging complete, seal 55902", H1)

print(f"Chain of custody for case {ledger.case_id}\n")
print(f"{'#':>2}  {'time':<20} {'item':<13} {'action':<9} {'from -> to':<52} hash")
for e in ledger.entries:
    who = f"{e['from']} -> {e['to']}"
    print(f"{e['seq']:>2}  {e['time']:<20} {e['item']:<13} {e['action']:<9} {who[:52]:<52} {e['hash'][:12]}..")
print(f"\nItem hashes at acquisition: HZ-01 {H1[:16]}..  HZ-02 {H2[:16]}..")

today = {"HZ-01 laptop": sha256(laptop_img), "HZ-02 phone": sha256(phone_img)}
problems = ledger.verify(today)
print("\n[1] Verify untouched ledger:", "INTACT" if not problems else problems)

# --- Scenario 2: someone quietly rewrites who held the laptop on 21 Oct ---
ledger.entries[3]["to"] = "Unknown contractor"
print("\n[2] Entry 4 edited to hide an unrecorded hand-over:")
for p in ledger.verify(today):
    print("   !", p)
ledger.entries[3]["to"] = "Analyst Omer (forensic lab)"      # undo for the next test

# --- Scenario 3: the forger also recomputes entry 4's own hash ---
ledger.entries[3]["to"] = "Unknown contractor"
ledger.entries[3]["hash"] = entry_hash(ledger.entries[3])
print("\n[3] Entry 4 edited AND its own hash recomputed:")
for p in ledger.verify(today):
    print("   !", p)
print("   -> the next entry still points at the old hash, so the chain exposes it.")
ledger.entries[3]["to"] = "Analyst Omer (forensic lab)"
ledger.entries[3]["hash"] = entry_hash(ledger.entries[3])

# --- Scenario 4: the evidence file itself changes in storage ---
tampered = laptop_img.replace(b"invoices", b"invoicez")
print("\n[4] One byte of the laptop image changed in storage:")
for p in ledger.verify({"HZ-01 laptop": sha256(tampered), "HZ-02 phone": H2}):
    print("   !", p)
print("\nTip: print the last entry hash on the paper form and in the case file;")
print("anyone can later recompute the chain and compare it with that number.")
print("Last entry hash:", ledger.entries[-1]["hash"])
