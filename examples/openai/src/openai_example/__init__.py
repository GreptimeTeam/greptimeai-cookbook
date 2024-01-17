import logging

from greptimeai import openai_patcher

from openai import AsyncOpenAI, OpenAI

logging.basicConfig(level=logging.DEBUG)

client = OpenAI()
openai_patcher.setup(client=client)

async_client = AsyncOpenAI()
openai_patcher.setup(client=async_client)


def chat_completion(message: str, user_id: str, raw: bool, stream: bool) -> str:
    kwargs = {
        "messages": [
            {
                "role": "user",
                "content": message,
            }
        ],
        "model": "gpt-3.5-turbo",
        "user": user_id,
        "stream": stream,
    }
    if raw:
        raw_resp = client.with_raw_response.chat.completions.create(**kwargs)
        resp = raw_resp.parse()
    else:
        resp = client.chat.completions.create(**kwargs)

    if stream:
        text = ""
        for chunk in resp:
            for choice in chunk.choices:
                if choice.delta.content:
                    text += choice.delta.content
        return text
    else:
        return str(resp)


async def async_chat_completion(
    message: str, user_id: str, raw: bool, stream: bool
) -> str:
    kwargs = {
        "messages": [
            {
                "role": "user",
                "content": message,
            }
        ],
        "model": "gpt-3.5-turbo",
        "user": user_id,
        "stream": stream,
    }
    if raw:
        raw_resp = await async_client.with_raw_response.chat.completions.create(
            **kwargs
        )
        resp = raw_resp.parse()
    else:
        resp = await async_client.chat.completions.create(**kwargs)

    if stream:
        text = ""
        async for chunk in resp:
            for choice in chunk.choices:
                if choice.delta.content:
                    text += choice.delta.content
        return text
    else:
        return str(resp)


def audio_speech(message: str, user_id: str) -> str:
    kwargs = {
        "input": message,
        "model": "tts-1",
        "voice": "alloy",
        "response_format": "mp3",
        "speed": 1.0,
        "user_id": user_id
        # "extra_headers": {"x-user-id": user_id},
    }
    resp = client.audio.speech.create(**kwargs)

    resp.stream_to_file("audio_test.mp3")

    return resp.text


def image_create(user_id: str) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt="a white siamese cat",
        size="1024x1024",
        quality="standard",
        n=1,
        user=user_id,
    )

    return response.data[0].url or ""


def tool_call(user_id: str) -> str:
    model = "gpt-4"
    messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]
    resp = client.chat.completions.create(
        messages=messages,
        model=model,
        user=user_id,
        seed=1,
        tools=tools,
        tool_choice="auto",
    )

    choice = resp.choices[0]
    assistant_message = choice.message
    tool_call = assistant_message.tool_calls[0]
    call_id = tool_call.id
    tool_message = {
        "content": "sunny",
        "role": "tool",
        "tool_call_id": call_id,
    }

    assistant_message_dict = assistant_message.model_dump()
    assistant_message_dict.pop("function_call", None)
    messages.append(assistant_message_dict)
    messages.append(tool_message)

    resp = client.chat.completions.create(
        messages=messages,
        model=model,
        user=user_id,
        seed=1,
        tools=tools,
        tool_choice="auto",
    )
    return str(resp)
