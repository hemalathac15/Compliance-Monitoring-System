import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

class ComplianceReport(BaseModel):
    report_type: str = Field(description="Type of filing, e.g., 'SAR', 'STR', 'INTERNAL_AUDIT', 'SEBI_INCIDENT_REPORT'.")
    severity: str = Field(description="Severity classification: HIGH, MEDIUM, or LOW.")
    executive_summary: str = Field(description="High-level narrative explaining the violation or event.")
    involved_parties: list[str] = Field(description="List of accounts, traders, or entities flagged.")
    regulatory_frameworks: list[str] = Field(description="Applicable rules breached, e.g., ['SEC Rule 17a-4', 'SEBI PIT', 'RBI KYC'].")
    recommended_next_steps: list[str] = Field(description="List of action items for compliance officers or regulators.")

def generate_report(flagged_data: dict) -> dict:
    """
    Compiles flagged findings from agents into an audit-ready compliance report.
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.0
    )
    
    structured_llm = llm.with_structured_output(ComplianceReport)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI Regulatory Report Generator for a global financial institution. "
                   "Draft formal, audit-ready compliance filings based on structured agent evaluations."),
        ("human", "Generate a compliance report based on these flagged findings:\n\n{flagged_data}")
    ])
    
    chain = prompt | structured_llm
    data_str = json.dumps(flagged_data, indent=2)
    
    result = chain.invoke({"flagged_data": data_str})
    return result.model_dump()

if __name__ == "__main__":
    sample_finding = {
        "source_agent": "TransactionMonitor",
        "violation": "SPOOFING",
        "confidence": 0.92,
        "details": "Account ACC-88210 placed and cancelled high-volume buy limit orders to inflate perceived market demand."
    }
    report = generate_report(sample_finding)
    print(json.dumps(report, indent=2))