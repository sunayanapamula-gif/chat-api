from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Replace with your current Cloudflare Tunnel URL
OLLAMA_URL = "https://impressive-echo-limitation-cities.trycloudflare.com"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": "mistral", "prompt": user_message},
            timeout=60
        )

        data = response.json()
        reply = data.get("response", "")  # ✅ extract the AI text

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
