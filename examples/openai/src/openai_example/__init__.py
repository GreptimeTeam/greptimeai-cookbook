import logging

from greptimeai.tracker.openai_tracker import setup

from openai import OpenAI

logging.basicConfig(level=logging.DEBUG)

client = OpenAI()
setup(client=client)


def chat_completion(message: str):
    resp = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return str(resp)
