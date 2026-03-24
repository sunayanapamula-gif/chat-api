import os
import requests
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")

# Ollama backend settings
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").strip()
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral").strip()

print(">>> OLLAMA_URL =", OLLAMA_URL)
print(">>> OLLAMA_MODEL =", OLLAMA_MODEL)

# Serve the frontend
@app.route("/")
def index():
    return render_template("index.html")

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"reply": "(no input)"})

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": user_input},
            stream=True,
            timeout=120
        )

        reply = ""
        for line in response.iter_lines():
            if not line:
                continue
            try:
                obj = json.loads(line.decode("utf-8"))
                reply += obj.get("response", "")
            except Exception:
                continue

        if not reply.strip():
            return jsonify({"reply": "(no response from Ollama)"})

        return jsonify({"reply": reply.strip()})

    except Exception as e:
        return jsonify({"reply": f"Error contacting Ollama: {str(e)}"})

# Health check
@app.route("/ping")
def ping():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        return jsonify({"status": "ok", "ollama_status": r.status_code})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)})

if __name__ == "__main__":
    # Run on port 8080 so ngrok can tunnel it
    app.run(host="0.0.0.0", port=8080)
