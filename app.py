import os
import requests
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").strip()
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral:latest").strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # ... (rest of your chat route code)
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
