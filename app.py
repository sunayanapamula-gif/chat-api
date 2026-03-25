import os
import json
import requests
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Configuration
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")   # Ollama server
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral:latest")      # default model

@app.route("/")
def home():
    # Serve index.html from templates folder
    return render_template("index.html")

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "Server is alive"})

@app.route("/chat", methods=["POST"])
def chat():
    """Collect full response from Ollama and return JSON"""
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
                    if j.get("done"):
                        break
                except Exception:
                    pass

        return jsonify({
            "response": reply_text.strip(),
            "model_url": OLLAMA_URL,
            "model": OLLAMA_MODEL
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    """Stream response chunks to frontend for live typing effect"""
    data = request.get_json(force=True)
    user_input = data.get("message", "")

    def generate():
        try:
            res = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": user_input},
                stream=True
            )
            for line in res.iter_lines():
                if line:
                    try:
                        j = json.loads(line.decode("utf-8"))
                        if "response" in j:
                            yield j["response"]
                    except Exception:
                        pass
        except Exception as e:
            yield f"Error: {str(e)}"

    return Response(generate(), mimetype="text/plain")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
