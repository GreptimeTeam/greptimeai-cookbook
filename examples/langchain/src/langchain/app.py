from flask import Flask, request
from langchains import (
    agent_executor,
    chat_chain,
    greptime_callback,
    llm_chain,
    stream_llm_chain,
)

app = Flask(__name__)


@app.route("/langchain/<scenario>", methods=["POST"])
def langchain(scenario: str):
    json = request.json
    message = json.get("message", "")
    metadata = {"user_id": json.get("user_id", "")}
    if scenario == "streaming":
        return stream_llm_chain.run(
            message, callbacks=[greptime_callback], metadata=metadata
        )
    elif scenario == "llm":
        return llm_chain.run(message, callbacks=[greptime_callback], metadata=metadata)
    elif scenario == "agent":
        return agent_executor.run(
            message, callbacks=[greptime_callback], metadata=metadata
        )
    else:
        return chat_chain.run(message, callbacks=[greptime_callback], metadata=metadata)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
