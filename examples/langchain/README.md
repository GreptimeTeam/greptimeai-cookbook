# langchain-example

TODO(yuanbohan): update greptimeai link when it is ready

## Prerequisites

- [rye][rye]
- [OpenAI API KEY][openai]
- [GreptimeAI Service][greptimeai]

## Quick Start

- Export OpenAI environment

```shell
export OPENAI_API_KEY='sk-xxx'
```

- Export GreptimeAI environment

```shell
export GREPTIMEAI_HOST='xxx'
export GREPTIMEAI_DATABASE='xxx'
export GREPTIMEAI_TOKEN='xxx'
```

- Running Flask

running by rye
```shell
rye sync
rye run app
```

running by docker
```
docker build -t greptime/greptimeai-langchain:latest .

docker run -p 8000:8000 -e OPENAI_API_KEY='sk-xxx' \
-e GREPTIMEAI_HOST='xxx' \
-e GREPTIMEAI_DATABASE='xxx' \
-e GREPTIMEAI_TOKEN='xxx' \
greptime/greptimeai-langchain:latest
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
