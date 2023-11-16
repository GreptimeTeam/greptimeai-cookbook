import logging

from greptimeai import setup_openai

from openai import OpenAI

logging.basicConfig(level=logging.DEBUG)

client = OpenAI()
setup_openai(client=client)


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
    return resp
