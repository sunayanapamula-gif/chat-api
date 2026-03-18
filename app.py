from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.data.decode("utf-8").strip()

    # If no input, return a default reply
    if not user_input:
        reply = "I didn’t receive any message. Please try again!"
    elif "code" in user_input.lower():
        # Generate a simple Python code snippet
        reply = """Here’s a sample Python code:

def greet(name):
    return f"Hello, {name}!"

print(greet("LinkedIn"))"""
    else:
        # Normal reply
        reply = f"You said: {user_input}. Here’s my reply: Hello from your API!"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
