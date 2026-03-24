import os
import subprocess
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

OLLAMA_MODEL = "mistral:latest"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ping", methods=["GET"])
def ping():
    try:
        # Try a simple run to see if Ollama responds
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input="ping".encode("utf-8"),
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            return jsonify({"status": "ok", "ollama_status": 200})
        else:
            return jsonify({"status": "error", "ollama_status": result.returncode}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_input = data.get("message", "")

    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=user_input.encode("utf-8"),
            capture_output=True,
            timeout=60
        )

        if result.returncode != 0:
            return jsonify({"error": f"Ollama failed with code {result.returncode}"}), 500

        reply = result.stdout.decode("utf-8").strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
