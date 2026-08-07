import json
import sys
from core.orchestrator import ComplianceOrchestrator
from database.db import log_audit_record

def main():
    print("=" * 60)
    print("  MERIDIAN GLOBAL BANK - AI COMPLIANCE MONITORING SYSTEM")
    print("=" * 60)
    
    orchestrator = ComplianceOrchestrator(risk_threshold=0.7)
    
    sample_payloads = [
        ("COMMUNICATION", {
            "text": "Hey, do not document this in email. Text me on Signal for tomorrow's trade targets."
        }),
        ("TRANSACTION", {
            "account_id": "ACC-3049",
            "trader_id": "TRD-88",
            "orders": [
                {"type": "BUY_LIMIT", "qty": 50000, "status": "CANCELLED"},
                {"type": "SELL_MARKET", "qty": 500, "status": "EXECUTED"}
            ]
        }),
        ("REGULATORY_UPDATE", {
            "update_text": "RBI issues mandatory cybersecurity guidelines for instant digital payment routes."
        })
    ]
    
    for event_type, payload in sample_payloads:
        print(f"\n[+] Processing Event Type: {event_type}")
        result = orchestrator.evaluate_event(event_type, payload)
        
        # Log to tamper-evident database
        hash_signature = log_audit_record(
            event_type=event_type,
            payload=payload,
            agent_output=result["agent_output"],
            escalation_required=result["escalation_required"],
            report=result["report"]
        )
        
        print(f"    - Escalation Required: {result['escalation_required']}")
        print(f"    - Audit Hash Signature: {hash_signature[:16]}...")
        
        if result["report"]:
            print(f"    - Draft Filing Type: {result['report'].get('report_type')}")
    
    print("\n[✔] Multi-agent surveillance execution complete.")

if __name__ == "__main__":
    main()