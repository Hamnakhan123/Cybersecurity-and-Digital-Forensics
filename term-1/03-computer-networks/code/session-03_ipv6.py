"""Session 3 - IPv6 essentials: compress/expand, address types and EUI-64.

Run:  python session-03_ipv6.py
"""
import ipaddress


def eui64_interface_id(mac: str) -> str:
    """Build the 64-bit interface ID from a 48-bit MAC (modified EUI-64).
    1. split the MAC in half and insert FF:FE in the middle
    2. flip bit 7 (the universal/local bit) of the first byte
    """
    b = [int(x, 16) for x in mac.split(":")]
    b = b[:3] + [0xFF, 0xFE] + b[3:]
    b[0] ^= 0x02
    groups = [f"{b[i]:02x}{b[i + 1]:02x}" for i in range(0, 8, 2)]
    return ":".join(groups)


def classify(addr: str) -> str:
    a = ipaddress.ip_address(addr)
    if a.is_loopback: return "loopback (::1)"
    if a.is_link_local: return "link-local (fe80::/10, never routed)"
    if a.is_multicast: return "multicast (ff00::/8)"
    if a in ipaddress.ip_network("fc00::/7"): return "unique local (fc00::/7, like private IPv4)"
    if a in ipaddress.ip_network("2001:db8::/32"): return "documentation (2001:db8::/32)"
    if a in ipaddress.ip_network("2000::/3"): return "global unicast (2000::/3)"
    if a.is_unspecified: return "unspecified (::)"
    return "other"


if __name__ == "__main__":
    print("Compress / expand:")
    for full in ["2001:0db8:0000:0000:0000:ff00:0042:8329",
                 "fe80:0000:0000:0000:0202:b3ff:fe1e:8329",
                 "0000:0000:0000:0000:0000:0000:0000:0001"]:
        a = ipaddress.IPv6Address(full)
        print(f"  {a.exploded}  ->  {a.compressed}")

    print("\nAddress types:")
    for x in ["::1", "fe80::1", "ff02::1", "fd12:3456:789a::10",
              "2001:db8:acad:1::5", "2606:4700:4700::1111", "::"]:
        print(f"  {x:<24} {classify(x)}")

    mac = "00:1a:2b:3c:4d:5e"
    iid = eui64_interface_id(mac)
    prefix = ipaddress.IPv6Network("2001:db8:acad:10::/64")
    full = ipaddress.IPv6Address(f"2001:db8:acad:10:{iid}")
    print(f"\nEUI-64 from MAC {mac}: interface ID {iid}")
    print(f"  SLAAC address in {prefix}: {full}")
    print(f"  link-local address:            {ipaddress.IPv6Address('fe80::' + iid)}")

    print(f"\nA single /64 holds {prefix.num_addresses:,} addresses")
    print(f"IPv4 has only        {2**32:,} in total")
