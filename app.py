import os
import requests
import json
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

UI_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat API Interface</title>
    <style>
        #chat-box {
            border:1px solid #ccc;
            padding:10px;
            width:400px;
            height:300px;
            overflow-y:scroll;
        }
        .typing {
            font-style: italic;
            color: gray;
        }
    </style>
</head>
<body>
    <h2>Chat API Interface</h2>
    <div id="chat-box"></div>
    <input type="text" id="user-input" placeholder="Type your message..." style="width:300px;">
    <button onclick="sendMessage()">Send</button>

    <script>
        async function sendMessage() {
            const userMessage = document.getElementById("user-input").value;
            const chatBox = document.getElementById("chat-box");
            chatBox.innerHTML += "<p><b>You:</b> " + userMessage + "</p>";

            // Show typing indicator
            const typingIndicator = document.createElement("p");
            typingIndicator.className = "typing";
            typingIndicator.innerText = "Bot is typing...";
            chatBox.appendChild(typingIndicator);

            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            });
            const data = await response.json();

            // Remove typing indicator
            chatBox.removeChild(typingIndicator);

            // Typing animation
            const botReply = data.reply;
            let i = 0;
            const botLine = document.createElement("p");
            botLine.innerHTML = "<b>Bot:</b> ";
            chatBox.appendChild(botLine);

            function typeWriter() {
                if (i < botReply.length) {
                    botLine.innerHTML += botReply.charAt(i);
                    i++;
                    setTimeout(typeWriter, 30); // speed in ms per character
                    chatBox.scrollTop = chatBox.scrollHeight; // auto-scroll
                }
            }
            typeWriter();

            document.getElementById("user-input").value = "";
        }
    </script>
</body>
</html>
"""

# Serve UI directly at root URL
@app.route("/")
def index():
    return render_template_string(UI_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": "mistral", "prompt": user_input},
            stream=True,
            timeout=60
        )

        reply = ""
        for line in response.iter_lines():
            if line:
                try:
                    obj = json.loads(line.decode("utf-8"))
                    if "response" in obj:
                        reply += obj["response"]
                except Exception:
                    pass  # ignore malformed lines

        return jsonify({"reply": reply.strip()})
    except Exception as e:
        return jsonify({"reply": f"Error contacting Ollama: {str(e)}"})
