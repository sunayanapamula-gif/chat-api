import os
import requests
import json
from flask import Flask, request, jsonify, render_template, Response

app = Flask(__name__)

# Read environment variable safely
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").strip()

# Sanity check: print values to logs
print(">>> OLLAMA_URL =", OLLAMA_URL)
print(">>> WEB_CONCURRENCY =", os.getenv("WEB_CONCURRENCY"))
print(">>> TIMEOUT =", os.getenv("TIMEOUT"))

# Serve index.html from templates folder
@app.route("/")
def index():
    return render_template("index.html")

# Chat route with streaming
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    def generate():
        try:
            with requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": "mistral", "prompt": user_input},
                stream=True,
                timeout=120
            ) as r:
                for line in r.iter_lines():
                    if line:
                        try:
                            obj = json.loads(line.decode("utf-8"))
                            yield obj.get("response", "")
                        except Exception:
                            pass
        except Exception as e:
            yield f"Error contacting Ollama: {str(e)}"

    return Response(generate(), mimetype="text/plain")

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
