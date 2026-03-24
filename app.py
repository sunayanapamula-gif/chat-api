import os
import requests
import simplejson as json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # allow cross-origin requests from your frontend

# Update this each time you restart ngrok
OLLAMA_URL = "https://nonsuppressed-glottal-tonette.ngrok-free.dev"
OLLAMA_MODEL = "mistral:latest"

# Serve your chat board HTML at root
@app.route("/")
def home():
    return render_template("index.html")   # index.html goes in /templates

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
    data = request.get_json(force=True)
    user_input = data.get("message", "")

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": user_input
    }

    try:
        # Streaming request: Ollama sends JSON lines
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": "true"
            },
            stream=True   # important for streaming
        )

        if r.status_code != 200:
            return jsonify({"error": f"Ollama returned {r.status_code}"}), r.status_code

        reply = ""
        for line in r.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                try:
                    obj = json.loads(decoded)
                    if "response" in obj:
                        reply += obj["response"]
                except Exception:
                    # ignore malformed lines
                    continue

        return jsonify({"response": reply.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))   # Railway expects this
    app.run(host="0.0.0.0", port=port)
