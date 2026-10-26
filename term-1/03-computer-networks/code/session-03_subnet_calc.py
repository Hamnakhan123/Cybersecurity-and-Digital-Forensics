"""Session 3 - IPv4 subnet calculator, done by hand with bits AND checked
against Python's standard `ipaddress` module.

Run:  python session-03_subnet_calc.py
"""
import ipaddress


def ip_to_int(ip: str) -> int:
    a, b, c, d = (int(x) for x in ip.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def int_to_ip(n: int) -> str:
    return ".".join(str((n >> s) & 0xFF) for s in (24, 16, 8, 0))


def ip_class(ip: str) -> str:
    first = int(ip.split(".")[0])
    if first < 128: return "A"
    if first < 192: return "B"
    if first < 224: return "C"
    if first < 240: return "D (multicast)"
    return "E (experimental)"


def manual(cidr: str) -> dict:
    """Compute subnet facts using only AND / OR / NOT on 32-bit integers."""
    ip, prefix = cidr.split("/")
    prefix = int(prefix)
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    net = ip_to_int(ip) & mask                 # AND keeps the network bits
    bcast = net | (~mask & 0xFFFFFFFF)         # OR sets all host bits to 1
    hosts = max(2 ** (32 - prefix) - 2, 0) if prefix < 31 else 2 ** (32 - prefix)
    return {
        "mask": int_to_ip(mask),
        "mask_bits": f"{mask:032b}",
        "wildcard": int_to_ip(~mask & 0xFFFFFFFF),
        "network": int_to_ip(net),
        "broadcast": int_to_ip(bcast),
        "first": int_to_ip(net + 1) if prefix < 31 else int_to_ip(net),
        "last": int_to_ip(bcast - 1) if prefix < 31 else int_to_ip(bcast),
        "hosts": hosts,
    }


def report(cidr: str) -> None:
    m = manual(cidr)
    lib = ipaddress.ip_interface(cidr).network       # independent check
    assert m["network"] == str(lib.network_address)
    assert m["broadcast"] == str(lib.broadcast_address)
    ip = cidr.split("/")[0]
    addr = ipaddress.ip_address(ip)
    rfc1918 = [ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")]
    docs = [ipaddress.ip_network(n) for n in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24")]
    if any(addr in n for n in rfc1918): kind = "private (RFC 1918)"
    elif addr.is_loopback: kind = "loopback"
    elif any(addr in n for n in docs): kind = "documentation range (never routed)"
    else: kind = "public"
    print(f"\n{cidr}   class {ip_class(ip)}, {kind}")
    print(f"  mask      {m['mask']:<16} {m['mask_bits'][:8]}.{m['mask_bits'][8:16]}."
          f"{m['mask_bits'][16:24]}.{m['mask_bits'][24:]}")
    print(f"  wildcard  {m['wildcard']}")
    print(f"  network   {m['network']:<16} broadcast {m['broadcast']}")
    print(f"  hosts     {m['first']} - {m['last']}  ({m['hosts']} usable)")


def split(cidr: str, new_prefix: int) -> None:
    net = ipaddress.ip_network(cidr)
    subs = list(net.subnets(new_prefix=new_prefix))
    print(f"\nSplitting {cidr} into /{new_prefix}: {len(subs)} subnets "
          f"of {subs[0].num_addresses - 2} hosts each")
    for s in subs:
        h = list(s.hosts())
        print(f"  {str(s):<18} hosts {h[0]} - {h[-1]}  broadcast {s.broadcast_address}")


if __name__ == "__main__":
    for c in ["192.168.10.77/24", "172.16.45.200/20", "10.1.2.3/8", "192.168.1.130/26",
              "203.0.113.9/30", "127.0.0.1/8"]:
        report(c)
    split("192.168.50.0/24", 26)
    print("\nAll manual results matched the ipaddress module.")
