from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            headers={"Content-Type": "application/json"},
            json={"model": OLLAMA_MODEL, "prompt": user_input},
            timeout=60
        )
        resp.raise_for_status()
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
