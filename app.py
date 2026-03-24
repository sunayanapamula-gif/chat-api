import os
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Configuration
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = "mistral:latest"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ping", methods=["GET"])
def ping():
    try:
        res = requests.post(f"{OLLAMA_URL}/api/generate",
                            json={"model": OLLAMA_MODEL, "prompt": "ping"})
        reply = res.json().get("response", "")
        return jsonify({"status": "ok", "ollama_reply": reply, "model_url": OLLAMA_URL})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_input = data.get("message", "")

    try:
        res = requests.post(f"{OLLAMA_URL}/api/generate",
                            json={"model": OLLAMA_MODEL, "prompt": user_input})
        reply = res.json().get("response", "")
        return jsonify({"response": reply, "model_url": OLLAMA_URL})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
