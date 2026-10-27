"""Session 3 - Plan evidence collection in the order of volatility.

Some evidence disappears in seconds (CPU state, RAM, network connections); some lasts
for years (backups, printouts). RFC 3227 and NIST SP 800-86 say: collect the most
volatile evidence first. This planner takes the artefacts on a fictional live machine,
sorts them by volatility, skips what is impossible in the device's state, warns about
traps (full-disk encryption, cloud sessions), and checks the plan fits the time on site.

Run:  python session-03_volatility_planner.py
"""

# rank: 1 = disappears fastest.  minutes = rough collection time.  needs_power: lost at shutdown
ARTEFACTS = [
    # name,                                   rank, minutes, needs_power
    ("Archival media (offsite backups)",          8, 0,  False),
    ("Disk image (with write blocker)",           6, 90, False),
    ("RAM (full memory capture)",                 2, 12, True),
    ("Network connections and ARP/route cache",   3, 2,  True),
    ("Running processes and open files",          4, 3,  True),
    ("Logged-in users and cloud sessions",        4, 2,  True),
    ("Temporary files and swap/pagefile",         5, 10, False),
    ("CPU registers and cache",                   1, 0,  True),
    ("Remote logs (firewall, SIEM, email)",       7, 20, False),
    ("Screen photo (what is visible now)",        1, 1,  True),
]

TOOLS = {
    "RAM": "memory imager (e.g. WinPmem/LiME) to external drive",
    "Network": "netstat/ss + arp -a output saved and hashed",
    "Running": "process list with command lines (e.g. tasklist /v, ps aux)",
    "Logged-in": "query user / who; note cloud tabs before they time out",
    "Disk": "imager + hardware write blocker, MD5+SHA-256",
    "Temporary": "collected inside the disk image; note pagefile/swap",
    "Remote": "preservation request to the log owner, export + hash",
    "Archival": "request through the organisation's backup custodian",
    "Screen": "photograph the screen with time visible",
    "CPU": "not practical to capture; noted for completeness",
}


def plan(device_on, disk_encrypted, minutes_on_site):
    print(f"\n=== Device {'ON' if device_on else 'OFF'} | full-disk encryption "
          f"{'YES' if disk_encrypted else 'no'} | {minutes_on_site} min on site ===")
    steps, used, skipped = [], 0, []
    for name, rank, mins, needs_power in sorted(ARTEFACTS, key=lambda a: (a[1], a[2])):
        if needs_power and not device_on:
            skipped.append(f"{name} (lost when the device powered off)")
            continue
        if mins == 0:
            skipped.append(f"{name} (not practical or done off site)")
            continue
        steps.append((rank, name, mins))
    for i, (rank, name, mins) in enumerate(steps, 1):
        used += mins
        flag = "" if used <= minutes_on_site else "  <- over time budget: hand to lab / preservation request"
        tool = TOOLS[name.split()[0]]
        print(f" {i:>2}. [vol {rank}] {name:<42} {mins:>3} min (t={used:>3})  {tool}{flag}")
    for s in skipped:
        print("     skip:", s)
    if device_on and disk_encrypted:
        print("  ! Encrypted disk is UNLOCKED now: capture RAM (keys) and consider a live logical")
        print("    copy of key folders BEFORE any shutdown, or the data may become unreadable.")
    if device_on:
        print("  ! Isolate from the network (unplug cable / airplane mode) rather than power off,")
        print("    unless destructive malware is actively wiping data.")
    else:
        print("  ! Device is off: do NOT switch it on. Bag, seal, label and image in the lab.")
    print("  ! Record every command you type, with the time, in your notes and custody form.")


# Case A: suspect laptop found running and unlocked, encrypted disk, 60 minutes on site
plan(device_on=True, disk_encrypted=True, minutes_on_site=60)
# Case B: same model found switched off
plan(device_on=False, disk_encrypted=True, minutes_on_site=60)
