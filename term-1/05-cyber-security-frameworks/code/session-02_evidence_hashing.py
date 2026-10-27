"""Session 2 - Hash digital evidence at acquisition and verify it later.

Investigators never analyse original evidence directly. They make a copy (an "image"),
calculate a cryptographic hash of the original and of the copy, and record both.
If even one bit changes later, the hash changes completely, so the court can trust
that the evidence examined is exactly what was seized.

This script creates a small fictional "evidence folder" in a temporary directory,
hashes every file with MD5 and SHA-256 (as forensic tools such as FTK Imager report),
then simulates an accidental change and detects it. Everything is deleted at the end.
Run:  python session-02_evidence_hashing.py
"""
import hashlib
import json
import os
import shutil
import tempfile


def hash_file(path, chunk=65536):
    """Read in chunks so even multi-GB images fit in memory."""
    md5, sha = hashlib.md5(), hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            md5.update(block)
            sha.update(block)
    return md5.hexdigest(), sha.hexdigest()


def manifest(folder):
    out = {}
    for name in sorted(os.listdir(folder)):
        m, s = hash_file(os.path.join(folder, name))
        out[name] = {"bytes": os.path.getsize(os.path.join(folder, name)), "md5": m, "sha256": s}
    return out


def main():
    work = tempfile.mkdtemp(prefix="evidence_")
    try:
        ev = os.path.join(work, "EXHIBIT-07")
        os.makedirs(ev)
        files = {
            "chat_export.txt": "2026-09-14 21:03 buyer: send the account details\n2026-09-14 21:05 seller: ok\n",
            "invoice_scan.pdf": "%PDF-1.4 fictional invoice PKR 85,000\n",
            "browser_history.csv": "time,url\n2026-09-14 20:58,https://shop.example.com/checkout\n",
        }
        for name, text in files.items():
            with open(os.path.join(ev, name), "w") as f:
                f.write(text)

        print("1) Acquisition: hash every file and save the manifest")
        before = manifest(ev)
        for name, h in before.items():
            print(f"   {name:<20} {h['bytes']:>4} B  MD5 {h['md5'][:12]}...  SHA-256 {h['sha256'][:16]}...")
        with open(os.path.join(work, "EXHIBIT-07.manifest.json"), "w") as f:
            json.dump(before, f, indent=1)

        print("\n2) Working copy for analysis, verified against the manifest")
        copy = os.path.join(work, "EXHIBIT-07-working-copy")
        shutil.copytree(ev, copy)
        ok = manifest(copy) == before
        print(f"   Working copy identical to original: {ok}")

        print("\n3) Somebody 'tidies' the chat export on the working copy ('ok' -> 'no')")
        p = os.path.join(copy, "chat_export.txt")
        with open(p) as f:
            text = f.read()
        with open(p, "w") as f:
            f.write(text.replace("ok", "no"))
        after = manifest(copy)
        for name in before:
            same = before[name]["sha256"] == after[name]["sha256"]
            print(f"   {name:<20} {'VERIFIED' if same else 'MISMATCH - integrity broken'}")
        print(f"\n   Old SHA-256: {before['chat_export.txt']['sha256']}")
        print(f"   New SHA-256: {after['chat_export.txt']['sha256']}")
        print("   A 2-character edit changed the whole hash (avalanche effect).")
        print("\n4) Why two algorithms? MD5 is fast but has known collisions; SHA-256 is the")
        print("   value to rely on. Many labs record both for compatibility with older tools.")
    finally:
        shutil.rmtree(work)


if __name__ == "__main__":
    main()
