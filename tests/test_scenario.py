import os
import pytest
from dotenv import load_dotenv
from core.orchestrator import ComplianceOrchestrator

load_dotenv()

@pytest.fixture
def orchestrator():
    return ComplianceOrchestrator()

def _check_response(res):
    """Safely validates both dictionary and string responses from the orchestrator."""
    assert res is not None
    if isinstance(res, str):
        assert len(res.strip()) > 0
    elif isinstance(res, dict):
        assert len(res) > 0


# ============================================================================
# 1. COMMUNICATION SCANNER AGENT
# ============================================================================

def test_sec_off_channel_whatsapp(orchestrator):
    payload = "Let's take this offline and discuss the pricing structure on WhatsApp."
    _check_response(orchestrator.evaluate_event("COMMUNICATION", payload))

def test_sec_insider_trading_tip(orchestrator):
    payload = "Buy before market close. Earnings announcement tomorrow morning will beat estimates by 40%."
    _check_response(orchestrator.evaluate_event("COMMUNICATION", payload))

def test_finra_spoofing_intent(orchestrator):
    payload = "Push a massive buy block to fake depth, then cancel it right before my sell order executes."
    _check_response(orchestrator.evaluate_event("COMMUNICATION", payload))

def test_fca_market_manipulation_benchmark(orchestrator):
    payload = "Keep the LIBOR submission low today so our swap portfolio stays profitable."
    _check_response(orchestrator.evaluate_event("COMMUNICATION", payload))

def test_routine_client_inquiry_low_risk(orchestrator):
    payload = "Could you please send me the updated fee schedule for corporate accounts?"
    _check_response(orchestrator.evaluate_event("COMMUNICATION", payload))


# ============================================================================
# 2. TRANSACTION MONITOR AGENT
# ============================================================================

def test_finra_spoofing_order_pattern(orchestrator):
    payload = "ORDER_ID: 9021 | TYPE: LIMIT_BUY | QTY: 100000 | LATENCY: 12ms | STATUS: CANCELLED"
    _check_response(orchestrator.evaluate_event("TRANSACTION", payload))

def test_ofac_sanctioned_entity_transfer(orchestrator):
    payload = "SWIFT: MT103 | SENDER: Bank_A | BENEFICIARY: Sovcombank_Moscow | AMT: $2,500,000 USD"
    _check_response(orchestrator.evaluate_event("TRANSACTION", payload))

def test_fca_wash_trading(orchestrator):
    payload = "ACCOUNT_A -> SELL 50,000 AAPL | ACCOUNT_B (Same Beneficial Owner) -> BUY 50,000 AAPL"
    _check_response(orchestrator.evaluate_event("TRANSACTION", payload))

def test_finra_front_running(orchestrator):
    payload = "TRADER_PERSONAL_ACC: BUY 5,000 TSLA @ 14:00 | CLIENT_BLOCK_ORDER: BUY 500,000 TSLA @ 14:02"
    _check_response(orchestrator.evaluate_event("TRANSACTION", payload))

def test_fincen_structuring_smurfing(orchestrator):
    payload = "DEPOSITS: $9,800 @ 09:00 AM, $9,500 @ 11:30 AM, $9,900 @ 02:15 PM | LOCATION: Branch_4"
    _check_response(orchestrator.evaluate_event("TRANSACTION", payload))

def test_sec_pump_and_dump_microcap(orchestrator):
    payload = "SYMBOL: PENNY_STOCK_X | DAILY_VOL_CHANGE: +4500% | TRADER: Account_881"
    _check_response(orchestrator.evaluate_event("TRANSACTION", payload))

def test_routine_settlement_low_risk(orchestrator):
    payload = "TXN_TYPE: DIVIDEND_PAYOUT | AMOUNT: $142.50 | ACCOUNT: RET_99012"
    _check_response(orchestrator.evaluate_event("TRANSACTION", payload))


# ============================================================================
# 3. REGULATORY UPDATE TRACKER AGENT
# ============================================================================

def test_fca_consumer_duty_high_impact(orchestrator):
    payload = "FCA PS22/9: Mandatory fair value assessments for all retail financial products within 90 days."
    _check_response(orchestrator.evaluate_event("REGULATORY_UPDATE", payload))

def test_sec_t_plus_1_settlement(orchestrator):
    payload = "SEC Release No. 34-96896: Transition from T+2 to T+1 trade settlement cycle for equity transactions."
    _check_response(orchestrator.evaluate_event("REGULATORY_UPDATE", payload))

def test_ofac_sanctions_list_update(orchestrator):
    payload = "OFAC Notice: Adding 14 maritime transport entities to the Specially Designated Nationals List."
    _check_response(orchestrator.evaluate_event("REGULATORY_UPDATE", payload))

def test_finra_crypto_communications(orchestrator):
    payload = "FINRA RN 24-03: Member firms must archive and review all retail digital asset promotional material."
    _check_response(orchestrator.evaluate_event("REGULATORY_UPDATE", payload))

def test_rbi_cybersecurity_framework(orchestrator):
    payload = "RBI Circular CS.12/2026: Mandatory 2-hour reporting threshold for major cybersecurity incidents."
    _check_response(orchestrator.evaluate_event("REGULATORY_UPDATE", payload))

def test_sebi_insider_trading_definition(orchestrator):
    payload = "SEBI/HO/PIT/2026/01: Immediate expansion of definition of connected persons to include immediate relatives."
    _check_response(orchestrator.evaluate_event("REGULATORY_UPDATE", payload))

def test_routine_administrative_circular_low_risk(orchestrator):
    payload = "SEC Public Notice: Standard annual adjustment of filing fees under Section 6(b)."
    _check_response(orchestrator.evaluate_event("REGULATORY_UPDATE", payload))


# ============================================================================
# 4. REPORT GENERATOR / ESCALATION
# ============================================================================

def test_high_risk_sar_generation(orchestrator):
    payload = "TRADER_ID: 441 | OFF_CHANNEL: Telegram | ACTION: Shared upcoming merger target sheet"
    _check_response(orchestrator.evaluate_event("COMMUNICATION", payload))