"""
Neuro Shield - Cybersecurity AI Backend
Handles: AI chat via Ollama, threat metrics, chat history, session management
"""
 
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
import datetime
import uuid
import json
import os
 
app = FastAPI(title="Neuro Shield Backend", version="1.0.0")
 
# ---------------------- CORS ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# ---------------------- CONFIG ----------------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "mistral")
 
SYSTEM_PROMPT = """
You are Neuro Shield, an elite AI-powered cybersecurity expert assistant.
Your capabilities include:
- Threat analysis and vulnerability assessment
- Malware identification and reverse engineering guidance
- Network intrusion detection advice
- Security hardening best practices
- CVE/exploit explanations
- OWASP Top 10 guidance
- Incident response procedures
- Penetration testing methodology
 
Always respond in a professional, structured format.
Use bullet points, code blocks, and clear headings where appropriate.
Flag critical security risks with [CRITICAL], high risks with [HIGH], medium with [MEDIUM].
Never provide actual malicious code or assist with illegal activities.
"""
 
# ---------------------- IN-MEMORY STORAGE ----------------------
# Replace with a real DB (PostgreSQL / MongoDB) in production
 
chat_sessions: dict = {}       # session_id -> list of messages
threat_log: list = []          # list of detected threat events
 
# Simulated live threat counters (replace with real IDS/SIEM integration)
threat_stats = {
    "detected_today": 1243,
    "blocked_attacks": 987,
    "active_alerts": 23,
    "last_updated": datetime.datetime.utcnow().isoformat()
}
 
# ---------------------- SCHEMAS ----------------------
 
class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    user_id: Optional[str] = "anonymous"
 
class ChatMessage(BaseModel):
    role: str           # "user" | "assistant"
    content: str
    timestamp: str
 
class ChatResponse(BaseModel):
    session_id: str
    reply: str
    timestamp: str
    model: str
    history: List[ChatMessage]
 
class ThreatStats(BaseModel):
    detected_today: int
    blocked_attacks: int
    active_alerts: int
    last_updated: str
 
class ThreatEvent(BaseModel):
    type: str           # e.g. "SQL Injection", "Port Scan"
    severity: str       # "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
    source_ip: Optional[str] = "0.0.0.0"
    details: str
 
# ---------------------- HELPERS ----------------------
 
def get_or_create_session(session_id: Optional[str]) -> str:
    if not session_id or session_id not in chat_sessions:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = []
    return session_id
 
 
def build_ollama_prompt(history: list, new_message: str) -> str:
    """Build a single prompt string from chat history for Ollama."""
    conversation = SYSTEM_PROMPT + "\n\n"
    for msg in history[-10:]:   # keep last 10 turns for context window
        if msg["role"] == "user":
            conversation += f"User: {msg['content']}\n"
        else:
            conversation += f"Assistant: {msg['content']}\n"
    conversation += f"User: {new_message}\nAssistant:"
    return conversation
 
 
def query_ollama(prompt: str) -> str:
    """Send prompt to local Ollama instance and get response."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 1024
                }
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "No response from model.")
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama service is not running. Start it with: ollama serve"
        )
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Model response timed out.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")
    

    #--------------------------------------------------------
    elif page == "settings":

    st.subheader("⚙ Neuro Shield Settings")

    temperature = st.slider("Model Temperature", 0.0, 1.0, 0.7)

    max_tokens = st.slider("Max Tokens", 100, 2000, 1024)

    theme = st.selectbox(
        "Theme Mode",
        ["Cyber Dark", "Matrix Green", "Blue Neon"]
    )

    st.button("Save Settings")

    st.markdown("""
    **Description**

    • Temperature controls creativity of AI  
    • Max Tokens controls response length  
    • Theme changes UI appearance
    """)
 
# ---------------------- ROUTES ----------------------
 
@app.get("/")
def root():
    return {
        "name": "Neuro Shield Backend",
        "status": "online",
        "model": MODEL_NAME,
        "version": "1.0.0"
    }
 
 
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Main chat endpoint.
    Accepts a message, maintains session history, returns AI reply.
    """
    session_id = get_or_create_session(req.session_id)
    history = chat_sessions[session_id]
 
    # Build prompt with history
    prompt = build_ollama_prompt(history, req.message)
    reply = query_ollama(prompt)
 
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
 
    # Save to session
    db = SessionLocal()

user_msg = ChatDB(
    id=str(uuid.uuid4()),
    session_id=session_id,
    role="user",
    content=req.message,
    timestamp=timestamp
)

ai_msg = ChatDB(
    id=str(uuid.uuid4()),
    session_id=session_id,
    role="assistant",
    content=reply,
    timestamp=timestamp
)

db.add(user_msg)
db.add(ai_msg)
db.commit()
db.close()
 
    return ChatResponse(
        session_id=session_id,
        reply=reply,
        timestamp=timestamp,
        model=MODEL_NAME,
        history=[ChatMessage(**m) for m in history]
    )
 
 
@app.get("/chat/{session_id}/history", response_model=List[ChatMessage])
def get_history(session_id: str):
    """Retrieve full chat history for a session."""
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found.")
    return [ChatMessage(**m) for m in chat_sessions[session_id]]
 
 
@app.delete("/chat/{session_id}")
def clear_session(session_id: str):
    """Clear a chat session."""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
    return {"status": "cleared", "session_id": session_id}
 
 
@app.get("/sessions")
def list_sessions():
    """List all active sessions with message counts."""
    return {
        sid: {"message_count": len(msgs)}
        for sid, msgs in chat_sessions.items()
    }
 
 
@app.get("/threats/stats", response_model=ThreatStats)
def get_threat_stats():
    """
    Returns live threat dashboard metrics.
    Replace the simulated values with real IDS/SIEM data in production.
    """
    return ThreatStats(**threat_stats)
 
 
@app.post("/threats/log")
def log_threat(event: ThreatEvent):
    """
    Log a new detected threat event.
    In production, connect this to your IDS (Snort/Suricata) or SIEM webhook.
    """
    entry = {
        "id": str(uuid.uuid4()),
        "type": event.type,
        "severity": event.severity,
        "source_ip": event.source_ip,
        "details": event.details,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    threat_log.append(entry)
 
    # Update counters
    threat_stats["detected_today"] += 1
    if event.severity in ("CRITICAL", "HIGH"):
        threat_stats["active_alerts"] += 1
    threat_stats["last_updated"] = datetime.datetime.utcnow().isoformat()
 
    return {"status": "logged", "event_id": entry["id"]}
 
 
@app.get("/threats/log")
def get_threat_log(limit: int = 50):
    """Retrieve recent threat log entries."""
    return threat_log[-limit:]
 
 
@app.get("/models")
def list_models():
    """List available Ollama models."""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        resp.raise_for_status()
        models = [m["name"] for m in resp.json().get("models", [])]
        return {"models": models, "active": MODEL_NAME}
    except Exception:
        return {"models": [], "active": MODEL_NAME, "error": "Could not reach Ollama"}
 
 
@app.get("/health")
def health_check():
    """Health check for the backend and Ollama connection."""
    ollama_ok = False
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        ollama_ok = r.status_code == 200
    except Exception:
        pass
 
    return {
        "backend": "online",
        "ollama": "online" if ollama_ok else "offline",
        "model": MODEL_NAME,
        "active_sessions": len(chat_sessions),
        "threats_logged": len(threat_log),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
 #---------------------------------------------------------
 chat_sessions: dict = {}
 
# ---------------------- ENTRY POINT ----------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
    #----------------------------------------------------------------------

from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///neuroshield.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class ChatDB(Base):
    __tablename__ = "chat_history"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String)
    role = Column(String)
    content = Column(Text)
    timestamp = Column(String)

Base.metadata.create_all(bind=engine)