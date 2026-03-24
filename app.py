import os
import requests
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Read environment variables safely
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").strip()
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral").strip()

# Sanity check: print values to logs
print(">>> OLLAMA_URL =", OLLAMA_URL)
print(">>> OLLAMA_MODEL =", OLLAMA_MODEL)
print(">>> WEB_CONCURRENCY =", os.getenv("WEB_CONCURRENCY"))
print(">>> TIMEOUT =", os.getenv("TIMEOUT"))

# Serve index.html from templates folder
@app.route("/")
def index():
    return render_template("index.html")

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"reply": "(no input)"})

    try:
        # Call Ollama through Cloudflare Tunnel or local
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

# Health-check route
@app.route("/ping")
def ping():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        return jsonify({"status": "ok", "ollama_status": r.status_code})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)})

if __name__ == "__main__":
    # Local dev server
    app.run(host="0.0.0.0", port=8080)
