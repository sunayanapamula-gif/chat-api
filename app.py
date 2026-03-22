import os
import requests
import json
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Read environment variable safely
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").strip()

# Sanity check: print values to logs
print(">>> OLLAMA_URL =", OLLAMA_URL)
print(">>> WEB_CONCURRENCY =", os.getenv("WEB_CONCURRENCY"))
print(">>> TIMEOUT =", os.getenv("TIMEOUT"))

# Simple HTML UI
UI_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat API Interface</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        #chat-box { border:1px solid #ccc; padding:10px; width:500px; height:350px; overflow-y:auto; background:#fff; }
        #input-box { margin-top:10px; }
        #message { width:400px; padding:8px; }
        button { padding:8px 14px; }
        .user { color:#333; margin:4px 0; }
        .bot { color:#0066cc; margin:4px 0; }
        .typing { font-style:italic; color:gray; margin:4px 0; }
    </style>
</head>
<body>
    <h1>Chat API Interface</h1>
    <div id="chat-box"></div>
    <div id="input-box">
        <input type="text" id="message" placeholder="Type your message..." />
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        async function sendMessage() {
            const msgInput = document.getElementById("message");
            const msg = msgInput.value.trim();
            if (!msg) return;

            const chatBox = document.getElementById("chat-box");
            chatBox.innerHTML += `<p class="user"><b>You:</b> ${msg}</p>`;
            chatBox.scrollTop = chatBox.scrollHeight;

            msgInput.value = "";

            const typingIndicator = document.createElement("p");
            typingIndicator.className = "typing";
            typingIndicator.innerText = "Bot is typing...";
            chatBox.appendChild(typingIndicator);
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const res = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: msg })
                });
                const data = await res.json();

                chatBox.removeChild(typingIndicator);
                chatBox.innerHTML += `<p class="bot"><b>Bot:</b> ${data.reply}</p>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (err) {
                chatBox.removeChild(typingIndicator);
                chatBox.innerHTML += `<p class="bot"><b>Error:</b> ${err}</p>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        }

        document.getElementById("message").addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

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
            timeout=60
        )

        reply = ""
        for line in response.text.splitlines():
            try:
                obj = json.loads(line)
                reply += obj.get("response", "")
            except Exception:
                pass

        return jsonify({"reply": reply.strip() or "(no response)"})
    except Exception as e:
        return jsonify({"reply": f"Error contacting Ollama: {str(e)}"})

# Health-check route
@app.route("/ping")
def ping():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        return jsonify({"status": "ok", "ollama_status": r.status_code})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)})
