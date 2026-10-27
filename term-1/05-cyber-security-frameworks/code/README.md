# 💻 Code · Module 5: Introduction to Cyber Security Frameworks

> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Every file below is complete and runnable on its own. Each one is used by a session page, which shows the real output it produced.

[⬅ Back to the module](../README.md)

## ⚙️ Setup

- Python 3.10 or newer; only the standard library is used, so there is nothing to install.
- Run every command from inside this `code/` folder. Each script is self-contained: no data files, no network access.
- All people, organisations, e-mails, IP addresses (documentation ranges), hashes and cases are fictional teaching data.
- `session-02_evidence_hashing.py` creates its sample evidence in a temporary folder and deletes it when it finishes.
- The legal and compliance tools are teaching simplifications, not legal advice.
- Prefer the browser? Each session's notebook (`.ipynb`) opens in Google Colab with one click.

## 📂 Files

### [Session 1: General Data Protection Regulation (GDPR)](../session-01-gdpr.md)

| File | What it does | How to run |
|---|---|---|
| [`session-01_breach_and_fines.py`](session-01_breach_and_fines.py) | The 72-hour breach clock and the two tiers of GDPR fines. | `python session-01_breach_and_fines.py` |
| [`session-01_dsar_handler.py`](session-01_dsar_handler.py) | Handle data subject requests (access, rectification, erasure, portability). | `python session-01_dsar_handler.py` |
| [`session-01_principles_audit.py`](session-01_principles_audit.py) | Audit a record of processing activities against the GDPR principles. | `python session-01_principles_audit.py` |
| [`session-01_pseudonymise.py`](session-01_pseudonymise.py) | Masking, hashing, keyed pseudonymisation and k-anonymity. | `python session-01_pseudonymise.py` |
| [`session-01-gdpr.ipynb`](session-01-gdpr.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/05-cyber-security-frameworks/code/session-01-gdpr.ipynb) |

### [Session 2: Types of Cybercrimes and Investigation Tools](../session-02-cybercrimes-and-investigation-tools.md)

| File | What it does | How to run |
|---|---|---|
| [`session-02_crime_classifier.py`](session-02_crime_classifier.py) | Triage incident reports into cybercrime categories. | `python session-02_crime_classifier.py` |
| [`session-02_email_header_analyzer.py`](session-02_email_header_analyzer.py) | Analyse a suspicious email's headers (phishing investigation and OSINT). | `python session-02_email_header_analyzer.py` |
| [`session-02_evidence_hashing.py`](session-02_evidence_hashing.py) | Hash digital evidence at acquisition and verify it later. | `python session-02_evidence_hashing.py` |
| [`session-02_ioc_matcher.py`](session-02_ioc_matcher.py) | Match threat-intelligence indicators (IOCs) against your own logs. | `python session-02_ioc_matcher.py` |
| [`session-02_log_triage.py`](session-02_log_triage.py) | Threat detection from authentication logs (a tiny SIEM rule engine). | `python session-02_log_triage.py` |
| [`session-02-cybercrimes-and-investigation-tools.ipynb`](session-02-cybercrimes-and-investigation-tools.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/05-cyber-security-frameworks/code/session-02-cybercrimes-and-investigation-tools.ipynb) |

### [Session 3: Cyber Laws, Data Protection and Digital Evidence](../session-03-cyber-laws-and-digital-evidence.md)

| File | What it does | How to run |
|---|---|---|
| [`session-03_custody_ledger.py`](session-03_custody_ledger.py) | A hash-chained chain-of-custody ledger. | `python session-03_custody_ledger.py` |
| [`session-03_law_matrix.py`](session-03_law_matrix.py) | Which laws apply? A law-applicability matrix for fictional incidents. | `python session-03_law_matrix.py` |
| [`session-03_volatility_planner.py`](session-03_volatility_planner.py) | Plan evidence collection in the order of volatility. | `python session-03_volatility_planner.py` |
| [`session-03-cyber-laws-and-digital-evidence.ipynb`](session-03-cyber-laws-and-digital-evidence.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/05-cyber-security-frameworks/code/session-03-cyber-laws-and-digital-evidence.ipynb) |

### [Session 4: AI in Cybersecurity Policies](../session-04-ai-in-cybersecurity-policies.md)

| File | What it does | How to run |
|---|---|---|
| [`session-04_adaptive_access.py`](session-04_adaptive_access.py) | Adaptive (risk-based) access control written as policy-as-code. | `python session-04_adaptive_access.py` |
| [`session-04_ai_governance_metrics.py`](session-04_ai_governance_metrics.py) | Governing an AI security model: accuracy, fairness and drift. | `python session-04_ai_governance_metrics.py` |
| [`session-04_login_anomaly.py`](session-04_login_anomaly.py) | User Behaviour Analytics: spotting unusual logins and enforcing policy. | `python session-04_login_anomaly.py` |
| [`session-04_phishing_classifier.py`](session-04_phishing_classifier.py) | A tiny, explainable phishing classifier (Naive Bayes from scratch). | `python session-04_phishing_classifier.py` |
| [`session-04-ai-in-cybersecurity-policies.ipynb`](session-04-ai-in-cybersecurity-policies.ipynb) | Executed notebook with every Python example of this session | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hamnakhan123/Cybersecurity-and-Digital-Forensics/blob/main/term-1/05-cyber-security-frameworks/code/session-04-ai-in-cybersecurity-policies.ipynb) |

## 🧩 Mini project

| File | What it does | How to run |
|---|---|---|
| [`mini_project_ai_compliance_toolkit.py`](mini_project_ai_compliance_toolkit.py) | AI security compliance toolkit. Walked through in [Session 4](../session-04-ai-in-cybersecurity-policies.md). | `python mini_project_ai_compliance_toolkit.py` |

---

<sub>Prepared by Hamna Zahid Khan, Junior Lecturer · Cybersecurity and Digital Forensics</sub>
