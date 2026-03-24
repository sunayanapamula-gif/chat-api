import os
import subprocess
import threading
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Configuration
OLLAMA_MODEL = "mistral:latest"
# If you’re exposing Ollama via ngrok, put your forwarding URL here
# Example: "https://nonsuppressed-glottal-tonette.ngrok-free.dev"
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

# Start Ollama process once (using run mode, not serve)
ollama_proc = subprocess.Popen(
    ["ollama", "run", OLLAMA_MODEL],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

ollama_lock = threading.Lock()

def ask_ollama(prompt: str) -> str:
    with ollama_lock:
        ollama_proc.stdin.write(prompt + "\n")
        ollama_proc.stdin.flush()

        reply_lines = []
        while True:
            line = ollama_proc.stdout.readline()
            if not line:
                break
            reply_lines.append(line.strip())
            if line.strip() == "":
                break

        return " ".join(reply_lines).strip()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ping", methods=["GET"])
def ping():
    try:
        reply = ask_ollama("ping")
        return jsonify({"status": "ok", "ollama_reply": reply, "model_url": OLLAMA_URL})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_input = data.get("message", "")

    try:
        reply = ask_ollama(user_input)
        return jsonify({"response": reply, "model_url": OLLAMA_URL})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
