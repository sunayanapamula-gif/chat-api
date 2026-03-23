import os
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow browser clients

# Hugging Face setup
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "(no input)"})

    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    payload = {
        "inputs": user_input,
        "parameters": {"max_new_tokens": 200}
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()

        # Hugging Face returns a list with generated_text
        if isinstance(result, list) and "generated_text" in result[0]:
            reply = result[0]["generated_text"]
        else:
            reply = str(result)

        return jsonify({"reply": reply.strip()})
    except requests.exceptions.RequestException as e:
        return jsonify({"reply": f"Error contacting Hugging Face: {str(e)}"})
    except Exception as e:
        return jsonify({"reply": f"Unexpected error: {str(e)}"})

@app.route("/ping")
def ping():
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    try:
        r = requests.get(HF_API_URL, headers=headers, timeout=10)
        return jsonify({"status": "ok", "hf_status": r.status_code})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
