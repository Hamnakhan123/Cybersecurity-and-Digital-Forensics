"""Session 4 - Sockets on localhost: how a port, a protocol and a service fit
together. Starts a tiny TCP echo service and a UDP time service on 127.0.0.1,
talks to them as a client, then checks which of a few local ports are open.

Lab-safe: everything stays on the loopback interface of your own machine.
Run:  python session-04_local_service.py
"""
import socket
import threading
import time

HOST = "127.0.0.1"


def tcp_echo_server(sock: socket.socket) -> None:
    conn, addr = sock.accept()                  # 3-way handshake already done
    with conn:
        data = conn.recv(1024)
        conn.sendall(b"ECHO: " + data)


def udp_time_server(sock: socket.socket) -> None:
    data, addr = sock.recvfrom(1024)            # no connection, just a datagram
    sock.sendto(b"TIME 12:00:00", addr)


def is_open(port: int) -> bool:
    """TCP connect check, the same thing a firewall test does. Local only."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex((HOST, port)) == 0


if __name__ == "__main__":
    # --- TCP: connection-oriented, reliable, ordered ---
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp.bind((HOST, 0))                          # 0 = let the OS pick a free port
    tcp.listen(1)
    tcp_port = tcp.getsockname()[1]
    threading.Thread(target=tcp_echo_server, args=(tcp,), daemon=True).start()

    with socket.create_connection((HOST, tcp_port)) as c:
        local = c.getsockname()[1]
        c.sendall(b"hello over TCP")
        reply = c.recv(1024).decode()
    print(f"TCP  client port {local} is {'ephemeral' if local > 1023 else 'low'}; "
          f"server port is in the dynamic range")
    print(f"TCP  reply: {reply}")

    # --- UDP: connectionless, best-effort ---
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((HOST, 0))
    udp_port = udp.getsockname()[1]
    threading.Thread(target=udp_time_server, args=(udp,), daemon=True).start()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as u:
        u.settimeout(1)
        u.sendto(b"what time?", (HOST, udp_port))
        print(f"UDP  reply: {u.recvfrom(1024)[0].decode()}")

    # --- Which local ports are listening? Start one more listener to compare ---
    extra = socket.socket(); extra.bind((HOST, 0)); extra.listen(1)
    listening = extra.getsockname()[1]
    time.sleep(0.1)
    closed = listening + 1 if listening < 65535 else listening - 1
    for p in (listening, closed):
        print(f"Port {'<listening port>' if p == listening else '<next port>'}: "
              f"{'OPEN' if is_open(p) else 'closed (connection refused)'}")
    extra.close(); tcp.close(); udp.close()
