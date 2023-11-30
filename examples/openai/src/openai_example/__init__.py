import logging
from pathlib import Path

from greptimeai.tracker import openai as openai_tracker

import openai

logging.basicConfig(level=logging.DEBUG)

client = openai.OpenAI()
openai_tracker.setup(client=client)

_audio_filename = "audio_test.mp3"


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

    resp.stream_to_file(_audio_filename)

    return resp.text


def audio_transcription(prompt: str, user_id: str) -> str:
    resp = client.audio.transcriptions.create(
        model="whisper-1",
        file=Path(_audio_filename),
        prompt=prompt,
        language="en",
        response_format="json",
        extra_headers={"x-user-id": user_id},
    )
    return str(resp)


def audio_translation(prompt: str, user_id: str) -> str:
    resp = client.audio.translations.create(
        model="whisper-1",
        file=Path(_audio_filename),
        prompt=prompt,
        response_format="json",
        extra_headers={"x-user-id": user_id},
    )
    return str(resp)
