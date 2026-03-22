from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Replace this with your current Cloudflare Tunnel URL
OLLAMA_URL = "https://impressive-echo-limitation-cities.trycloudflare.com"

@app.route("/")
def home():
    # Render the frontend interface from templates/index.html
    return render_template("index.html")

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
    # Local dev run (Railway will use Gunicorn via Procfile)
    app.run(host="0.0.0.0", port=8080)
