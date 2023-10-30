import os

import openai

import greptimeai.openai as greptime_ai

openai.api_key = os.getenv("OPEN_API_KEY")

greptime_ai.init()


def completion():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="how are you?",
        stream=True,
        max_tokens=20,
        temperature=0,
    )
    for i in response:
        print(i)


completion()
