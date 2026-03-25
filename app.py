from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Point directly to your local Ollama server
OLLAMA_URL = "http://localhost:8080/api/generate"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    payload = {
        "model": "mistral:latest",
        "prompt": user_message,
        "stream": True
    }

    reply_text = ""
    try:
        res = requests.post(OLLAMA_URL, json=payload, stream=True)
        for line in res.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    reply_text += data["response"]
                if data.get("done", False):
                    break
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

    return jsonify({"response": reply_text})
