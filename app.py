from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    # Get user input safely
    user_input = request.data.decode("utf-8").strip()

    # If no input, return a default reply
    if not user_input:
        reply = "I didn’t receive any message. Please try again!"
    else:
        # Generate a simple reply
        reply = f"You said: {user_input}. Here’s my reply: Hello from your API!"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
