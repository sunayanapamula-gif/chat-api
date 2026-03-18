from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    # Try to parse JSON first
    data = request.get_json(silent=True)
    if data and "message" in data:
        user_input = data["message"].strip()
    else:
        # Fallback: check form data or raw text
        user_input = request.form.get("message") or request.data.decode("utf-8").strip()

    if not user_input:
        reply = "I didn’t receive any message. Please try again!"
    elif "code" in user_input.lower():
        reply = """Here’s a sample Python code:

def greet(name):
    return f"Hello, {name}!"

print(greet("LinkedIn"))"""
    else:
        reply = f"You said: {user_input}. Here’s my reply: Hello from your API!"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
