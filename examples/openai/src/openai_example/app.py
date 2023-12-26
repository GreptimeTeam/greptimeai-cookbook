from flask import Flask, request

app = Flask(__name__)

from openai_example import audio_speech, chat_completion, image_create, tool_call


@app.route("/openai/chat", methods=["POST"])
def chat():
    json = request.json
    if not json:
        return "No json body provided"

    message: str = json.get("message", "")
    user_id: str = json.get("user_id", "")
    streaming: bool = json.get("streaming", False)
    raw: bool = json.get("raw", False)

    return chat_completion(message, user_id, raw, streaming)


@app.route("/openai/tool_call", methods=["POST"])
def tool():
    json = request.json
    if not json:
        return "No json body provided"

    user_id: str = json.get("user_id", "")

    return tool_call(user_id)


@app.route("/openai/audio/speech", methods=["POST"])
def audio():
    json = request.json
    if not json:
        return "No json body provided"

    message = json.get("message", "")
    user_id = json.get("user_id", "")

    return audio_speech(message, user_id)


@app.route("/openai/image/create", methods=["POST"])
def image():
    json = request.json
    if not json:
        return "No json body provided"

    user_id = json.get("user_id", "")

    return image_create(user_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
