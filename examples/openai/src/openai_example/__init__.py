from greptimeai import openai_patcher

import openai

client = openai.OpenAI()
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
