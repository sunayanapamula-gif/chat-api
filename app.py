import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

OLLAMA_URL = "https://nonsuppressed-glottal-tonette.ngrok-free.dev"
OLLAMA_MODEL = "mistral:latest"

@app.route("/")
def home():
    return "OK"

@app.route("/ping", methods=["GET"])
def ping():
    try:
        r = requests.get(
            f"{OLLAMA_URL}/api/tags",
            headers={"ngrok-skip-browser-warning": "true"}
        )
        return jsonify({"status": "ok", "ollama_status": r.status_code})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": user_input
    }

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": "true"
            },
            stream=True
        )

        output = ""
        for line in r.iter_lines():
            if line:
                try:
                    chunk = line.decode("utf-8")
                    output += chunk
                except Exception:
                    pass

        return jsonify({"response": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
