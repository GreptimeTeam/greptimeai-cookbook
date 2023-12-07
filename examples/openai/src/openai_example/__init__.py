import logging

from greptimeai import openai_patcher

from openai import OpenAI

logging.basicConfig(level=logging.DEBUG)
client = OpenAI()
openai_patcher.setup(client=client)


def chat_completion(message: str, user_id: str, raw: bool) -> str:
    kwargs = {
        "messages": [
            {
                "role": "user",
                "content": message,
            }
        ],
        "model": "gpt-3.5-turbo",
        "user": user_id,
    }

    resp = (
        client.with_raw_response.chat.completions.create(**kwargs)
        if raw
        else client.chat.completions.create(**kwargs)
    )

    return str(resp)


def stream_chat(message: str, user_id: str) -> str:
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="gpt-3.5-turbo",
        user=user_id,
        stream=True,
    )

    text = ""
    for chunk in stream:
        for choice in chunk.choices:
            print(f"{ choice = }")
            if choice.delta.content:
                text += choice.delta.content
    return text


def audio_speech(message: str, user_id: str) -> str:
    resp = client.audio.speech.create(
        input=message,
        model="tts-1",
        voice="alloy",
        response_format="mp3",
        speed=1.0,
        extra_headers={"x-user-id": user_id},
    )

    resp.stream_to_file("audio_test.mp3")

    return resp.text
