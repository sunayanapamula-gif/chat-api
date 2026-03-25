<!DOCTYPE html>
<html>
<head>
    <title>🍊 Orange Chat Board</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: linear-gradient(to bottom, #e0f7fa, #ffffff); text-align: center; transition: background 0.5s ease; }
        h1 { margin-bottom: 15px; }

        #chat-box { 
            border: 8px solid #ff8c00; border-radius: 50%; 
            background: radial-gradient(circle at center, #ffa500 55%, #ffcc80 100%);
            width: 420px; height: 420px; margin: auto; padding: 20px; 
            overflow-y: auto; color: #333; position: relative;
            box-shadow: 0 0 30px rgba(255,140,0,0.6), inset 0 0 20px rgba(255,255,255,0.4);
            transition: background 0.5s ease, box-shadow 0.5s ease;
        }

        .glossy { position: absolute; top: 10%; left: 15%; width: 60%; height: 30%; background: radial-gradient(circle at top left, rgba(255,255,255,0.8), transparent 70%); border-radius: 50%; opacity: 0.7; pointer-events: none; }

        .user { background: #ff7043; color: #fff; padding: 8px 12px; border-radius: 16px; margin: 8px auto; text-align: right; font-size: 14px; display: block; max-width: 80%; box-shadow: 0 2px 6px rgba(0,0,0,0.2); }
        .ai { background: #fff3e0; color: #222; padding: 8px 12px; border-radius: 16px; margin: 8px auto; text-align: left; font-size: 14px; display: block; max-width: 80%; box-shadow: 0 2px 6px rgba(0,0,0,0.2); }
        .typing { font-style: italic; color: #ff8c00; margin: 6px auto; text-align: left; display: block; }

        #input-box { margin-top: 15px; display: flex; gap: 8px; max-width: 420px; margin-left: auto; margin-right: auto; }
        #message { flex: 1; padding: 8px; border-radius: 8px; border: 1px solid #ccc; font-size: 14px; }
        button { padding: 8px 14px; background: #ff8c00; color: #fff; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
        button:hover { background: #e67e22; }

        #code-panel { position: fixed; top: 0; left: -500px; width: 400px; height: 100%; background: #2d2d2d; color: #f8f8f2; box-shadow: 4px 0 12px rgba(0,0,0,0.3); padding: 20px; overflow-y: auto; transition: all 0.6s ease; opacity: 0; z-index: 999; }
        #code-panel.show { left: 0; opacity: 1; }
        #close-btn, #normal-btn, #clear-btn { background: #ff8c00; color: #fff; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-weight: bold; margin: 5px; }
        #close-btn:hover, #normal-btn:hover, #clear-btn:hover { background: #e67e22; }

        pre { background: #1e1e1e; padding: 12px; border-radius: 8px; font-size: 13px; font-family: Consolas, monospace; text-align: left; white-space: pre-wrap; word-wrap: break-word; line-height: 1.4; }
    </style>
</head>
<body>
    <h1>🍊 Orange Chat Board</h1>
    <div id="chat-box"><div class="glossy"></div></div>
    <div id="input-box">
        <input type="text" id="message" placeholder="Type your message..." />
        <button onclick="sendMessage()">Send</button>
    </div>

    <div id="code-panel">
        <button id="close-btn" onclick="closeCode()">Close ✖</button>
        <button id="clear-btn" onclick="clearAppear()">Clear Appear</button>
        <button id="normal-btn" onclick="backToNormal()">Back to Normal</button>
        <pre id="code-content"></pre>
    </div>

    <script>
        const msgInput = document.getElementById("message");
        const chatBox = document.getElementById("chat-box");

        msgInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
            }
        });

        async function sendMessage() {
            const msg = msgInput.value.trim();
            if (!msg) return;

            const userBubble = document.createElement("div");
            userBubble.className = "user";
            userBubble.innerHTML = "🥺 " + msg;
            chatBox.appendChild(userBubble);

            msgInput.value = "";

            const typingBubble = document.createElement("div");
            typingBubble.className = "typing";
            typingBubble.innerHTML = "🤖 AI is thinking...";
            chatBox.appendChild(typingBubble);
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const res = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: msg })
                });
                const data = await res.json();

                chatBox.removeChild(typingBubble);

                const aiBubble = document.createElement("div");
                aiBubble.className = "ai";
                aiBubble.innerHTML = "🍊 " + (data.response || "(no reply)");
                chatBox.appendChild(aiBubble);
                chatBox.scrollTop = chatBox.scrollHeight;

                // If the reply looks like code, also show in code panel
                if (msg.toLowerCase().includes("code")) {
                    showCodePanel(data.response);
                }
            } catch (err) {
                chatBox.removeChild(typingBubble);
                const aiBubble = document.createElement("div");
                aiBubble.className = "ai";
                aiBubble.innerHTML = "🍊 Error: " + err.message;
                chatBox.appendChild(aiBubble);
            }
        }

        function showCodePanel(reply) {
            const codePanel = document.getElementById("code-panel");
            const codeContent = document.getElementById("code-content");
            codeContent.textContent = reply;
            codePanel.classList.add("show");
        }

        function closeCode() {
            document.getElementById("code-panel").classList.remove("show");
        }

        function clearAppear() {
            const codePanel = document.getElementById("code-panel");
            codePanel.style.opacity = "0";
            setTimeout(() => { codePanel.style.opacity = "1"; }, 600);
        }

        function backToNormal() {
            const codePanel = document.getElementById("code-panel");
            const codeContent = document.getElementById("code-content");
            codeContent.textContent = "";
            codePanel.classList.remove("show");
            codePanel.style.opacity = "0";
        }
    </script>
</body>
</html>
