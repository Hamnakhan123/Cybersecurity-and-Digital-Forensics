"""Session 2 - Map protocols, devices and PDUs to OSI and TCP/IP layers.

Also classifies example networks into PAN / LAN / CAN / MAN / WAN by their
span, which is the "types of area networks" part of the session.
Run:  python session-02_osi_mapper.py
"""

OSI = {7: "Application", 6: "Presentation", 5: "Session", 4: "Transport",
       3: "Network", 2: "Data Link", 1: "Physical"}
TCPIP = {7: "Application", 6: "Application", 5: "Application", 4: "Transport",
         3: "Internet", 2: "Network Access", 1: "Network Access"}
PDU = {7: "Data", 6: "Data", 5: "Data", 4: "Segment / Datagram", 3: "Packet", 2: "Frame", 1: "Bits"}

ITEMS = {"HTTP": 7, "DNS": 7, "SSH": 7, "TLS encryption": 6, "JPEG / ASCII": 6,
         "NetBIOS / RPC sessions": 5, "TCP": 4, "UDP": 4, "IPv4 / IPv6": 3, "ICMP (ping)": 3,
         "OSPF": 3, "Router": 3, "Ethernet / 802.3": 2, "Wi-Fi / 802.11": 2, "ARP": 2,
         "Switch": 2, "Hub / repeater": 1, "Cat6 cable / fibre": 1}


def area_type(span_m):
    if span_m <= 10: return "PAN"
    if span_m <= 1_000: return "LAN"
    if span_m <= 5_000: return "CAN"
    if span_m <= 50_000: return "MAN"
    return "WAN"


if __name__ == "__main__":
    print(f"{'Item':24} {'OSI layer':18} {'TCP/IP layer':15} PDU")
    for item, layer in ITEMS.items():
        print(f"{item:24} {str(layer) + ' ' + OSI[layer]:18} {TCPIP[layer]:15} {PDU[layer]}")
    print("\nArea network types by span")
    for name, span in [("Bluetooth earbuds to phone", 3), ("Computer lab", 60),
                       ("University campus, 6 buildings", 2_500), ("City-wide bank branches", 30_000),
                       ("Offices in Karachi and Islamabad", 1_150_000)]:
        print(f"  {name:36} {span:>9,} m  -> {area_type(span)}")
