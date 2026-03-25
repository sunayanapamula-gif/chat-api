import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Configuration
OLLAMA_URL = os.environ.get("OLLAMA_URL", "https://nonsuppressed-glottal-tonette.ngrok-free.dev")
OLLAMA_MODEL = "mistral:latest"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ping", methods=["GET"])
def ping():
    try:
        res = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": "ping"},
            stream=True
        )
        reply_text = ""
        for line in res.iter_lines():
            if line:
                try:
                    j = json.loads(line.decode("utf-8"))
                    if "response" in j:
                        reply_text += j["response"]
                except:
                    pass
        return jsonify({"status": "ok", "ollama_reply": reply_text.strip(), "model_url": OLLAMA_URL})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_input = data.get("message", "")

    try:
        res = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": user_input},
            stream=True
        )

        reply_text = ""
        for line in res.iter_lines():
            if line:
                try:
                    j = json.loads(line.decode("utf-8"))
                    if "response" in j:
                        reply_text += j["response"]
                except:
                    pass

        return jsonify({"response": reply_text.strip(), "model_url": https://nonsuppressed-glottal-tonette.ngrok-free.dev})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
