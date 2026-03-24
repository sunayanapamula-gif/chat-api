import os
import requests
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Environment variables
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").strip()
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral:latest").strip()

print(">>> OLLAMA_URL =", OLLAMA_URL)
print(">>> OLLAMA_MODEL =", OLLAMA_MODEL)


@app.route("/")
def index():
    # Serve the chat interface
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "(no input)"})

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": user_input},
            stream=True,
            timeout=120
        )

        reply_parts = []
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                obj = json.loads(line)
                piece = obj.get("response", "")
                if piece:
                    reply_parts.append(piece)
            except Exception:
                continue

        reply = "".join(reply_parts).strip()
        if not reply:
            return jsonify({"reply": "(no response from Ollama)"})

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error contacting Ollama: {str(e)}"})


@app.route("/ping")
def ping():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        return jsonify({"status": "ok", "ollama_status": r.status_code})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
