"""Session 5 - Will this link become a trunk? The DTP negotiation matrix.

Dynamic Trunking Protocol (Cisco) lets two switch ports agree on trunk or
access. Security best practice is to switch it off: hard-code access ports
with "switchport mode access" + "switchport nonegotiate", and trunks with
"switchport mode trunk" + "switchport nonegotiate".
Run:  python session-05_dtp_matrix.py
"""

MODES = ["access", "dynamic auto", "dynamic desirable", "trunk"]


def result(a, b):
    if "access" in (a, b):
        if {a, b} == {"access", "trunk"}:
            return "mismatch!"         # one side tags, the other does not
        return "access"
    if a == "trunk" or b == "trunk":
        return "trunk"
    if "dynamic desirable" in (a, b):
        return "trunk"
    return "access"                      # auto + auto: nobody asks


if __name__ == "__main__":
    w = 18
    print(" " * w + "".join(f"{m:>{w}}" for m in MODES))
    for a in MODES:
        print(f"{a:<{w}}" + "".join(f"{result(a, b):>{w}}" for b in MODES))
    print("\nWhy it matters for security:")
    print(" - A port left in 'dynamic desirable' or 'dynamic auto' can be talked into trunking")
    print("   by a device that speaks DTP, giving it access to every VLAN (VLAN hopping).")
    print(" - Fix: switchport mode access + switchport nonegotiate on every user port.")
    print("\nVTP reminder: a switch in server mode with a HIGHER revision number")
    print("overwrites the VLAN database of every client in the domain. Use VTP transparent")
    print("or VTP v3 with a primary server, and reset the revision before adding a switch.")
