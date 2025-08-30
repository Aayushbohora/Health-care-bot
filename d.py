from flask import Flask, request, jsonify
import requests
import speech_recognition as sr

app = Flask(__name__)

# Your Groq API key
API_KEY = "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"

@app.route("/health-assistant", methods=["POST"])
def health_assistant():
    """
    Expects JSON:
    {
      "problem": "headache",
      "hours": "2"
    }
    """
    data = request.get_json()

    problem = data.get("problem")
    hours = data.get("hours", "0")

    # Call Groq API
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a health assistant. Keep answers short and concise."},
                {"role": "user", "content": f"I have {problem} and I spent {hours} hours on this problem. Give me some advice to cure it."}
            ]
        }
    ).json()

    try:
        reply = response['choices'][0]['message']['content']
    except Exception:
        reply = "Error: Unexpected API response"
    
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
