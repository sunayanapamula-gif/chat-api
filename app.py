from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# Ollama exposed via ngrok
OLLAMA_URL = "https://nonsuppressed-glottal-tonette.ngrok-free.dev/api/generate"

@app.route("/", methods=["POST"])
def root_chat():
    user_message = request.json.get("message", "")
    payload = {
        "model": "mistral:latest",
        "prompt": user_message,
        "stream": True
    }

    reply_text = ""
    try:
        # Forward request to ngrok Ollama endpoint
        res = requests.post(OLLAMA_URL, json=payload, stream=True)
        for line in res.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    reply_text += data["response"]
                if data.get("done", False):
                    break
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

    return jsonify({
        "model_url": OLLAMA_URL,
        "response": reply_text
    })

if __name__ == "__main__":
    # Railway sets PORT automatically
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
