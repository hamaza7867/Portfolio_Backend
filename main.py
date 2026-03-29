from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from ai_engine import AIEngine
from mailer import Mailer

app = FastAPI()
ai = AIEngine()
mailer = Mailer()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your portfolio domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ReportRequest(BaseModel):
    user_name: str
    user_email: str
    project_type: str
    budget_est: str
    chat_summary: str

@app.get("/")
def health_check():
    return {"status": "online", "message": "Portfolio AI Assistant is running."}

@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    try:
        # Convert Pydantic models to dicts for Groq
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        response = ai.get_response(messages)
        
        # Analyze budget briefly for frontend tracking
        budget_tip = ai.analyze_budget(messages[-1]['content'])
        
        return {"response": response, "budget_tip": budget_tip}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/report")
def send_report(request: ReportRequest):
    try:
        response = mailer.send_report(
            request.user_name,
            request.user_email,
            request.project_type,
            request.budget_est,
            request.chat_summary
        )
        if response:
            return {"status": "success", "message": "Report sent to Ali Hamza."}
        else:
            raise HTTPException(status_code=500, detail="Failed to send report. Check Resend logs.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
