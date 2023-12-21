import logging

from greptimeai import openai_patcher

from openai import OpenAI

logging.basicConfig(level=logging.DEBUG)
client = OpenAI()
openai_patcher.setup(client=client)


def chat_completion(message: str, user_id: str, streaming: bool = False) -> str:
    resp = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="gpt-3.5-turbo",
        user=user_id,
        stream=streaming,
    )
    if streaming:
        text = ""
        for chunk in resp:
            for choice in chunk.choices:
                if choice.delta.content:
                    text += choice.delta.content
        return text
    else:
        return str(resp)


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
