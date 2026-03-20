from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "I didn’t receive any message. Please try again!"})

    # Send request to Ollama local API
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "codellama:7b", "prompt": user_input}
    )

    reply = response.json().get("response", "No reply generated.")
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
