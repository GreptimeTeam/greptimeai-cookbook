# langchain-example

TODO(yuanbohan): update when greptimeai service is ready

## Prerequisites

- [rye][rye]
- [OpenAI API KEY][openai]
- [GreptimeCloud Service][greptimeai]

## Quick Start

- Export environment

```shell
export OPENAI_API_KEY=sk-xxx
export GREPTIME_LLM_HOST=xxx
export GREPTIME_LLM_DATABASE=xxx
export GREPTIME_LLM_USERNAME=xxx
export GREPTIME_LLM_PASSWORD=xxx
```
- Running Flask

```shell
rye sync
rye run app
```

## Visit Flask

Flask will listen on :8000, and you can use cURL to try:

- chat
```shell
curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:8000/langchain/chat -d '{"message":"give me a baby name", "user_id": "111"}'
```

- llm
```shell
curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:8000/langchain/llm -d '{"message":"give me a joke", "user_id": "222"}'
```

- agent
```shell
curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:8000/langchain/agent -d '{"message":"how many letters in the word open-source", "user_id": "333"}'
```

- streaming
```shell
curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:8000/langchain/streaming -d '{"message":"give me a joke", "user_id": "444"}'
```

## Visit GreptimeAI Dashboard

TODO(yuanbohan): more information here: link, capture, etc.

[rye]: https://rye-up.com/guide/installation/
[greptimeai]: https://console.greptime.cloud/ai
[openai]: https://platform.openai.com/account/api-keys
