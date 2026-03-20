from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Root route just to confirm the app is running
@app.route("/")
def home():
    return "Hello, Flask is running on Railway!"

# Chat route that connects to Ollama
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "I didn’t receive any message. Please try again!"})

    try:
        # Send request to Ollama local API
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "codellama:7b", "prompt": user_input}
        )

        # Extract reply from Ollama response
        reply = response.json().get("response", "No reply generated.")
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Run Flask in dev mode locally
    app.run(host="0.0.0.0", port=8080)
