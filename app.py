from flask import Flask, request

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.data.decode("utf-8")
    return f"Echo: {user_input}"

if __name__ == "__main__":
    print("Server listening on port 8080")
    app.run(host="0.0.0.0", port=8080)