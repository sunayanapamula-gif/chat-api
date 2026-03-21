import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": user_input},
        stream=True
    )

    output = ""
    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8")
            if "\"response\"" in data:
                part = data.split("\"response\":\"")[1].split("\"")[0]
                output += part

    return jsonify({"reply": output})
