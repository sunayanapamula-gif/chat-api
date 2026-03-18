from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if data and "message" in data:
        user_input = data["message"].strip()
    else:
        user_input = request.data.decode("utf-8").strip()

    if not user_input:
        reply = "I didn’t receive any message. Please try again!"
    elif "python" in user_input.lower():
        reply = """Here’s a Python example:

def greet(name):
    return f"Hello, {name}!"

print(greet("LinkedIn"))"""
    elif "javascript" in user_input.lower():
        reply = """Here’s a JavaScript example:

function greet(name) {
  return `Hello, ${name}!`;
}

console.log(greet("LinkedIn"));"""
    elif "sql" in user_input.lower():
        reply = """Here’s a SQL example:

CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(100)
);

INSERT INTO users (id, name) VALUES (1, 'LinkedIn');"""
    else:
        reply = f"You said: {user_input}. Here’s my reply: Hello from your API!"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
