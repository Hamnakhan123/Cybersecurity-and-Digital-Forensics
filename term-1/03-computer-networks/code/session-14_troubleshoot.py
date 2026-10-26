"""Session 14 - The troubleshooting methodology as code: a bottom-up checker
that runs only SAFE, LOCAL checks on your own machine, plus a symptom ->
likely-cause lookup that follows the OSI layers.

Run:  python session-14_troubleshoot.py
"""
import socket
import ipaddress

SYMPTOMS = {
    "no link light":              (1, "cable unplugged/damaged, wrong port, NIC disabled"),
    "link up but 169.254.x.x ip": (3, "DHCP server unreachable: check VLAN, DHCP scope, relay"),
    "can ping ip but not name":   (7, "DNS server wrong or down: check resolver settings"),
    "slow and many crc errors":   (1, "bad cable, EMI, duplex mismatch"),
    "one vlan cannot reach others": (3, "missing inter-VLAN route or trunk not allowing VLAN"),
    "intermittent drop on wi-fi": (1, "interference, channel overlap, weak signal"),
    "website loads but not https": (4, "firewall blocks 443 or certificate problem"),
}


def step(name, ok, detail):
    print(f"  [{'OK ' if ok else 'BAD'}] {name:<34} {detail}")
    return ok


def local_checks():
    print("Bottom-up checks on this machine:")
    host = socket.gethostname()
    step("Host name", bool(host), host)
    try:
        lo = socket.gethostbyname("localhost")
        step("Loopback resolves (TCP/IP stack)", ipaddress.ip_address(lo).is_loopback, lo)
    except OSError as e:
        step("Loopback resolves (TCP/IP stack)", False, str(e))
    srv = socket.socket(); srv.bind(("127.0.0.1", 0)); srv.listen(1)
    port = srv.getsockname()[1]
    try:
        socket.create_connection(("127.0.0.1", port), timeout=1).close()
        step("TCP connect to local service", True, "handshake completed on 127.0.0.1")
    except OSError as e:
        step("TCP connect to local service", False, str(e))
    srv.close()
    try:
        socket.create_connection(("127.0.0.1", port), timeout=1).close()
        step("Same port after service stopped", True, "unexpected")
    except OSError:
        step("Same port after service stopped", False, "connection refused = nothing listening (Layer 4/7)")


def diagnose(symptom):
    layer, cause = SYMPTOMS[symptom]
    return f"Layer {layer}: {cause}"


if __name__ == "__main__":
    local_checks()
    print("\nSymptom -> where to start:")
    for s in SYMPTOMS:
        print(f"  {s:<30} {diagnose(s)}")
