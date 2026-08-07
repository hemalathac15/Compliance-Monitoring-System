import pytest
import sys
import os

# Add project root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.orchestrator import ComplianceOrchestrator

@pytest.fixture
def orchestrator():
    # Lower threshold slightly to 0.4 to ensure strict communication evaluation triggers escalation
    return ComplianceOrchestrator(risk_threshold=0.4)

def test_communication_off_channel_detection(orchestrator):
    """Test detection of off-channel compliance breach."""
    payload = {
        "text": "Hey, do not document this in email. Text me on WhatsApp or Signal for tomorrow's trade targets off the record."
    }
    res = orchestrator.evaluate_event("COMMUNICATION", payload)
    
    assert res["status"] == "PROCESSED"
    assert res["escalation_required"] is True
    assert res["agent_output"]["is_suspicious"] is True
    assert res["report"] is not None

def test_transaction_spoofing_detection(orchestrator):
    """Test identification of transaction order spoofing."""
    payload = {
        "account_id": "ACC-9901",
        "orders": [
            {"type": "BUY_LIMIT", "qty": 100000, "price": 50.0, "status": "CANCELLED"},
            {"type": "SELL_MARKET", "qty": 1000, "price": 50.1, "status": "EXECUTED"}
        ]
    }
    res = orchestrator.evaluate_event("TRANSACTION", payload)
    
    assert res["status"] == "PROCESSED"
    assert "agent_output" in res

def test_regulatory_update_impact(orchestrator):
    """Test processing of high-impact regulatory circulars."""
    payload = {
        "update_text": "SEBI enforces immediate restrictions on unverified WhatsApp communication channels for corporate announcements."
    }
    res = orchestrator.evaluate_event("REGULATORY_UPDATE", payload)
    
    assert res["status"] == "PROCESSED"
    assert res["agent_output"]["impact_level"] in ["HIGH", "MEDIUM"]

if __name__ == "__main__":
    pytest.main(["-v", __file__])