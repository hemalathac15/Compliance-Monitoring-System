from agents.communication import analyze_communication
from agents.transaction import analyze_transaction
from agents.regulatory import analyze_regulatory
from agents.reporter import generate_report

class ComplianceOrchestrator:
    def __init__(self, risk_threshold: float = 0.4):
        self.risk_threshold = risk_threshold

    def evaluate_event(self, event_type: str, payload: dict) -> dict:
        agent_output = {}
        report = None
        
        if event_type == "COMMUNICATION":
            text = payload.get("text", "")
            agent_output = analyze_communication(text)
        elif event_type == "TRANSACTION":
            agent_output = analyze_transaction(payload)
        elif event_type == "REGULATORY_UPDATE":
            agent_output = analyze_regulatory(payload)
        else:
            raise ValueError(f"Unknown event type: {event_type}")

        # Extract risk metrics
        risk_score = agent_output.get("risk_score", 0.0)
        is_suspicious = agent_output.get("is_suspicious", False)
        impact_level = agent_output.get("impact_level", "")

        # Determine escalation logic
        escalation_required = (risk_score >= self.risk_threshold) or is_suspicious or (impact_level in ["HIGH", "MEDIUM"])

        if escalation_required:
            # Bundle data into a single dictionary parameter expected by generate_report()
            report_payload = {
                "event_type": event_type,
                "payload": payload,
                "agent_output": agent_output
            }
            report = generate_report(report_payload)

        return {
            "status": "PROCESSED",
            "event_type": event_type,
            "agent_output": agent_output,
            "escalation_required": escalation_required,
            "report": report
        }