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

---

## Execution & Test Results

### 1. Automated Test Suite Execution (`pytest`)
All multi-agent detection pipelines and escalation paths pass end-to-end unit testing with 100% success rate:

```bash
$ pytest tests/test_scenario.py -v

===================================== test session starts ======================================
platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0
plugins: anyio-4.14.2, langsmith-0.10.16
collected 3 items                                                                               

tests/test_scenario.py::test_communication_off_channel_detection PASSED                 [ 33%]
tests/test_scenario.py::test_transaction_spoofing_detection PASSED                        [ 66%]
tests/test_scenario.py::test_regulatory_update_impact PASSED                             [100%]

====================================== 3 passed in 12.30s ======================================


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