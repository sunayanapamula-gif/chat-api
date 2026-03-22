import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Get Ollama/ngrok URL from environment
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

# Simple UI template
UI_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat API Interface</title>
</head>
<body>
    <h2>Chat API Interface</h2>
    <div id="chat-box" style="border:1px solid #ccc; padding:10px; width:400px; height:300px; overflow-y:scroll;"></div>
    <input type="text" id="user-input" placeholder="Type your message..." style="width:300px;">
    <button onclick="sendMessage()">Send</button>

    <script>
        async function sendMessage() {
            const userMessage = document.getElementById("user-input").value;
            document.getElementById("chat-box").innerHTML += "<p><b>You:</b> " + userMessage + "</p>";
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            });
            const data = await response.json();
            document.getElementById("chat-box").innerHTML += "<p><b>Bot:</b> " + data.reply + "</p>";
            document.getElementById("user-input").value = "";
        }
    </script>
</body>
</html>
"""

@app.route("/ui")
def ui():
    return render_template_string(UI_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    try:
        # Call Ollama through ngrok
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": "mistral", "prompt": user_input},
            stream=True,
            timeout=60
        )

        reply = ""
        for line in response.iter_lines():
            if line:
                reply += line.decode("utf-8")

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error contacting Ollama: {str(e)}"})
