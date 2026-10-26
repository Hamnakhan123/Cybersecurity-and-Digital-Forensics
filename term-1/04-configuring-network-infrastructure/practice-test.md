# Module 4 Practice Test: Configuring Network Infrastructure

> [Cybersecurity and Digital Forensics](../../README.md) › [Term 1](../README.md) › [Module 4](README.md) › **Practice Test**

| ⬅ [Last session](session-15-automation-and-programmability.md) | [Module overview](README.md) ➡ |
|:---|---:|

Answer every question first, then open the hidden answers to check yourself. Aim for 16/20 or better before moving on.

---

## Part A: Multiple-choice questions

**1.** A 10 MB file is sent over a 100 Mbps link. Ignoring other delays, the transmission delay is about:
A) 0.08 s B) 0.8 s C) 8 s D) 80 s

**2.** At which OSI layer does a router make its forwarding decision?
A) Layer 2 B) Layer 3 C) Layer 4 D) Layer 7

**3.** The MAC address `01:00:5E:00:00:05` is a:
A) unicast address B) multicast address C) broadcast address D) burned-in Cisco address

**4.** What is the broadcast address of `10.4.77.130/26`?
A) 10.4.77.127 B) 10.4.77.191 C) 10.4.77.255 D) 10.4.77.159

**5.** Where does a Cisco router store its startup-config?
A) RAM B) flash C) NVRAM D) ROM

**6.** Which pair of DTP modes forms a trunk?
A) dynamic auto + dynamic auto B) access + dynamic desirable C) dynamic desirable + dynamic auto D) access + trunk

**7.** A port configured with PortFast and BPDU Guard receives a BPDU. What happens?
A) It becomes the root port B) It is placed in err-disabled state C) It forwards the BPDU D) Nothing

**8.** Which EtherChannel combination forms a bundle?
A) LACP passive + passive B) PAgP auto + auto C) LACP active + passive D) on + LACP active

**9.** A router has `10.1.0.0/16` from OSPF and `10.1.1.0/24` from RIP. Which route is used for `10.1.1.20`?
A) OSPF, lower AD B) RIP, longer prefix C) both, load-balanced D) neither

**10.** A floating static route that backs up an OSPF route should have an administrative distance of:
A) 1 B) 90 C) 110 D) 130

**11.** Two HSRP routers have priorities 110 and 100. The 110 router fails and later recovers without `preempt` configured. Which router is Active afterwards?
A) The 110 router B) The 100 router C) Both D) Neither

**12.** Which FHRP is an open standard and preempts by default?
A) HSRP B) GLBP C) VRRP D) CARP

**13.** A DHCP client renews its lease (T1) at what point of the lease?
A) 25% B) 50% C) 75% D) 87.5%

**14.** Which command makes a router forward DHCP broadcasts from a VLAN to a central server?
A) `ip dhcp relay` B) `ip helper-address` C) `ip dhcp forward` D) `service dhcp`

**15.** Where should an extended ACL normally be placed?
A) Close to the destination B) Close to the source C) Only on VTY lines D) On the core only

**16.** With DHCP snooping enabled, DHCP OFFER messages are accepted only on:
A) untrusted ports B) trusted ports C) access ports D) ports in VLAN 1

**17.** Which IPv6 NDP message gives hosts the prefix and default gateway?
A) Neighbor Solicitation B) Neighbor Advertisement C) Router Solicitation D) Router Advertisement

**18.** An SVI on a multilayer switch stays down/down. Which is the most likely cause?
A) `ip routing` is missing B) No active port or trunk carries that VLAN C) CEF is disabled D) DNS is misconfigured

**19.** Which IPsec protocol provides encryption?
A) AH B) ESP C) IKE D) GRE

**20.** Which wireless security option is recommended for university staff with individual accounts?
A) WEP B) WPA2-Personal with a shared password C) WPA3-Enterprise with 802.1X D) Open network with a hidden SSID

<details>
<summary>✅ Show answers</summary>

| Q | Answer | Why |
|---|---|---|
| 1 | B | 10 MB ≈ 80 Mb ÷ 100 Mbps = 0.8 s |
| 2 | B | Routers use IP addresses (network layer) |
| 3 | B | Lowest bit of the first byte is 1 → multicast |
| 4 | B | /26 block 64 → network .128, broadcast .191 |
| 5 | C | NVRAM keeps the startup-config |
| 6 | C | Desirable actively asks; auto agrees |
| 7 | B | BPDU Guard err-disables the edge port |
| 8 | C | Active initiates, passive responds |
| 9 | B | Longest prefix match comes before AD |
| 10 | D | Must be higher than OSPF's 110 |
| 11 | B | Without preemption the current Active keeps its role |
| 12 | C | VRRP, RFC 5798, preempt on by default |
| 13 | B | T1 = 50%, T2 = 87.5% |
| 14 | B | Relay converts the broadcast into a unicast |
| 15 | B | Drop unwanted traffic as early as possible |
| 16 | B | Only uplinks towards the real server are trusted |
| 17 | D | RA carries prefix, flags and the router's link-local |
| 18 | B | Autostate keeps an SVI down without active ports in the VLAN |
| 19 | B | ESP encrypts; AH only authenticates |
| 20 | C | Per-user authentication, revocation and logging |
</details>

## Part B: Scenario questions

**Scenario 1 – A new faculty building.**
The building receives `10.70.0.0/22`. It needs: Computer labs (420 hosts), Lecturers (110), Student Wi-Fi (230), Printers and CCTV (40) and two router links. Two distribution switches will provide the gateways. Design the VLSM plan, assign VLANs, and explain how you would provide gateway redundancy and loop-free Layer 2 with load sharing.

<details>
<summary>✅ Model answer</summary>

Largest first:

| VLAN | Segment | Hosts | Subnet | Gateway (virtual) | Broadcast |
|---|---|---|---|---|---|
| 10 | Labs | 420 | 10.70.0.0/23 | 10.70.0.1 | 10.70.1.255 |
| 20 | Student Wi-Fi | 230 | 10.70.2.0/24 | 10.70.2.1 | 10.70.2.255 |
| 30 | Lecturers | 110 | 10.70.3.0/25 | 10.70.3.1 | 10.70.3.127 |
| 40 | Printers/CCTV | 40 | 10.70.3.128/26 | 10.70.3.129 | 10.70.3.191 |
| – | Link 1 | 2 | 10.70.3.192/30 | – | 10.70.3.195 |
| – | Link 2 | 2 | 10.70.3.196/30 | – | 10.70.3.199 |

Free: `10.70.3.200/29`, `10.70.3.208/28`, `10.70.3.224/27`. The building summarises as `10.70.0.0/22`.

- **Gateways:** SVIs on DIST-1 (`.2`) and DIST-2 (`.3`) with **HSRPv2** virtual IP `.1`, authentication, preempt with delay, and tracking of each switch's uplink.
- **Load sharing:** DIST-1 HSRP active (priority 110) **and** STP root for VLANs 10 and 30; DIST-2 for VLANs 20 and 40 (`spanning-tree vlan … root primary`).
- **Loop-free:** Rapid PVST+, PortFast + BPDU Guard on all edge ports, LACP EtherChannel between DIST-1 and DIST-2 and from each access switch where two uplinks go to the same switch.
- **Services:** `ip helper-address` on each SVI to the central DHCP server, DHCP snooping + DAI on access switches.
</details>

**Scenario 2 – "Some users can't get online, and others are redirected."**
In a lab VLAN, half the PCs show `169.254.x.x` addresses and the others receive gateway `192.168.0.1` instead of the expected `10.20.30.1`. A small home router has been found connected to a desk port. Explain what happened and give the immediate fix and the permanent controls.

<details>
<summary>✅ Model answer</summary>

- **Cause:** the home router is a **rogue DHCP server** answering faster than the real server, handing out its own subnet/gateway (`192.168.0.1`) – a man-in-the-middle risk. Its small pool ran out, so later clients received nothing and self-assigned **APIPA** addresses.
- **Immediate:** remove the device / shut the port (find it via `show mac address-table` and the rogue gateway MAC); have clients release/renew; check whether any credentials were entered on redirected pages and reset them.
- **Permanent controls:** **DHCP snooping** on the VLAN with only the uplink trusted and rate limits on access ports; **DAI** and **IP Source Guard**; **port security** (max MACs) and **BPDU Guard** on desk ports; 802.1X for lab PCs; log snooping drops to syslog and alert; awareness for lab users. Verify that a test rogue's OFFERs are dropped and logged.
</details>

**Scenario 3 – Connecting a branch and automating it.**
A company opens a branch in Lahore that must reach the Karachi data centre. Users report after the first tunnel test that "ping works but file uploads and some web pages hang". Management also wants every future branch built in under a day with consistent configuration. Explain the VPN design, the cause and fix of the problem, and the automation approach.

<details>
<summary>✅ Model answer</summary>

- **VPN design:** route-based site-to-site IPsec (VTI or GRE over IPsec) with **IKEv2**, AES-256-GCM, DH group 14+/19, **PFS**, certificate authentication from an internal CA; OSPF over the tunnel; a second ISP and tunnel with a higher cost for resilience; remote-access VPN with MFA for mobile staff.
- **Problem:** an **MTU black hole** – encapsulation adds ~60–80 bytes, so 1 500-byte packets with DF set cannot pass and are dropped. **Fix:** `ip mtu 1400` and `ip tcp adjust-mss 1360` on the tunnel interfaces; confirm with `ping … size 1472 df-bit` (fails) vs smaller sizes (work).
- **Automation:** define every branch in a **source of truth** (JSON/YAML in Git: subnets, VLANs, tunnel addresses, peers); **validate** data (no overlaps, unique IDs); **render** router/switch configs from templates that include the security baseline; deploy through a controller's **REST API** or Ansible after peer review; run **drift detection** and nightly backups; record every change in Git for rollback and audit.
</details>

---

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Cybersecurity and Digital Forensics</sub>
