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