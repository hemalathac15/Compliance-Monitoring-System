import json
from typing import Union, Dict, Any
from agents.communication import analyze_communication
from agents.transaction import analyze_transaction
from agents.regulatory import analyze_regulatory
from agents.reporter import generate_report

class ComplianceOrchestrator:
    def __init__(self, risk_threshold: float = 0.4):
        self.risk_threshold = risk_threshold

    def evaluate_event(self, event_type: str, payload: Union[dict, str]) -> dict:
        # 1. Normalize payload if passed as a raw string
        if isinstance(payload, str):
            payload_dict = {"text": payload, "raw": payload}
        elif isinstance(payload, dict):
            payload_dict = payload
        else:
            payload_dict = {"raw": str(payload)}

        agent_output: Any = {}
        report = None
        
        # 2. Route event to corresponding agent
        if event_type == "COMMUNICATION":
            text = payload_dict.get("text", "")
            agent_output = analyze_communication(text)
        elif event_type == "TRANSACTION":
            agent_output = analyze_transaction(payload_dict)
        elif event_type == "REGULATORY_UPDATE":
            agent_output = analyze_regulatory(payload_dict)
        else:
            raise ValueError(f"Unknown event type: {event_type}")

        # 3. Ensure agent_output is parsed as a dictionary if returned as a JSON string
        if isinstance(agent_output, str):
            try:
                agent_output_dict = json.loads(agent_output)
            except json.JSONDecodeError:
                agent_output_dict = {"summary": agent_output}
        elif isinstance(agent_output, dict):
            agent_output_dict = agent_output
        else:
            agent_output_dict = {}

        # 4. Extract risk metrics safely
        risk_score = float(agent_output_dict.get("risk_score", 0.0))
        is_suspicious = bool(agent_output_dict.get("is_suspicious", False))
        impact_level = str(agent_output_dict.get("impact_level", "")).upper()

        # 5. Determine escalation logic
        escalation_required = (
            (risk_score >= self.risk_threshold) or 
            is_suspicious or 
            (impact_level in ["HIGH", "MEDIUM"])
        )

        if escalation_required:
            report_payload = {
                "event_type": event_type,
                "payload": payload_dict,
                "agent_output": agent_output_dict
            }
            report = generate_report(report_payload)

        return {
            "status": "PROCESSED",
            "event_type": event_type,
            "agent_output": agent_output,
            "escalation_required": escalation_required,
            "report": report
        }