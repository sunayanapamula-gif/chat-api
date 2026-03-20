from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask is running on Railway!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "I didn’t receive any message. Please try again!"})

    # Check environment: Railway vs Local
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        # Mock response for Railway (no Ollama available in cloud)
        return jsonify({
            "reply": f"(Mocked reply) You asked: '{user_input}'. "
                     f"Since Ollama runs locally, here’s a placeholder response."
        })
    else:
        # Real Ollama integration for local testing
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "codellama:7b", "prompt": user_input}
            )
            reply = response.json().get("response", "No reply generated.")
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
