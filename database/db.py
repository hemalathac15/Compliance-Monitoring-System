import sqlite3
import json
import hashlib
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "compliance_audit.db")

def init_db():
    """Initializes the SQLite audit database table with cryptographic tracking."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            agent_output TEXT NOT NULL,
            escalation_required INTEGER NOT NULL,
            report TEXT,
            prev_hash TEXT NOT NULL,
            current_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def _get_last_hash() -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT current_hash FROM audit_logs ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "0" * 64

def log_audit_record(event_type: str, payload: dict, agent_output: dict, escalation_required: bool, report: dict = None) -> str:
    """Inserts a tamper-evident record linked with SHA-256 hash chaining."""
    init_db()
    
    timestamp = datetime.utcnow().isoformat()
    prev_hash = _get_last_hash()
    
    payload_str = json.dumps(payload, sort_keys=True)
    agent_output_str = json.dumps(agent_output, sort_keys=True)
    report_str = json.dumps(report, sort_keys=True) if report else ""
    
    # Generate cryptographic signature for audit compliance
    raw_data = f"{timestamp}{event_type}{payload_str}{agent_output_str}{escalation_required}{report_str}{prev_hash}"
    current_hash = hashlib.sha256(raw_data.encode("utf-8")).hexdigest()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_logs (timestamp, event_type, payload, agent_output, escalation_required, report, prev_hash, current_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, event_type, payload_str, agent_output_str, 1 if escalation_required else 0, report_str, prev_hash, current_hash))
    
    conn.commit()
    conn.close()
    return current_hash

if __name__ == "__main__":
    init_db()
    h = log_audit_record("TEST", {"test": True}, {"status": "OK"}, False)
    print(f"Audit log recorded. SHA-256 Hash: {h}")