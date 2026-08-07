import streamlit as st
import json
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env explicitly from the project root before importing orchestrator
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Add root folder to sys.path to allow direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.orchestrator import ComplianceOrchestrator

st.set_page_config(page_title="Meridian Compliance Monitor", layout="wide")
st.title("🛡️ Meridian Global Bank - AI Compliance Dashboard")

orchestrator = ComplianceOrchestrator(risk_threshold=0.7)

event_type = st.selectbox("Select Surveillance Domain", ["COMMUNICATION", "TRANSACTION", "REGULATORY_UPDATE"])

payload = {}

if event_type == "COMMUNICATION":
    user_input = st.text_area("Input Communication Log", "Let's move this conversation to WhatsApp to discuss the deal pricing")
    payload = {"text": user_input}

elif event_type == "REGULATORY_UPDATE":
    user_input = st.text_area("Input Regulatory Circular", "SEBI releases new guidelines restricting insider trading disclosures via unverified communication channels")
    payload = {"update_text": user_input}

elif event_type == "TRANSACTION":
    raw_json = st.text_area("Input Transaction Payload (JSON)", json.dumps({
        "account_id": "ACC-1092",
        "trader_id": "TRD-99",
        "orders": [{"type": "BUY", "qty": 100000, "status": "CANCELLED"}]
    }, indent=2))
    try:
        payload = json.loads(raw_json)
    except Exception:
        st.warning("Invalid JSON payload format.")
        payload = {}

if st.button("Run Compliance Analysis"):
    with st.spinner("Processing through multi-agent network..."):
        try:
            output = orchestrator.evaluate_event(event_type, payload)

            st.subheader("Analysis Result")
            if output["escalation_required"]:
                st.error("⚠️ HIGH RISK DETECTED - Escalation Required")
            else:
                st.success("✅ LOW RISK - Compliant")

            col1, col2 = st.columns(2)
            with col1:
                st.write("**Agent Output:**")
                st.json(output["agent_output"])

            with col2:
                st.write("**Generated Filing Draft:**")
                if output["report"]:
                    st.json(output["report"])
                else:
                    st.info("No formal filing generated (threshold not breached).")

        except Exception as e:
            st.error(f"Execution Error: {e}")