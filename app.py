import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Hugging Face setup
HF_TOKEN = os.getenv("HF_TOKEN")  # set this in Railway variables
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"reply": "(no input)"})

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": user_input,
        "parameters": {"max_new_tokens": 200}
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()

        # Hugging Face returns a list with generated_text
        if isinstance(result, list) and "generated_text" in result[0]:
            reply = result[0]["generated_text"]
        else:
            reply = str(result)

        return jsonify({"reply": reply.strip()})
    except Exception as e:
        return jsonify({"reply": f"Error contacting Hugging Face: {str(e)}"})

@app.route("/ping")
def ping():
    try:
        r = requests.get(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            timeout=10
        )
        return jsonify({"status": "ok", "hf_status": r.status_code})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
