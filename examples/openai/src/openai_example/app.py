from flask import Flask, request

app = Flask(__name__)

from openai_example import chat_completion


@app.route("/openai/<scenario>", methods=["POST"])
def run(scenario: str):
    json = request.json
    message = json.get("message", "")
    user_id = json.get("user_id", "")

    return chat_completion(message, user_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
