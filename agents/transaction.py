import os 
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

class TransactionAnalysis(BaseModel):
    is_suspicious: bool = Field(description="True if transaction pattern indicates market abuse or structuring.")
    violation_type: str = Field(description="Type of violation detected(e.g., 'WASH_TRADING', 'SPOOFING', 'STRUCTURING', 'POSITION BREACH', 'NONE').")
    risk_score: float = Field(description="Risk/confidence score between 0.0 and 1.0.")
    flagged_entities: list[str] = Field(description="List of account IDs, trader IDs, or symbols involved.")
    explanation: str = Field(description="Detailed compliance reason and evidence for the classification.")
    recommended_action: str = Field(description="Action to take, e.g., 'BLOCK_TRADE', 'ESCALATE_TO_AML', 'LOG_ONLY'.")

def analyze_transaction(transaction_data: dict) -> dict:
    """
    Analyzes transaction patterns for market manipulation, structuring, or regulatory limit breaches.
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.0
    )

    structured_llm = llm.with_structured_output(TransactionAnalysis)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI Transaction Monitoring & Market Surveillance Specialist for a global bank."
                   "Analyze transaction data an order history for illegal patterns such as wash trading, spoofing,"
                   "structuring under AML thresholds, or position limit breaches."),
        ("human", "Analyze the following transaction record and execution history:\n\n{transaction_data}")
    ])

    chain = prompt | structured_llm

    # Convert input dict to formatted JSON string for prompt
    data_str = json.dumps(transaction_data, indent=2)

    result = chain.invoke({"transaction_data": data_str})
    return result.model_dump()

if __name__ == "__main__":
    sample_transaction = {
             "account_id": "ACC-882100",
             "trader_id": "TRD-004200",
             "symbol": "INDFX-DEC26",
             "order": [
                 {"time": "9:30:01", "type": "BUY_LIMIT", "qty": 5000, "price":100.50, "status": "CANCELLED"},
                 {"time": "9:30:02", "type": "BUY_LIMIT", "qty": 5000, "price":100.55, "status": "CANCELLED"},
                 {"time": "9:30:03", "type": "SELL_MARKET", "qty": 2000, "price":100.60, "status": "EXECUTED"}
             ],
             "cash_flow_pattern": "Multiple large buy orders placed and rapidly cancelled before executing a smaller sell order."
    }

    analysis = analyze_transaction(sample_transaction)
    print(json.dumps(analysis, indent=2))