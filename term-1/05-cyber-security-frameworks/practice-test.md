# Module 5 Practice Test: Introduction to Cyber Security Frameworks

> [Cybersecurity and Digital Forensics](../../README.md) › [Term 1](../README.md) › [Module 5](README.md) › **Practice Test**

| ⬅ [Last session](session-04-ai-in-cybersecurity-policies.md) | [Module overview](README.md) ➡ |
|:---|---:|

Answer every question first, then open the hidden answers to check yourself. Aim for 16/20 or better before moving on.

---

## Part A: Multiple-choice questions

**1.** Which of the following is **personal data** under the GDPR?
A) A company's annual turnover B) A dynamic IP address linked to a student's login record C) Fully anonymised national statistics D) The weather in Lahore

**2.** A Karachi software house builds a payroll app and processes staff data only on the instructions of a German client. Under the GDPR, the software house is the:
A) controller B) processor C) data subject D) supervisory authority

**3.** An online shop asks for a customer's date of birth, mother's name and blood group just to deliver a book. Which principle is most clearly broken?
A) Accuracy B) Data minimisation C) Storage limitation D) Accountability

**4.** A customer sends a subject access request on 3 March. Without an extension, the controller must normally reply by:
A) 10 March B) 3 April C) 3 May D) 3 June

**5.** After discovering a personal-data breach that poses a risk to people, a controller must notify the supervisory authority within:
A) 24 hours B) 72 hours C) 7 days D) 30 days

**6.** A company has worldwide annual turnover of EUR 2 billion and commits a top-tier GDPR infringement. The maximum fine is:
A) EUR 20 million B) EUR 40 million C) EUR 80 million D) EUR 200 million

**7.** Ransomware encrypts a hospital's file server. In this case the computer is the cybercrime's:
A) tool B) target C) evidence store only D) witness

**8.** What is the correct order of the digital-investigation process?
A) Collection → identification → analysis → preservation → presentation
B) Identification → preservation → collection → examination → analysis → presentation
C) Analysis → collection → preservation → presentation → identification
D) Preservation → presentation → identification → collection → analysis

**9.** Which tool is used mainly to analyse a **memory (RAM) image**?
A) Wireshark B) Volatility C) Nmap D) Cellebrite

**10.** A SIEM shows one IP trying one common password against 300 different accounts in 10 minutes. This pattern is:
A) brute force B) password spraying C) SQL injection D) a DDoS attack

**11.** According to the Pyramid of Pain, which indicator is **hardest** for an attacker to change once defenders detect it?
A) File hashes B) IP addresses C) Domain names D) Tactics, techniques and procedures (TTPs)

**12.** Which statement about OSINT is correct?
A) Logging in with a leaked password to view a private profile is OSINT B) OSINT uses public sources for a lawful purpose and records the URL, time and a hash of each capture C) OSINT findings need no corroboration D) OSINT is illegal in Pakistan

**13.** In most computer-misuse laws, including PECA 2016, the key element that separates a penetration test from a crime is:
A) the tool used B) written authorisation C) the time of day D) the attacker's nationality

**14.** Which Pakistani law gives electronic documents and electronic signatures legal recognition?
A) PECA 2016 B) Qanun-e-Shahadat Order 1984 C) Electronic Transactions Ordinance 2002 D) Pakistan Penal Code 1860

**15.** According to RFC 3227, which should be collected **first** from a live suspect system?
A) Backup tapes B) The hard disk image C) Memory, running processes and network connections D) Remote log server archives

**16.** An investigator finds a running laptop with full-disk encryption. The best first action is to:
A) pull the power plug immediately B) capture memory (and note open sessions) before shutting down, with authority and a write-blocking plan for the disk C) reinstall the operating system D) copy interesting files with drag and drop

**17.** Why is a SHA-256 hash recorded when evidence is imaged?
A) To compress the image B) To prove later that the image has not changed since collection C) To encrypt the evidence D) To identify the suspect

**18.** An AI phishing filter had TP = 90, FP = 30, FN = 10, TN = 870. Its **precision** is:
A) 0.75 B) 0.90 C) 0.96 D) 0.97

**19.** The Population Stability Index (PSI) between a model's training data and this month's data is 0.31. The right action is to:
A) do nothing, it is stable B) watch it for another month C) investigate and retrain or recalibrate the model D) delete the model logs

**20.** An AI exam-proctoring tool flags a student for cheating. Under GDPR Article 22 and good AI policy, what should happen before a penalty?
A) The penalty is applied automatically B) A trained human reviews the evidence, the student can respond, and the decision is logged C) The student is told nothing D) The vendor decides

<details>
<summary>✅ Show answers</summary>

| Q | Answer | Why |
|---|---|---|
| 1 | B | It can identify a living person when combined with the login record; anonymised statistics and company data are not personal data |
| 2 | B | It processes on the client's instructions; the German client decides why and how, so it is the controller |
| 3 | B | Only name and address are needed to deliver a book |
| 4 | B | One month from receipt; extendable by two more months for complex or many requests |
| 5 | B | Article 33: 72 hours from becoming aware, unless the breach is unlikely to cause risk |
| 6 | C | Higher of EUR 20 m or 4% of turnover: 4% × 2 bn = EUR 80 m |
| 7 | B | The system itself is attacked; when it is used to commit fraud it is the tool |
| 8 | B | Identify, preserve before collecting, then examine, analyse and present |
| 9 | B | Volatility analyses memory images; Wireshark is for packets, Cellebrite for mobiles |
| 10 | B | One password against many accounts = spraying; many passwords against one account = brute force |
| 11 | D | Hashes, IPs and domains are cheap to change; behaviour is not |
| 12 | B | Public sources, lawful purpose, documented and corroborated; logging in with stolen credentials is unauthorised access |
| 13 | B | Unauthorised access is the offence; authorisation (scope in writing) makes testing lawful |
| 14 | C | ETO 2002 recognises electronic records and signatures; PECA covers offences, QSO covers evidence |
| 15 | C | Most volatile first: memory and live state disappear at shutdown |
| 16 | B | Pulling the plug loses the RAM and may lock the data behind encryption |
| 17 | B | Matching hashes at any later point prove integrity for the court |
| 18 | A | Precision = 90 ÷ (90 + 30) = 0.75; recall would be 90 ÷ 100 = 0.90 |
| 19 | C | PSI > 0.25 means a significant shift; the model needs investigation and retraining |
| 20 | B | Significant decisions need meaningful human review, a chance to contest and an audit trail |
</details>

## Part B: Scenario questions

**Scenario 1 – A breach at a Karachi software house.**
"CodeKarachi" (fictional) runs an online learning platform used by 40 000 students, 6 000 of them in Germany and France. On Monday at 09:00 the team discovers that a misconfigured cloud storage bucket exposed names, e-mail addresses, course grades and hashed passwords for three weeks. Explain whether the GDPR applies, what must happen in the first 72 hours, which principles were broken, and the maximum fine if the company's worldwide turnover is EUR 30 million.

<details>
<summary>✅ Model answer</summary>

- **Scope:** yes. The platform **offers services to people in the EU** (Article 3(2)), so the GDPR applies even though the company is in Pakistan. It must also appoint an **EU representative** (Article 27).
- **First 72 hours (deadline: Thursday 09:00):**
  1. **Contain:** make the bucket private, rotate keys, force password resets, keep logs (do not delete evidence).
  2. **Assess:** what data, how many people, for how long, was it actually accessed (check access logs), how risky (grades and e-mails enable phishing; hashed passwords can be cracked if the hashing is weak).
  3. **Notify** the lead supervisory authority within **72 hours** with: nature of the breach, categories and approximate numbers, DPO contact, likely consequences, measures taken. Partial information is allowed, with more to follow.
  4. **Tell affected students** without undue delay because the risk is high: what happened, what they should do (change reused passwords, watch for phishing).
  5. **Record** it in the breach register, even the parts not reported.
- **Principles broken:** **integrity and confidentiality** (no appropriate security), **accountability** (no checks that would show the bucket was public), possibly **storage limitation** if old records were kept.
- **Maximum fine:** security failures sit in the lower tier: higher of EUR 10 m or 2% × 30 m = 0.6 m → **EUR 10 million**. (If principles under Article 5 are judged infringed, the upper tier applies: higher of EUR 20 m or 4% → EUR 20 million.) Real fines are usually far smaller and depend on cooperation and the steps taken.
- **Pakistan angle:** PECA 2016 offences apply to whoever accessed the data unlawfully; report to the NCCIA.
</details>

**Scenario 2 – An insider at a university.**
The IT office of a university finds that marks in the exam database were changed late at night from a lab workstation, `LAB-WS-14`. A junior lab assistant is suspected. The workstation is still switched on and logged in. You are asked to lead the investigation. Describe how you would collect and preserve the evidence so it is admissible, which tools you would use, and which laws apply in Pakistan.

<details>
<summary>✅ Model answer</summary>

- **Authority first:** written approval from the registrar/legal office; define scope (one workstation, database logs, CCTV, door access logs). Involve HR; if criminal, report to the **NCCIA**.
- **Plan and isolate:** photograph the screen and setup; do **not** switch the machine off; disconnect it from the network only if the plan says so (to stop remote wiping) and note the time.
- **Order of volatility (RFC 3227):** capture **RAM** (e.g. a trusted memory acquisition tool from a clean USB), running processes, network connections and logged-in users; then shut down correctly and **image the disk with a write blocker** (FTK Imager or `dd`).
- **Integrity:** compute **SHA-256** of every image and log export at collection; seal and label exhibits; start a **chain-of-custody** form (who, what, when, where, why, hash) for every transfer.
- **Other sources:** database audit logs, authentication logs and the SIEM timeline, the badge-access system and CCTV for who was in the lab at that time. Export with hashes.
- **Analysis on copies only:** Volatility for memory, Autopsy for the disk image, Plaso for a super-timeline; correlate the change time with logins and door access. Remember a logged-in account does not prove who was at the keyboard; corroborate.
- **Laws:** **PECA 2016** (unauthorised access to and interference with information systems and data); **Qanun-e-Shahadat 1984** and **ETO 2002** for admitting electronic records; follow **ISO/IEC 27037** and the **ACPO** principles so the defence cannot challenge the handling.
- **Report:** factual, repeatable, with hashes, tool versions and the full custody record.
</details>

**Scenario 3 – Deploying AI in a bank's SOC.**
A Karachi bank wants to (a) use an AI model to flag unusual employee logins and automatically lock accounts, and (b) use an AI system to score loan applicants. In a pilot month the login model produced TP = 40, FP = 160, FN = 10, TN = 9 790. Evaluate the login model, explain the risks, and write the key AI-policy controls the bank should adopt before going live with both systems.

<details>
<summary>✅ Model answer</summary>

- **Metrics:** accuracy = (40 + 9 790) ÷ 10 000 = **98.3%** (misleading because attacks are rare). Precision = 40 ÷ 200 = **0.20** (4 of 5 alerts are false). Recall = 40 ÷ 50 = **0.80**. FPR = 160 ÷ 9 950 ≈ **1.6%**.
- **Verdict:** good at catching attacks, but automatic locking would block about 160 genuine staff a month. Use **adaptive access** instead: high risk → step-up MFA, very high risk → lock plus analyst review. Tune thresholds and re-measure.
- **Risks:** **bias** (shift workers or staff in other cities flagged more often; check the flag-rate ratio by group ≥ 0.80), **black box** (analysts must be able to explain a lock), **adversarial AI** (attackers mimic normal behaviour; poisoned training data), **drift** (new working patterns; monitor PSI monthly), **privacy** (behaviour monitoring needs a lawful basis, transparency and minimisation), **over-reliance** (analysts stop checking).
- **Loan scoring is high-risk:** it makes significant decisions about people, so it needs a **DPIA**, bias testing before release, explanations for applicants, **human review** of declines (GDPR Article 22 idea), and records of every decision.
- **Policy controls:** register every AI system with an owner; risk tier; accuracy, fairness and drift thresholds with re-testing schedule; human-in-the-loop for high-impact actions; adversarial and prompt-injection testing; logging for audit and evidence; vendor contracts covering data use and incidents; an AI incident and rollback plan; alignment with the **NIST AI RMF** (Govern, Map, Measure, Manage), **ISO/IEC 42001**, the State Bank's regulations and Pakistan's National AI Policy 2025.
- **Golden rule:** AI recommends, written policy decides the action, humans own high-impact decisions, logs prove it.
</details>

---

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer · Cybersecurity and Digital Forensics</sub>
