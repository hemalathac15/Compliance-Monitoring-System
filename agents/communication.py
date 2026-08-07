import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class CommunicationAnalysis(BaseModel):
    is_suspicious: bool = Field(description="True if off-channel communication, record deletion, or market manipulation is detected.")
    violation_type: str = Field(description="Type of violation, e.g., OFF_CHANNEL_COMMUNICATION, RECORD_TAMPERING, NONE.")
    risk_score: float = Field(description="Risk score between 0.0 and 1.0. Set >= 0.8 for off-channel messaging attempts.")
    flagged_entities: list[str] = Field(description="Channels, messaging apps, or key terms flagged.")
    explanation: str = Field(description="Detailed compliance assessment.")
    recommended_action: str = Field(description="Recommended compliance step.")

def analyze_communication(text: str) -> dict:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.0
    )
    
    structured_llm = llm.with_structured_output(CommunicationAnalysis)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert financial compliance officer. Analyze employee communications for unauthorized off-channel messaging (e.g., WhatsApp, Signal, Telegram), insider trading, or collusion."),
        ("human", "Analyze this message:\n\n{text}")
    ])
    
    chain = prompt | structured_llm
    result = chain.invoke({"text": text})
    return result.model_dump()