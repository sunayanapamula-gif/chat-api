from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder="static")

# Replace this with your current Cloudflare Tunnel URL
OLLAMA_URL = "https://impressive-echo-limitation-cities.trycloudflare.com"

@app.route("/")
def home():
    # Serve the frontend interface
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Forward the request to Ollama through Cloudflare Tunnel
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": "mistral", "prompt": user_message},
            stream=True,
            timeout=60
        )

        output = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = line.decode("utf-8")
                    output += data
                except Exception:
                    continue

        return jsonify({"reply": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Railway expects the app to listen on 0.0.0.0 and port 8080
    app.run(host="0.0.0.0", port=8080)
