import os

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        # Mocked reply for Railway
        return jsonify({"reply": f"Mocked reply for: {user_input}"})
    else:
        # Local Ollama call
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
