import streamlit as st
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Create a mini Flask app inside Streamlit
app = Flask(__name__)
CORS(app)  # Allow requests from other domains

API_KEY = "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"

@app.route("/health-assistant", methods=["POST"])
def health_assistant():
    data = request.get_json()
    problem = data.get("problem")
    hours = data.get("hours", "0")

    if not problem:
        return jsonify({"reply": "No problem text provided!"})

    # Call Groq API
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a health assistant. Keep answers short and concise."},
            {"role": "user", "content": f"I have {problem} and I spent {hours} hours on this problem. Give me some advice to cure it."}
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

    return jsonify({"reply": reply})

# Run the Flask server inside Streamlit
if st.button("Start API Server"):
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)).start()
    st.success("API server running at http://localhost:5000/health-assistant")
