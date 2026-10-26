# Module 3 Practice Test: Technologies of Computer Networks

> [Cybersecurity and Digital Forensics](../../README.md) › [Term 1](../README.md) › [Module 3](README.md) › **Practice Test**

| ⬅ [Last session](session-14-network-troubleshooting.md) | [Module overview](README.md) ➡ |
|:---|---:|

Answer every question first, then open the hidden answers to check yourself. Aim for 16/20 or better before moving on.

---

## Part A: Multiple-choice questions

**1.** At which OSI layer does a switch normally forward traffic?
A) Layer 1 B) Layer 2 C) Layer 3 D) Layer 4

**2.** How many links does a full mesh of 6 routers need?
A) 6 B) 12 C) 15 D) 30

**3.** What is the maximum length of a standard twisted-pair Ethernet channel?
A) 55 m B) 90 m C) 100 m D) 185 m

**4.** A cable has T568A on one end and T568B on the other. It is a:
A) straight-through cable B) crossover cable C) rollover cable D) coaxial cable

**5.** How many usable hosts does `192.168.10.0/27` provide?
A) 32 B) 30 C) 62 D) 14

**6.** What is the broadcast address of `172.16.45.200/20`?
A) 172.16.45.255 B) 172.16.47.255 C) 172.16.63.255 D) 172.16.32.255

**7.** A laptop shows the address `169.254.20.7`. The most likely cause is:
A) a DNS failure B) the DHCP server could not be reached C) a duplex mismatch D) an expired certificate

**8.** Which IPv6 address type is never routed beyond the local link?
A) 2001:db8::1 B) fd00::1 C) fe80::1 D) ff02::1 used across the internet

**9.** Which port and transport does NTP use?
A) TCP 123 B) UDP 123 C) UDP 161 D) TCP 514

**10.** Which IPsec component provides encryption?
A) AH B) ESP C) IKE D) SPI

**11.** In a spine-leaf fabric, leaf switches connect to:
A) each other only B) every spine switch C) one spine only D) the access layer

**12.** In IaaS, who is responsible for patching the guest operating system?
A) the cloud provider B) the customer C) the ISP D) nobody

**13.** A router has routes to `10.0.0.0/8` via OSPF and `10.1.0.0/16` via RIP. For destination `10.1.4.4` it uses:
A) the OSPF route because AD 110 < 120 B) the RIP route because it is the longest prefix C) both equally D) the default route

**14.** OSPF calculates the best path using:
A) Bellman-Ford B) DUAL C) Dijkstra's shortest path first D) hop count only

**15.** On a trunk, frames belonging to the native VLAN are:
A) tagged with VLAN 1 B) sent untagged C) dropped D) encrypted

**16.** Which switch feature drops ARP replies that do not match the DHCP snooping binding table?
A) BPDU Guard B) Port security C) Dynamic ARP Inspection D) VTP

**17.** Which Wi-Fi security option is recommended for a company with user accounts?
A) WEP B) WPA2-PSK with a shared password C) WPA3-Enterprise with 802.1X D) open network with hidden SSID

**18.** A syslog message has PRI 187. What is its severity?
A) 2 Critical B) 3 Error C) 4 Warning D) 7 Debug

**19.** Which backup scheme needs the last full backup plus **every** later backup to restore?
A) Full only B) Incremental C) Differential D) Snapshot

**20.** A packet matches no rule in a Cisco ACL. What happens?
A) It is permitted B) It is denied by the implicit deny C) It is logged and permitted D) The router reloads the ACL

<details>
<summary>✅ Show answers</summary>

| Q | Answer | Why |
|---|---|---|
| 1 | B | Switches use MAC addresses (data link) |
| 2 | C | 6 × 5 / 2 = 15 |
| 3 | C | 90 m permanent link + 10 m patch cords |
| 4 | B | A + B swaps pairs 1↔3 and 2↔6 |
| 5 | B | 2⁵ − 2 = 30 |
| 6 | B | /20 block in 3rd octet = 16 → 32–47 |
| 7 | B | APIPA is self-assigned when DHCP fails |
| 8 | C | fe80::/10 is link-local |
| 9 | B | NTP is UDP 123 |
| 10 | B | ESP encrypts; AH only authenticates |
| 11 | B | Every leaf connects to every spine |
| 12 | B | Shared responsibility: the customer manages the OS in IaaS |
| 13 | B | Longest prefix match is checked before administrative distance |
| 14 | C | OSPF is link state using SPF (Dijkstra) |
| 15 | B | The native VLAN is untagged |
| 16 | C | DAI validates ARP against DHCP snooping bindings |
| 17 | C | Per-user authentication, revocation, certificate validation |
| 18 | B | 187 = 23 × 8 + 3 → local7, severity 3 (Error) |
| 19 | B | Incremental chains every backup since the full |
| 20 | B | Every ACL ends with an implicit deny |
</details>

## Part B: Scenario questions

**Scenario 1 – Addressing a new branch.**
A branch receives `10.50.0.0/23`. It needs Staff (180 hosts), Lab (90 hosts), Guest Wi-Fi (40 hosts), Printers/IoT (12 hosts) and two router-to-router links. Design the VLSM plan (subnet, mask, gateway, broadcast) and say how much address space remains.

<details>
<summary>✅ Model answer</summary>

Largest first:

| Segment | Hosts | Prefix | Subnet | Gateway | Broadcast |
|---|---|---|---|---|---|
| Staff | 180 | /24 (254) | 10.50.0.0/24 | 10.50.0.1 | 10.50.0.255 |
| Lab | 90 | /25 (126) | 10.50.1.0/25 | 10.50.1.1 | 10.50.1.127 |
| Guest Wi-Fi | 40 | /26 (62) | 10.50.1.128/26 | 10.50.1.129 | 10.50.1.191 |
| Printers/IoT | 12 | /28 (14) | 10.50.1.192/28 | 10.50.1.193 | 10.50.1.207 |
| Link 1 | 2 | /30 | 10.50.1.208/30 | .209 – .210 | .211 |
| Link 2 | 2 | /30 | 10.50.1.212/30 | .213 – .214 | .215 |

Remaining: 10.50.1.216/29, 10.50.1.224/27 = 40 addresses. Put each segment in its own VLAN; isolate Guest Wi-Fi with an ACL (internet only). Verify no overlaps with Python `ipaddress` (`a.overlaps(b)`).
</details>

**Scenario 2 – "The network is slow and people lose connection."**
A design studio's users say file transfers are slow and their Wi-Fi drops every few minutes. Findings: the uplink from the access switch shows thousands of CRC errors and late collisions; the switch port is set to 100 Mbps full duplex while the server NIC auto-negotiated half duplex; the 2.4 GHz AP is on channel 3 with 40 MHz width; logs show repeated deauthentication frames from an unknown MAC address. Describe your troubleshooting steps and fixes.

<details>
<summary>✅ Model answer</summary>

1. **Identify** – gather symptoms and recent changes; separate the wired and wireless problems and handle them one at a time.
2. **Wired (bottom-up):** CRC errors + late collisions point to Layer 1/2. Fix the **duplex mismatch** (set both ends to auto/auto or the same fixed speed/duplex); test/replace the cable with a certifier; recheck counters (`clear counters`, then `show interfaces` after an hour – errors should stay at 0).
3. **Wireless:** move 2.4 GHz to channel 1, 6 or 11 with **20 MHz** width; enable 5 GHz with band steering; run a site survey.
4. **Security:** repeated deauth frames from an unknown MAC suggest a **deauthentication attack** or misbehaving device. Enable **802.11w Protected Management Frames** (move to WPA3), use the controller's WIPS to locate the source, and treat it as a security incident under the IRP.
5. **Verify** throughput with iperf3 and Wi-Fi stability over a day; **document** root causes (duplex mismatch, poor channel plan, deauth attack) and preventive actions (standard port templates, channel plan, WIPS alerts to syslog/SIEM).
</details>

**Scenario 3 – Securing and keeping a clinic online.**
A clinic has a flat network (one VLAN), Telnet enabled on its router, SNMP community `public`, a single ISP, and nightly backups to a USB disk kept next to the server. Patient records must be available during clinic hours and no more than 1 hour of data may be lost. Propose a plan covering segmentation, hardening, monitoring, high availability and backups.

<details>
<summary>✅ Model answer</summary>

- **Segmentation:** VLANs for Reception, Clinical, Servers, Medical devices, Guest Wi-Fi, Management; inter-VLAN ACLs (only Clinical and Reception reach the records application on its port; guests internet only); DHCP snooping + DAI; 802.1X for clinical PCs.
- **Hardening:** `enable secret`, SSH v2 only with a VTY ACL and timeout, remove Telnet and HTTP server, remove SNMP `public` and use SNMPv3, shut unused ports, login banner, firmware updates, configuration backups and a baseline audit script.
- **Monitoring:** NTP on all devices; central syslog (warnings and above) to a log server/SIEM; alerts for severity 0–3, failed admin logins, port-security violations, high utilisation.
- **High availability:** second ISP (or 4G/5G backup) with failover; UPS for network and server; dual power supplies; consider two firewalls in an HA pair; VRRP if two routers.
- **Backups and DR:** RPO 1 h → hourly incremental/snapshots plus nightly full; **3-2-1-1-0**: local NAS copy, encrypted off-site/cloud copy, one immutable copy; monthly restore tests; written DR runbook with RTO agreed with management (e.g. 2 h) and a warm or cloud recovery site.
- **People and process:** AUP, change management, offboarding procedure, phishing awareness, incident response plan tested by tabletop exercise.
</details>

---

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Cybersecurity and Digital Forensics</sub>
