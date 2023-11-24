from flask import Flask, request

app = Flask(__name__)

from openai_example import (
    audio_speech,
    audio_transcription,
    audio_translation,
    chat_completion,
)


@app.route("/openai/chat", methods=["POST"])
def chat():
    json = request.json
    message = json.get("message", "")
    user_id = json.get("user_id", "")

    return chat_completion(message, user_id)


@app.route("/openai/audio/<scenario>", methods=["POST"])
def audio(scenario: str):
    json = request.json
    message = json.get("message", "")
    user_id = json.get("user_id", "")

    if scenario == "speech":
        return audio_speech(message, user_id)
    elif scenario == "transcription":
        return audio_transcription(message, user_id)
    elif scenario == "translation":
        return audio_translation(message, user_id)
    else:
        return f"Unknown scenario {scenario}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
