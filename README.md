# Meridian Sentinel - AI Compliance Monitoring System

An end-to-end, multi-agent AI surveillance system designed to detect compliance breaches across communications, trading transactions, and regulatory updates in real time.

---

## Features

* **Multi-Agent Architecture:** Specialized agents powered by **LangChain** and **Groq (Llama 3.3 70B)**.
* **Structured Output Parsing:** Guaranteed typed JSON output (`risk_score`, `is_suspicious`, `impact_level`) via **Pydantic V2**.
* **Automated Risk Escalation:** Centralized `ComplianceOrchestrator` evaluates risk thresholds across domains.
* **Incident Report Generation:** Automated `Reporter Agent` creates audit-grade filings (SARs, Incident Reports) upon breach detection.
* **Interactive Dashboard:** Built with **Streamlit** for live event testing and compliance monitoring.
* **Unit Testing Suite:** Automated test validation covering real-world compliance scenarios using **pytest**.
## System Architecture

![System Architecture Flowchart](./assets/workflow.png)

```text
                      +-----------------------------------+
                      |      Input Event / Dashboard      |
                      |          (dashboard/app.py)       |
                      +-----------------+-----------------+
                                        |
                                        v
                      +-----------------+-----------------+
                      |     Compliance Orchestrator       |
                      |       (core/orchestrator.py)      |
                      +-----------------+-----------------+
                                        |
        +-------------------------------+-------------------------------+
        |                               |                               |
        v                               v                               v
+-------+-------+               +-------+-------+               +-------+-------+
| Communication |               |  Transaction  |               |  Regulatory   |
| Scanner Agent |               | Monitor Agent |               | Tracker Agent |
| (agents/      |               | (agents/      |               | (agents/      |
| communication)|               |  transaction) |               |  regulatory)  |
+-------+-------+               +-------+-------+               +-------+-------+
        |                               |                               |
        +-------------------------------+-------------------------------+
                                        |
                                        v
                       [ Risk Score & Threshold Check ]
                                        |
                         +--------------+--------------+
                         |                             |
                         | Risk >= Threshold           | Risk < Threshold
                         v                             v
               +---------+---------+          +--------+--------+
               |  Report Generator |          |     Log to      |
               |       Agent       |          |    Database     |
               | (agents/reporter) |          +-----------------+
               +---------+---------+
                         |
                         v
               +---------+---------+
               | Audit DB / Stream |
               | (database/db.py)  |
               +-------------------+

---

## 🧪 Test Results & Validation

The system undergoes automated end-to-end testing against **20 real-world compliance scenarios** using `pytest`. The scenarios cover global regulatory standards from the **SEC, FCA, FINRA, OFAC, RBI, and SEBI**.

### Scenario Test Coverage

* **Communication Scanner:** SEC off-channel chats (WhatsApp), insider trading tips, FINRA spoofing intent, FCA market manipulation, routine client inquiries.
* **Transaction Monitor:** Spoofing order patterns, OFAC sanctioned entity transfers, wash trading, front-running, FinCEN structuring/smurfing, microcap pump & dump, routine settlements.
* **Regulatory Tracker:** FCA Consumer Duty impact, SEC T+1 settlement transitions, OFAC SDN additions, FINRA crypto guidance, RBI cybersecurity framework, SEBI insider trading definitions, administrative circulars.
* **Report Generator:** Automated Suspicious Activity Report (SAR) generation and escalation triggers.

### Execution Summary

```text
===================================== test session starts ======================================
platform win32 -- Python 3.14.2, pytest-9.1.1
rootdir: D:\Zetheta Project\compliance-monitoring-system

tests/test_scenario.py::test_sec_off_channel_whatsapp PASSED                              [  5%]
tests/test_scenario.py::test_sec_insider_trading_tip PASSED                                [ 10%]
tests/test_scenario.py::test_finra_spoofing_intent PASSED                                 [ 15%]
tests/test_scenario.py::test_fca_market_manipulation_benchmark PASSED                     [ 20%]
tests/test_scenario.py::test_routine_client_inquiry_low_risk PASSED                       [ 25%]
tests/test_scenario.py::test_finra_spoofing_order_pattern PASSED                          [ 30%]
tests/test_scenario.py::test_ofac_sanctioned_entity_transfer PASSED                       [ 35%]
tests/test_scenario.py::test_fca_wash_trading PASSED                                      [ 40%]
tests/test_scenario.py::test_finra_front_running PASSED                                   [ 45%]
tests/test_scenario.py::test_fincen_structuring_smurfing PASSED                           [ 50%]
tests/test_scenario.py::test_sec_pump_and_dump_microcap PASSED                            [ 55%]
tests/test_scenario.py::test_routine_settlement_low_risk PASSED                           [ 60%]
tests/test_scenario.py::test_fca_consumer_duty_high_impact PASSED                         [ 65%]
tests/test_scenario.py::test_sec_t_plus_1_settlement PASSED                               [ 70%]
tests/test_scenario.py::test_ofac_sanctions_list_update PASSED                            [ 75%]
tests/test_scenario.py::test_finra_crypto_communications PASSED                           [ 80%]
tests/test_scenario.py::test_rbi_cybersecurity_framework PASSED                           [ 85%]
tests/test_scenario.py::test_sebi_insider_trading_definition PASSED                       [ 90%]
tests/test_scenario.py::test_routine_administrative_circular_low_risk PASSED              [ 95%]
tests/test_scenario.py::test_high_risk_sar_generation PASSED                             [100%]

================================ 20 passed in 75.77s (0:01:15) =================================

### 2. Live CLI Multi-Agent Orchestration:
Sample output showing real-time event evaluation, threat detection, and auto-filing draft assignment across all 3 surveillance domains:

============================================================
  MERIDIAN GLOBAL BANK - AI COMPLIANCE MONITORING SYSTEM
============================================================

[+] Processing Event Type: COMMUNICATION
    - Escalation Required: True
    - Audit Hash Signature: bef403d0ff153bbe...
    - Draft Filing Type: SAR

[+] Processing Event Type: TRANSACTION
    - Escalation Required: True
    - Draft Filing Type: SAR

[+] Processing Event Type: REGULATORY_UPDATE
    - Escalation Required: True
    - Audit Hash Signature: d87b8f1e86dc90d2...
    - Draft Filing Type: REGULATORY_UPDATE_REPORT

[✔] Multi-agent surveillance execution complete.

### 3. Interactive Streamlit Dashboard Output:
When an off-channel communication violation is evaluated ("Let's move this conversation to WhatsApp..."), the system flags the high risk and outputs structured agent JSON along with the generated filing draft:

Agent Evaluation (Structured JSON Output):
{
  "is_suspicious": true,
  "violation_type": "OFF_CHANNEL_COMMUNICATION",
  "risk_score": 0.9,
  "flagged_entities": [
    "WhatsApp"
  ],
  "explanation": "The message suggests moving the conversation to an off-channel messaging platform, which may be a violation of compliance policies.",
  "recommended_action": "Report the incident to the compliance team and remind the employee of the company's communication policies."
}

Generated SAR Filing Draft:
{
  "report_type": "SAR",
  "severity": "HIGH",
  "executive_summary": "Off-channel communication violation detected, with a risk score of 0.9, where an employee suggested moving a conversation to WhatsApp, potentially breaching company communication policies.",
  "involved_parties": [
    "Employee",
    "WhatsApp"
  ],
  "regulatory_frameworks": [
    "SEC Rule 17a-4",
    "SEBI PIT"
  ],
  "recommended_next_steps": [
    "Report the incident to the compliance team",
    "Remind the employee of the company's communication policies"
  ]
}


---

## Project Structure

```text
compliance-monitoring-system/
├── agents/
│   ├── communication.py    # Communication Scanner Agent
│   ├── transaction.py      # Transaction Monitor Agent
│   ├── regulatory.py       # Regulatory Update Tracker Agent
│   └── reporter.py         # Report Generator Agent
├── assets/
│   └── workflow.png        # System architecture diagram image
├── core/
│   └── orchestrator.py     # Central Compliance Orchestrator
├── dashboard/
│   └── app.py              # Streamlit Web UI
├── database/
│   └── db.py               # Database connections and persistence models
├── tests/
│   └── test_scenario.py    # pytest scenario test suite
├── .env                    # API keys and environment variables
├── main.py                 # Main application CLI entrypoint
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

---
## Tech Stack

* **Language:** Python 3.10+
* **Framework:** LangChain, LangChain-Groq
* **LLM Engine:** Llama-3.3-70B-Versatile (via Groq API)
* **Validation:** Pydantic V2
* **Storage / Persistence:** SQLite (`database/db.py`)
* **Testing:** pytest
* **UI Dashboard:** Streamlit

---

## Getting Started

### 1. Prerequisites
* Python 3.10+ installed
* A valid **Groq API Key**

### 2. Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/hemalathac15/Compliance-Monitoring-System.git](https://github.com/hemalathac15/Compliance-Monitoring-System.git)
   cd Compliance-Monitoring-System

Create and activate a virtual environment:
python -m venv .venv
.\.venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Set up Environment Variables:
Create a .env file in the root directory and add your Groq API key:
GROQ_API_KEY=your_groq_api_key_here

Running the Project
Run via Terminal CLI
To test the pipeline via command line execution:

Bash
python main.py
Launch Streamlit Web UI
To start the interactive compliance monitoring dashboard:

Bash
streamlit run dashboard/app.py
Open http://localhost:8501 in your browser to inspect logs, submit test events, and view generated reports.

Run Automated Unit Tests
To validate system scenarios and multi-agent responses:

Bash
pytest tests/test_scenario.py -v