import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    
    # Call Ollama through ngrok
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": "mistral", "prompt": user_input},
        stream=True
    )

    # Collect Ollama’s reply
    reply = ""
    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8")
            reply += data

    return jsonify({"reply": reply})
