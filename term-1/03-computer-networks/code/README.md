# 💻 Code · Module 3: Technologies of Computer Networks

> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Every file below is complete and runnable on its own. Each one is used by a session page, which shows the real output it produced.

[⬅ Back to the module](../README.md)

## ⚙️ Setup

- Python 3.10 or newer; only the standard library is used, so there is nothing to install.
- Run every command from inside this `code/` folder so relative data paths resolve.
- Socket examples only talk to `127.0.0.1` (your own computer). Log and capture examples use recorded lab data.
- `.ios` files are Cisco IOS configurations: open the router/switch **CLI** tab in Cisco Packet Tracer and type them in.
- Prefer the browser? Each session's notebook (`.ipynb`) opens in Google Colab with one click.

## 📂 Files

### [Session 1: Basic Concepts of a Network](../session-01-basic-network-concepts.md)

| File | What it does | How to run |
|---|---|---|
| [`session-01_encapsulation.py`](session-01_encapsulation.py) | Encapsulation through the TCP/IP and OSI layers (simulation). | `python session-01_encapsulation.py` |
| [`session-01_topology.py`](session-01_topology.py) | Compare network topologies by cable count and fault tolerance. | `python session-01_topology.py` |
| [`session-01-basic-network-concepts.ipynb`](session-01-basic-network-concepts.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-01-basic-network-concepts.ipynb) |

### [Session 2: Network Cables, Connectors and Wiring Standards](../session-02-cables-connectors-wiring.md)

| File | What it does | How to run |
|---|---|---|
| [`session-02_cable_selector.py`](session-02_cable_selector.py) | Choose a cable type for a link from distance, speed and environment. | `python session-02_cable_selector.py` |
| [`session-02_wiremap.py`](session-02_wiremap.py) | T568A / T568B pin maps and a simulated cable wire-map tester. | `python session-02_wiremap.py` |
| [`session-02-cables-connectors-wiring.ipynb`](session-02-cables-connectors-wiring.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-02-cables-connectors-wiring.ipynb) |

### [Session 3: IP Addressing](../session-03-ip-addressing.md)

| File | What it does | How to run |
|---|---|---|
| [`session-03_ipv6.py`](session-03_ipv6.py) | IPv6 essentials: compress/expand, address types and EUI-64. | `python session-03_ipv6.py` |
| [`session-03_subnet_calc.py`](session-03_subnet_calc.py) | IPv4 subnet calculator, done by hand with bits AND checked against Python's standard `ipaddress` module. | `python session-03_subnet_calc.py` |
| [`session-03-ip-addressing.ipynb`](session-03-ip-addressing.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-03-ip-addressing.ipynb) |

### [Session 4: Common Ports, Protocols and Services](../session-04-ports-protocols-services.md)

| File | What it does | How to run |
|---|---|---|
| [`session-04_local_service.py`](session-04_local_service.py) | Sockets on localhost: how a port, a protocol and a service fit together. Starts a tiny TCP echo service and a UDP time service on 127.0.0.1, talks to them as a client, then checks which of a few local ports are open. | `python session-04_local_service.py` |
| [`session-04_ntp_offset.py`](session-04_ntp_offset.py) | How NTP works out the clock offset and the round-trip delay from four timestamps, and why log timestamps go wrong when clocks drift. | `python session-04_ntp_offset.py` |
| [`session-04_ports.py`](session-04_ports.py) | Well-known ports: lookup, range classification and a risk note for each service (what a defender should check). | `python session-04_ports.py` |
| [`session-04-ports-protocols-services.ipynb`](session-04-ports-protocols-services.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-04-ports-protocols-services.ipynb) |

### [Session 5: Corporate, Data Centre Network and Cloud Architecture](../session-05-datacentre-and-cloud.md)

| File | What it does | How to run |
|---|---|---|
| [`session-05_spine_leaf.py`](session-05_spine_leaf.py) | Size a data-centre network: three-tier vs spine-leaf. | `python session-05_spine_leaf.py` |
| [`session-05_storage_cloud.py`](session-05_storage_cloud.py) | Storage and cloud maths: RAID usable capacity, SAN vs NAS vs DAS, and a simple on-premises vs public-cloud cost comparison over 3 years. | `python session-05_storage_cloud.py` |
| [`session-05-datacentre-and-cloud.ipynb`](session-05-datacentre-and-cloud.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-05-datacentre-and-cloud.ipynb) |

### [Session 6: Network Devices, Components and Packet Tracer](../session-06-network-devices-packet-tracer.md)

| File | What it does | How to run |
|---|---|---|
| [`session-06_basic_router.ios`](session-06_basic_router.ios) | First configuration of a router in Cisco Packet Tracer (lab only) | Type into the device CLI in Cisco Packet Tracer |
| [`session-06_routing_table.py`](session-06_routing_table.py) | How a router picks a route: longest-prefix match, then administrative distance, then metric. | `python session-06_routing_table.py` |
| [`session-06_switch_vs_hub.py`](session-06_switch_vs_hub.py) | Why switches replaced hubs: simulate MAC-address learning. | `python session-06_switch_vs_hub.py` |
| [`session-06-network-devices-packet-tracer.ipynb`](session-06-network-devices-packet-tracer.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-06-network-devices-packet-tracer.ipynb) |

### [Session 7: Dynamic Routing: RIP, OSPF and EIGRP](../session-07-dynamic-routing.md)

| File | What it does | How to run |
|---|---|---|
| [`session-07_dynamic_routing.ios`](session-07_dynamic_routing.ios) | RIPv2, OSPF and EIGRP on router R1 (Cisco Packet Tracer lab) | Type into the device CLI in Cisco Packet Tracer |
| [`session-07_ospf_dijkstra.py`](session-07_ospf_dijkstra.py) | Link-state routing (OSPF) simulated with Dijkstra's algorithm. | `python session-07_ospf_dijkstra.py` |
| [`session-07_rip_bellman_ford.py`](session-07_rip_bellman_ford.py) | Distance-vector routing (RIP) simulated with Bellman-Ford. | `python session-07_rip_bellman_ford.py` |
| [`session-07-dynamic-routing.ipynb`](session-07-dynamic-routing.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-07-dynamic-routing.ipynb) |

### [Session 8: LAN Switching Technologies](../session-08-lan-switching.md)

| File | What it does | How to run |
|---|---|---|
| [`session-08_arp_watch.py`](session-08_arp_watch.py) | ARP cache behaviour and a defensive ARP-spoofing detector. | `python session-08_arp_watch.py` |
| [`session-08_dot1q.py`](session-08_dot1q.py) | Build and read an IEEE 802.1Q (VLAN) tagged Ethernet header. | `python session-08_dot1q.py` |
| [`session-08_vlan_trunk.ios`](session-08_vlan_trunk.ios) | VLANs, access ports, a trunk and Dynamic ARP Inspection on switch SW1 | Type into the device CLI in Cisco Packet Tracer |
| [`session-08-lan-switching.ipynb`](session-08-lan-switching.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-08-lan-switching.ipynb) |

### [Session 9: Wireless Technologies](../session-09-wireless-technologies.md)

| File | What it does | How to run |
|---|---|---|
| [`session-09_wifi_planner.py`](session-09_wifi_planner.py) | Wi-Fi planning maths: 2.4 GHz channel overlap, free-space path loss and a simple link budget for an access point. | `python session-09_wifi_planner.py` |
| [`session-09_wpa2_psk.py`](session-09_wpa2_psk.py) | Why WPA2-Personal needs a long passphrase. | `python session-09_wpa2_psk.py` |
| [`session-09-wireless-technologies.ipynb`](session-09-wireless-technologies.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-09-wireless-technologies.ipynb) |

### [Session 10: Network Availability and Monitoring](../session-10-network-availability.md)

| File | What it does | How to run |
|---|---|---|
| [`session-10_logging.ios`](session-10_logging.ios) | Send device logs to a central syslog server and keep time accurate | Type into the device CLI in Cisco Packet Tracer |
| [`session-10_metrics.py`](session-10_metrics.py) | Network performance metrics from ping-style samples: latency, jitter, packet loss, throughput/utilisation and the meaning of "nines". | `python session-10_metrics.py` |
| [`session-10_syslog_monitor.py`](session-10_syslog_monitor.py) | A tiny syslog collector on localhost plus a log analyser. | `python session-10_syslog_monitor.py` |
| [`session-10-network-availability.ipynb`](session-10-network-availability.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-10-network-availability.ipynb) |

### [Session 11: Policies and Procedures](../session-11-policies-and-procedures.md)

| File | What it does | How to run |
|---|---|---|
| [`session-11_hardened.ios`](session-11_hardened.ios) | The audited device after remediation (compare with session-11_router.cfg) | Type into the device CLI in Cisco Packet Tracer |
| [`session-11_password_policy.py`](session-11_password_policy.py) | Check passwords against an acceptable-use / password policy and estimate their strength. Modern guidance (e.g. NIST SP 800-63B) favours length and a block-list over forced complexity and frequent changes. Run: python session-11_password_policy.py | `python session-11_password_policy.py` |
| [`session-11_policy_audit.py`](session-11_policy_audit.py) | Audit a switch/router configuration against a hardening policy. | `python session-11_policy_audit.py` |
| [`session-11_router.cfg`](session-11_router.cfg) | Lab device: branch-r1 (fictional configuration for the audit exercise) | Input data read by the audit script |
| [`session-11-policies-and-procedures.ipynb`](session-11-policies-and-procedures.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-11-policies-and-procedures.ipynb) |

### [Session 12: High Availability and Disaster Recovery](../session-12-high-availability-dr.md)

| File | What it does | How to run |
|---|---|---|
| [`session-12_availability.py`](session-12_availability.py) | High-availability maths: MTBF/MTTR, components in series versus in parallel (redundancy), and RPO/RTO for backup strategies. | `python session-12_availability.py` |
| [`session-12-high-availability-dr.ipynb`](session-12-high-availability-dr.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-12-high-availability-dr.ipynb) |

### [Session 13: Network Security](../session-13-network-security.md)

| File | What it does | How to run |
|---|---|---|
| [`session-13_firewall_acl.py`](session-13_firewall_acl.py) | A first-match packet-filter (ACL / firewall rule) evaluator. | `python session-13_firewall_acl.py` |
| [`session-13_ids_detect.py`](session-13_ids_detect.py) | Simple intrusion-detection rules over a connection log. | `python session-13_ids_detect.py` |
| [`session-13-network-security.ipynb`](session-13-network-security.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-13-network-security.ipynb) |

### [Session 14: Network Troubleshooting](../session-14-network-troubleshooting.md)

| File | What it does | How to run |
|---|---|---|
| [`session-14_troubleshoot.py`](session-14_troubleshoot.py) | The troubleshooting methodology as code: a bottom-up checker that runs only SAFE, LOCAL checks on your own machine, plus a symptom -> likely-cause lookup that follows the OSI layers. | `python session-14_troubleshoot.py` |
| [`session-14-network-troubleshooting.ipynb`](session-14-network-troubleshooting.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/03-computer-networks/code/session-14-network-troubleshooting.ipynb) |

## 🧩 Mini project

| File | What it does | How to run |
|---|---|---|
| [`mini_project_netplan.py`](mini_project_netplan.py) | "Campus Branch Network Planner". Walked through in [Session 14](../session-14-network-troubleshooting.md). | `python mini_project_netplan.py` |

---

<sub>Prepared by Hamna Zahid Khan, Junior Lecturer · Cybersecurity and Digital Forensics</sub>
