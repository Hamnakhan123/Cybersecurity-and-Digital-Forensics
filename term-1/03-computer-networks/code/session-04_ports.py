"""Session 4 - Well-known ports: lookup, range classification and a
risk note for each service (what a defender should check).

Run:  python session-04_ports.py
"""

SERVICES = {
    20: ("FTP data", "TCP", "cleartext; prefer SFTP/FTPS"),
    21: ("FTP control", "TCP", "cleartext logins; prefer SFTP"),
    22: ("SSH / SFTP / SCP", "TCP", "use keys, disable root login"),
    23: ("Telnet", "TCP", "cleartext: replace with SSH"),
    25: ("SMTP", "TCP", "block outbound from PCs to stop spam bots"),
    53: ("DNS", "TCP/UDP", "UDP queries, TCP zone transfers: restrict AXFR"),
    67: ("DHCP server", "UDP", "enable DHCP snooping on switches"),
    68: ("DHCP client", "UDP", ""),
    69: ("TFTP", "UDP", "no authentication; lab/config use only"),
    80: ("HTTP", "TCP", "redirect to HTTPS"),
    110: ("POP3", "TCP", "use POP3S 995"),
    123: ("NTP", "UDP", "accurate time is essential for logs"),
    143: ("IMAP", "TCP", "use IMAPS 993"),
    161: ("SNMP", "UDP", "use SNMPv3; change 'public' community"),
    162: ("SNMP trap", "UDP", ""),
    389: ("LDAP", "TCP/UDP", "use LDAPS 636"),
    443: ("HTTPS", "TCP", "keep TLS 1.2+ only"),
    445: ("SMB", "TCP", "never expose to the internet"),
    514: ("Syslog", "UDP", "consider TLS syslog 6514"),
    636: ("LDAPS", "TCP", ""),
    993: ("IMAPS", "TCP", ""),
    995: ("POP3S", "TCP", ""),
    1433: ("MS SQL Server", "TCP", "never expose to the internet"),
    3306: ("MySQL", "TCP", "bind to localhost/app subnet"),
    3389: ("RDP", "TCP", "put behind VPN + MFA"),
    5060: ("SIP", "TCP/UDP", "VoIP signalling"),
}


def port_range(p: int) -> str:
    if 0 <= p <= 1023: return "well-known"
    if p <= 49151: return "registered"
    if p <= 65535: return "dynamic/ephemeral"
    return "invalid"


def audit(open_ports: list[int]) -> None:
    """Review a list of open ports found on one of YOUR lab hosts."""
    risky = {21, 23, 69, 445, 1433, 3306, 3389, 161}
    for p in sorted(open_ports):
        name, proto, note = SERVICES.get(p, ("unknown", "?", "identify the process using it"))
        flag = "REVIEW" if p in risky else "ok"
        print(f"  {p:>5}/{proto:<7} {name:<16} {port_range(p):<17} {flag:<6} {note}")


if __name__ == "__main__":
    print("Port ranges:")
    for p in (22, 443, 8080, 3389, 50000, 70000):
        print(f"  {p:>5} -> {port_range(p)}")
    print("\nAudit of lab server 'web01' (ports reported by the admin's own inventory):")
    audit([22, 80, 443, 3306, 23, 8080])
    secure_pairs = [(80, 443), (21, 22), (23, 22), (110, 995), (143, 993), (389, 636)]
    print("\nInsecure -> secure replacements:")
    for old, new in secure_pairs:
        print(f"  {SERVICES[old][0]:<12} {old:>4}  ->  {SERVICES[new][0]:<16} {new}")
