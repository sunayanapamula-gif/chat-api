from flask import Response

@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    data = request.get_json(force=True)
    user_input = data.get("message", "")

    def generate():
        res = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": user_input},
            stream=True
        )
        for line in res.iter_lines():
            if line:
                try:
                    j = json.loads(line.decode("utf-8"))
                    if "response" in j:
                        yield j["response"]
                except Exception:
                    pass

    return Response(generate(), mimetype="text/plain")
