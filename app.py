from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# Use your actual Groq key here
GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

app = Flask(__name__)
CORS(app)  # Allow requests from your front-end

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload)
        res.raise_for_status()
        result = res.json()
        reply = result["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": reply})
    except requests.exceptions.RequestException as e:
        return jsonify({"reply": f"Error: Server unreachable ({str(e)})"}), 500
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
