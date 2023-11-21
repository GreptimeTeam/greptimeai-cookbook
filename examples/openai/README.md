# openai-example

## Prerequisites

- [rye][rye] or docker
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

## Visit Flask

Flask will listen on :8001, and you can use cURL to try:

- chat completion
```shell
curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:8001/openai/chat -d '{"message":"give me a baby name", "user_id": "111"}'
```

## Visit GreptimeAI Dashboard

Visit [greptimeai][greptimeai] and navigate to dashboard to explore the traces, analytics, etc.

[rye]: https://rye-up.com/guide/installation/
[greptimeai]: https://console.greptime.cloud/ai
[openai]: https://platform.openai.com/account/api-keys
