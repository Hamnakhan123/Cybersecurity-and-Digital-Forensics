"""Session 15 - A REST API like a network controller's, running only on 127.0.0.1.

Starts a tiny mock controller with Python's http.server, then acts as a client:
- POST /api/v1/auth/token        -> get a token (like a controller login)
- GET  /api/v1/devices           -> inventory as JSON
- GET  /api/v1/devices/<name>    -> one device
- POST /api/v1/vlans             -> create a VLAN (validated, 201 Created)
- requests without a token get 401 Unauthorized
Nothing leaves your computer.
Run:  python session-15_rest_controller.py
"""
import json
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

TOKEN = "lab-token-123"
DEVICES = [{"hostname": "CORE-SW1", "role": "distribution", "ip": "192.168.99.2", "os": "IOS-XE 17.9", "reachable": True},
           {"hostname": "ACC-SW1", "role": "access", "ip": "192.168.99.11", "os": "IOS 15.2", "reachable": True},
           {"hostname": "EDGE-R1", "role": "border", "ip": "192.168.99.1", "os": "IOS-XE 17.6", "reachable": False}]
VLANS = {10: "LECTURERS", 20: "STUDENTS"}


class Controller(BaseHTTPRequestHandler):
    def log_message(self, *a):             # keep the output tidy
        pass

    def send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def authorised(self):
        return self.headers.get("X-Auth-Token") == TOKEN

    def do_GET(self):
        if not self.authorised():
            return self.send(401, {"error": "missing or invalid token"})
        if self.path == "/api/v1/devices":
            return self.send(200, {"response": DEVICES})
        if self.path.startswith("/api/v1/devices/"):
            name = self.path.rsplit("/", 1)[1]
            d = next((x for x in DEVICES if x["hostname"] == name), None)
            return self.send(200, {"response": d}) if d else self.send(404, {"error": "not found"})
        self.send(404, {"error": "no such endpoint"})

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if self.path == "/api/v1/auth/token":
            ok = body == {"username": "netops", "password": "lab-only"}
            return self.send(200, {"token": TOKEN}) if ok else self.send(401, {"error": "bad credentials"})
        if not self.authorised():
            return self.send(401, {"error": "missing or invalid token"})
        if self.path == "/api/v1/vlans":
            vid = body.get("id")
            if not isinstance(vid, int) or not 1 <= vid <= 4094:
                return self.send(400, {"error": "id must be 1-4094"})
            if vid in VLANS:
                return self.send(409, {"error": f"VLAN {vid} exists"})
            VLANS[vid] = body.get("name", f"VLAN{vid:04d}")
            return self.send(201, {"created": {"id": vid, "name": VLANS[vid]}})
        self.send(404, {"error": "no such endpoint"})


LOCAL = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # never route 127.0.0.1 via a proxy


def call(method, url, body=None, token=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json", **({"X-Auth-Token": token} if token else {})})
    try:
        with LOCAL.open(req, timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


if __name__ == "__main__":
    srv = HTTPServer(("127.0.0.1", 0), Controller)
    base = f"http://127.0.0.1:{srv.server_address[1]}/api/v1"
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    print("GET /devices without a token  ->", call("GET", base + "/devices"))
    code, tok = call("POST", base + "/auth/token", {"username": "netops", "password": "lab-only"})
    token = tok["token"]
    print("POST /auth/token              ->", code, "token received")
    code, data = call("GET", base + "/devices", token=token)
    print(f"GET /devices                  -> {code}, {len(data['response'])} devices")
    for d in data["response"]:
        print(f"   {d['hostname']:9} {d['role']:12} {d['ip']:14} {d['os']:12} {'UP' if d['reachable'] else 'UNREACHABLE'}")
    print("GET /devices/ACC-SW1          ->", call("GET", base + "/devices/ACC-SW1", token=token))
    print("POST /vlans {id: 30, LAB}     ->", call("POST", base + "/vlans", {"id": 30, "name": "LAB"}, token))
    print("POST /vlans {id: 30} again    ->", call("POST", base + "/vlans", {"id": 30, "name": "LAB"}, token))
    print("POST /vlans {id: 5000}        ->", call("POST", base + "/vlans", {"id": 5000}, token))
    srv.shutdown()
