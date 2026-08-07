import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class RegulatoryAnalysis(BaseModel):
    impact_level: str = Field(description="Impact level: HIGH, MEDIUM, LOW, or NONE.")
    summary: str = Field(description="Brief summary of regulatory changes.")
    affected_operations: list[str] = Field(description="List of banking domains affected.")
    risk_score: float = Field(description="Risk score between 0.0 and 1.0.")
    recommended_policy_updates: list[str] = Field(description="Policy change recommendations.")

def analyze_regulatory(update_text: str) -> dict:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.0
    )
    
    structured_llm = llm.with_structured_output(RegulatoryAnalysis)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Regulatory Compliance Intelligence Specialist."),
        ("human", "Analyze the following regulatory circular or update:\n\n{update_text}")
    ])
    
    chain = prompt | structured_llm
    
    # Handle dict or string payload inputs safely
    text_content = update_text.get("update_text", "") if isinstance(update_text, dict) else update_text
    
    result = chain.invoke({"update_text": text_content})
    return result.model_dump()