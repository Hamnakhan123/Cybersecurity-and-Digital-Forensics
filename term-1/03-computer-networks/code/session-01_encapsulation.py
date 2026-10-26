"""Session 1 - Encapsulation through the TCP/IP and OSI layers (simulation).

Shows how application data gains a header at each layer on the way DOWN the
sending stack, and loses it again on the way UP the receiving stack.
Nothing is sent on a real network: it is a teaching model only.
Run:  python session-01_encapsulation.py
"""

# Each layer: (OSI number, OSI name, PDU name, header added by that layer)
LAYERS = [
    (7, "Application",  "Data",    "HTTP: GET /index.html"),
    (6, "Presentation", "Data",    "TLS: encrypted record"),
    (5, "Session",      "Data",    "Session id=42"),
    (4, "Transport",    "Segment", "TCP: src=50123 dst=443 seq=1"),
    (3, "Network",      "Packet",  "IP: 10.0.0.5 -> 93.184.216.34 TTL=64"),
    (2, "Data Link",    "Frame",   "ETH: aa:aa:aa:00:00:01 -> bb:bb:bb:00:00:fe"),
    (1, "Physical",     "Bits",    "signal on the wire"),
]


def encapsulate(payload: str) -> list[str]:
    """Wrap the payload in one header per layer, top (7) to bottom (1)."""
    stack = [payload]
    unit = payload
    for num, name, pdu, header in LAYERS:
        if num == 1:                       # physical layer turns the frame into bits
            size = len(unit)
            unit = f"010110... (the {size}-character frame sent as signals)"
        else:
            unit = f"[{header}] {unit}"
            size = len(unit)
        stack.append(unit)
        print(f"L{num} {name:<12} PDU={pdu:<8} size={size:>3}  {unit[:60]}")
    return stack


def decapsulate(stack: list[str]) -> str:
    """Receiver reads from the bottom up, removing one header per layer."""
    print("\nReceiver strips headers bottom-up:")
    for (num, name, pdu, header), unit in zip(reversed(LAYERS), reversed(stack[1:])):
        print(f"L{num} {name:<12} reads its header -> passes {pdu.lower()} up")
    return stack[0]


if __name__ == "__main__":
    data = "Hello, lab server!"
    print("Sender encapsulates top-down:")
    s = encapsulate(data)
    delivered = decapsulate(s)
    overhead = len(s[-2]) - len(data)
    print(f"\nDelivered to the application: {delivered!r}")
    print(f"Header overhead before the wire: {overhead} characters "
          f"for {len(data)} characters of real data ({overhead / len(data):.0%})")
