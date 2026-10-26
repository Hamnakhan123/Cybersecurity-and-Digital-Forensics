"""Session 9 - A DHCP server's view: pool, exclusions, DORA and leases.

Mirrors what "ip dhcp pool" on a Cisco router does: hand out the lowest free
address that is not excluded, remember the lease against the client MAC,
renew at T1 (50% of the lease), and release addresses that expire.
Run:  python session-09_dhcp_pool.py
"""
import ipaddress


class DhcpServer:
    def __init__(self, network, gateway, dns, lease_s, excluded):
        self.net = ipaddress.ip_network(network)
        self.gateway, self.dns, self.lease_s = gateway, dns, lease_s
        self.excluded = set()
        for lo, hi in excluded:
            a, b = int(ipaddress.ip_address(lo)), int(ipaddress.ip_address(hi))
            self.excluded |= {ipaddress.ip_address(x) for x in range(a, b + 1)}
        self.bindings = {}            # mac -> (ip, expiry time)

    def free(self):
        used = {ip for ip, _ in self.bindings.values()}
        return [h for h in self.net.hosts() if h not in self.excluded and h not in used]

    def dora(self, mac, now):
        print(f"  DISCOVER  from {mac} (broadcast, src 0.0.0.0 -> 255.255.255.255, UDP 68->67)")
        if mac in self.bindings:
            ip = self.bindings[mac][0]
        else:
            pool = self.free()
            if not pool:
                print("  (no OFFER: pool exhausted - client falls back to APIPA 169.254.x.x)")
                return None
            ip = pool[0]
        print(f"  OFFER     {ip}/{self.net.prefixlen} gw {self.gateway} dns {self.dns} lease {self.lease_s}s")
        print(f"  REQUEST   {mac} asks for {ip} (broadcast, so other servers withdraw their offers)")
        self.bindings[mac] = (ip, now + self.lease_s)
        print(f"  ACK       {ip} bound to {mac}, renew (T1) at t={now + self.lease_s // 2}s")
        return ip

    def assign(self, mac, now):
        """Same result as DORA, without printing each message."""
        pool = self.free()
        if mac not in self.bindings and not pool:
            return None
        ip = self.bindings[mac][0] if mac in self.bindings else pool[0]
        self.bindings[mac] = (ip, now + self.lease_s)
        return ip

    def expire(self, now):
        gone = [m for m, (_, exp) in self.bindings.items() if exp <= now]
        for m in gone:
            print(f"  lease of {self.bindings[m][0]} for {m} expired and returned to the pool")
            del self.bindings[m]

    def show_bindings(self):
        print("  IP address       Client-ID/Hardware address   Lease expiration (t)")
        for mac, (ip, exp) in sorted(self.bindings.items(), key=lambda x: x[1][0]):
            print(f"  {str(ip):16} {mac:28} {exp}s")


if __name__ == "__main__":
    srv = DhcpServer("192.168.10.0/28", "192.168.10.1", "192.168.10.5", lease_s=3600,
                     excluded=[("192.168.10.1", "192.168.10.5")])
    print(f"Pool 192.168.10.0/28: {len(list(srv.net.hosts()))} hosts, 5 excluded -> {len(srv.free())} leasable\n")
    clients = [f"aaaa.bbbb.{i:04x}" for i in range(1, 12)]
    for t, mac in enumerate(clients[:3]):
        print(f"t={t}s"); srv.dora(mac, t); print()
    print("Bindings (like 'show ip dhcp binding'):"); srv.show_bindings()
    print("\nEight more clients arrive at t=10s")
    for m in clients[3:]:
        ip = srv.assign(m, 10)
        print(f"  {m} -> {ip if ip else 'NO ADDRESS (pool exhausted, client uses APIPA 169.254.x.x)'}")
    print("\nAt t=3601s the first leases expire:")
    srv.expire(3601)
    print(f"  free addresses now: {', '.join(map(str, srv.free()))}")
