from fastapi import FastAPI
from pydantic import BaseModel
import requests

API_KEY = "YOUR_GROQ_API_KEY"

app = FastAPI(title="Health Assistant API")

class ProblemRequest(BaseModel):
    problem: str
    hours: int = 0

@app.post("/health-assistant")
def health_assistant(req: ProblemRequest):
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a health assistant. Keep answers short and concise."},
            {"role": "user", "content": f"I have {req.problem} and I spent {req.hours} hours on this problem. Give me some advice to cure it."}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        json=payload
    ).json()

    try:
        reply = response['choices'][0]['message']['content']
    except Exception:
        reply = "Error: Could not get AI response"

    return {"reply": reply}
