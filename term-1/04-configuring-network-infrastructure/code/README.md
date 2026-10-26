# 💻 Code · Module 4: Configuring Network Infrastructure

> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Every file below is complete and runnable on its own. Each one is used by a session page, which shows the real output it produced.

[⬅ Back to the module](../README.md)

## ⚙️ Setup

- Python 3.10 or newer; only the standard library is used, so there is nothing to install.
- Run every command from inside this `code/` folder so relative data paths resolve (on Colab, scripts fetch their data files from this repository).
- `.ios` files are Cisco IOS configurations: open the router/switch **CLI** tab in Cisco Packet Tracer and type them in. Lines starting with `!` are comments.
- The shell script needs `bash` and `openssl` (Linux, macOS, WSL, or `!bash file.sh` on Colab).
- Network examples talk only to `127.0.0.1` or use recorded lab data; addresses are private or documentation ranges.
- Prefer the browser? Each session's notebook (`.ipynb`) opens in Google Colab with one click.

## 📂 Files

### [Session 1: Fundamentals of Networking](../session-01-fundamentals-of-networking.md)

| File | What it does | How to run |
|---|---|---|
| [`session-01_delay_calc.py`](session-01_delay_calc.py) | Measure what makes a network "good": delay, throughput and availability. | `python session-01_delay_calc.py` |
| [`session-01_device_roles.py`](session-01_device_roles.py) | Pick the right device for each networking job. | `python session-01_device_roles.py` |
| [`session-01-fundamentals-of-networking.ipynb`](session-01-fundamentals-of-networking.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-01-fundamentals-of-networking.ipynb) |

### [Session 2: Models in Computer Networking: OSI and TCP/IP](../session-02-osi-and-tcpip-models.md)

| File | What it does | How to run |
|---|---|---|
| [`session-02_encapsulate.py`](session-02_encapsulate.py) | Encapsulation with real header bytes: Ethernet / IPv4 / TCP. | `python session-02_encapsulate.py` |
| [`session-02_osi_mapper.py`](session-02_osi_mapper.py) | Map protocols, devices and PDUs to OSI and TCP/IP layers. | `python session-02_osi_mapper.py` |
| [`session-02-osi-and-tcpip-models.ipynb`](session-02-osi-and-tcpip-models.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-02-osi-and-tcpip-models.ipynb) |

### [Session 3: Types of Addresses: MAC, IP, Subnetting and CIDR](../session-03-mac-ip-subnetting-cidr.md)

| File | What it does | How to run |
|---|---|---|
| [`session-03_cidr_planner.py`](session-03_cidr_planner.py) | Subnetting, VLSM and CIDR summarisation with the ipaddress module. | `python session-03_cidr_planner.py` |
| [`session-03_mac_tool.py`](session-03_mac_tool.py) | MAC address anatomy: OUI, unicast/multicast and local/universal bits. | `python session-03_mac_tool.py` |
| [`session-03-mac-ip-subnetting-cidr.ipynb`](session-03-mac-ip-subnetting-cidr.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-03-mac-ip-subnetting-cidr.ipynb) |

### [Session 4: Hardware and Software of Cisco Devices](../session-04-cisco-hardware-and-ios.md)

| File | What it does | How to run |
|---|---|---|
| [`session-04_config_audit.py`](session-04_config_audit.py) | Read a Cisco IOS running-config and audit it like an engineer. | `python session-04_config_audit.py` |
| [`session-04_first_config.ios`](session-04_first_config.ios) | First configuration of a Cisco switch/router (Cisco Packet Tracer lab) | Type into the device CLI in Cisco Packet Tracer |
| [`session-04_running-config.txt`](session-04_running-config.txt) | Sample branch-router configuration audited by the script. | Input data read by the audit script |
| [`session-04-cisco-hardware-and-ios.ipynb`](session-04-cisco-hardware-and-ios.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-04-cisco-hardware-and-ios.ipynb) |

### [Session 5: Introduction to Switching and VLANs](../session-05-switching-and-vlans.md)

| File | What it does | How to run |
|---|---|---|
| [`session-05_dtp_matrix.py`](session-05_dtp_matrix.py) | Will this link become a trunk? The DTP negotiation matrix. | `python session-05_dtp_matrix.py` |
| [`session-05_switch_sim.py`](session-05_switch_sim.py) | How a Layer 2 switch learns, floods, forwards and filters, per VLAN. | `python session-05_switch_sim.py` |
| [`session-05_vlans.ios`](session-05_vlans.ios) | VLANs, access ports and an 802.1Q trunk (Cisco Packet Tracer lab) | Type into the device CLI in Cisco Packet Tracer |
| [`session-05-switching-and-vlans.ipynb`](session-05-switching-and-vlans.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-05-switching-and-vlans.ipynb) |

### [Session 6: Loop Avoidance: STP, BPDU Guard and EtherChannel](../session-06-stp-and-etherchannel.md)

| File | What it does | How to run |
|---|---|---|
| [`session-06_etherchannel.py`](session-06_etherchannel.py) | EtherChannel: which modes form a bundle, and how traffic is shared. | `python session-06_etherchannel.py` |
| [`session-06_stp_election.py`](session-06_stp_election.py) | Spanning Tree Protocol: root bridge, root ports and blocked ports. | `python session-06_stp_election.py` |
| [`session-06_stp_etherchannel.ios`](session-06_stp_etherchannel.ios) | Spanning tree tuning, edge protection and LACP EtherChannel (lab) | Type into the device CLI in Cisco Packet Tracer |
| [`session-06-stp-and-etherchannel.ipynb`](session-06-stp-and-etherchannel.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-06-stp-and-etherchannel.ipynb) |

### [Session 7: Routing Technologies: Static Routes and OSPF](../session-07-routing-static-and-ospf.md)

| File | What it does | How to run |
|---|---|---|
| [`session-07_route_lookup.py`](session-07_route_lookup.py) | How a router chooses a route: longest prefix, then AD, then metric. | `python session-07_route_lookup.py` |
| [`session-07_static_and_ospf.ios`](session-07_static_and_ospf.ios) | Static, default, floating static and OSPF (single and multi-area) - lab only | Type into the device CLI in Cisco Packet Tracer |
| [`session-07-routing-static-and-ospf.ipynb`](session-07-routing-static-and-ospf.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-07-routing-static-and-ospf.ipynb) |

### [Session 8: First Hop Redundancy: HSRP, VRRP and GLBP](../session-08-first-hop-redundancy.md)

| File | What it does | How to run |
|---|---|---|
| [`session-08_fhrp_sim.py`](session-08_fhrp_sim.py) | First Hop Redundancy: HSRP election, failover and GLBP load sharing. | `python session-08_fhrp_sim.py` |
| [`session-08_hsrp.ios`](session-08_hsrp.ios) | HSRP v2 with preemption and tracking, plus VRRP and GLBP equivalents (lab) | Type into the device CLI in Cisco Packet Tracer |
| [`session-08-first-hop-redundancy.ipynb`](session-08-first-hop-redundancy.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-08-first-hop-redundancy.ipynb) |

### [Session 9: Protocols for Network Management: NTP, DHCP, DNS, TFTP](../session-09-network-management-protocols.md)

| File | What it does | How to run |
|---|---|---|
| [`session-09_dhcp_pool.py`](session-09_dhcp_pool.py) | A DHCP server's view: pool, exclusions, DORA and leases. | `python session-09_dhcp_pool.py` |
| [`session-09_dns_ntp.py`](session-09_dns_ntp.py) | Look inside DNS, NTP and TFTP messages (built and parsed offline). | `python session-09_dns_ntp.py` |
| [`session-09_services.ios`](session-09_services.ios) | NTP, DHCP, DNS and TFTP on Cisco IOS (lab only) | Type into the device CLI in Cisco Packet Tracer |
| [`session-09-network-management-protocols.ipynb`](session-09-network-management-protocols.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-09-network-management-protocols.ipynb) |

### [Session 10: Network Security Fundamentals: ACLs and DHCP Snooping](../session-10-network-security-fundamentals.md)

| File | What it does | How to run |
|---|---|---|
| [`session-10_acl_engine.py`](session-10_acl_engine.py) | Evaluate Cisco-style ACLs exactly as a router does. | `python session-10_acl_engine.py` |
| [`session-10_certificate_lab.sh`](session-10_certificate_lab.sh) | Digital certificates in a lab: a private CA signs a device certificate. | `bash session-10_certificate_lab.sh` |
| [`session-10_dhcp_snooping.py`](session-10_dhcp_snooping.py) | DHCP snooping: stop rogue DHCP servers and build the binding table. | `python session-10_dhcp_snooping.py` |
| [`session-10_security.ios`](session-10_security.ios) | ACLs, DHCP snooping, DAI and port security (Cisco Packet Tracer lab) | Type into the device CLI in Cisco Packet Tracer |
| [`session-10-network-security-fundamentals.ipynb`](session-10-network-security-fundamentals.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-10-network-security-fundamentals.ipynb) |

### [Session 11: IPv6](../session-11-ipv6.md)

| File | What it does | How to run |
|---|---|---|
| [`session-11_ipv6.ios`](session-11_ipv6.ios) | IPv6 addressing, SLAAC/DHCPv6, static routes and OSPFv3 (lab only) | Type into the device CLI in Cisco Packet Tracer |
| [`session-11_ipv6_toolkit.py`](session-11_ipv6_toolkit.py) | IPv6 toolkit: notation, address types, SLAAC and NDP multicast. | `python session-11_ipv6_toolkit.py` |
| [`session-11-ipv6.ipynb`](session-11-ipv6.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-11-ipv6.ipynb) |

### [Session 12: Layer 3 Switches and Inter-VLAN Routing](../session-12-layer-3-switching.md)

| File | What it does | How to run |
|---|---|---|
| [`session-12_intervlan_cef.py`](session-12_intervlan_cef.py) | Inter-VLAN routing on a Layer 3 switch, and how CEF forwards fast. | `python session-12_intervlan_cef.py` |
| [`session-12_l3switch.ios`](session-12_l3switch.ios) | Inter-VLAN routing: router-on-a-stick vs Layer 3 switch SVIs (lab) | Type into the device CLI in Cisco Packet Tracer |
| [`session-12-layer-3-switching.ipynb`](session-12-layer-3-switching.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-12-layer-3-switching.ipynb) |

### [Session 13: Virtual Private Networks](../session-13-virtual-private-networks.md)

| File | What it does | How to run |
|---|---|---|
| [`session-13_ipsec_concepts.py`](session-13_ipsec_concepts.py) | The security building blocks of a VPN, shown with real primitives. | `python session-13_ipsec_concepts.py` |
| [`session-13_site_to_site.ios`](session-13_site_to_site.ios) | Site-to-site VPN: GRE tunnel protected by IPsec (IKEv2), lab addresses only | Type into the device CLI in Cisco Packet Tracer |
| [`session-13_vpn_overhead.py`](session-13_vpn_overhead.py) | VPN tunnels cost bytes: overhead, MTU and TCP MSS. | `python session-13_vpn_overhead.py` |
| [`session-13-virtual-private-networks.ipynb`](session-13-virtual-private-networks.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-13-virtual-private-networks.ipynb) |

### [Session 14: Wireless Technologies and WLAN Configuration](../session-14-wireless-lan-configuration.md)

| File | What it does | How to run |
|---|---|---|
| [`session-14_wlan_audit.py`](session-14_wlan_audit.py) | Audit WLAN profiles and estimate signal strength at a desk. | `python session-14_wlan_audit.py` |
| [`session-14_wlan_setup.txt`](session-14_wlan_setup.txt) | Step-by-step WLAN configuration checklist (controller, VLANs, security, RF). | Read and follow |
| [`session-14-wireless-lan-configuration.ipynb`](session-14-wireless-lan-configuration.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-14-wireless-lan-configuration.ipynb) |

### [Session 15: Automation and Network Programmability](../session-15-automation-and-programmability.md)

| File | What it does | How to run |
|---|---|---|
| [`session-15_automation.py`](session-15_automation.py) | Network automation with JSON, templates and configuration drift checks. | `python session-15_automation.py` |
| [`session-15_inventory.json`](session-15_inventory.json) | Source-of-truth data (VLANs, switches) used by the automation script. | Data file read by the session's script |
| [`session-15_rest_controller.py`](session-15_rest_controller.py) | A REST API like a network controller's, running only on 127.0.0.1. | `python session-15_rest_controller.py` |
| [`session-15-automation-and-programmability.ipynb`](session-15-automation-and-programmability.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/04-configuring-network-infrastructure/code/session-15-automation-and-programmability.ipynb) |

## 🧩 Mini project

| File | What it does | How to run |
|---|---|---|
| [`mini_project_campus_builder.py`](mini_project_campus_builder.py) | Campus network builder: from intent to device configs. Walked through in [Session 15](../session-15-automation-and-programmability.md). | `python mini_project_campus_builder.py` |

---

<sub>Prepared by Hamna Zahid Khan, Junior Lecturer · Cybersecurity and Digital Forensics</sub>
