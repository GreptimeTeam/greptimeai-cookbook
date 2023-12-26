from flask import Flask, request

from langchain_example.langchain_ import agent_chain, chat_chain, llm_chain
from langchain_example.retrieval import retrieve

app = Flask(__name__)


@app.route("/langchain/<scenario>", methods=["POST"])
def langchain(scenario: str):
    json = request.json
    message = json.get("message", "")
    streaming = json.get("streaming", False)
    if not isinstance(streaming, bool):
        streaming = bool(streaming)
    metadata = {"user_id": json.get("user_id", "")}

    if scenario == "llm":
        return llm_chain(message, metadata=metadata, streaming=streaming)
    elif scenario == "agent":
        return agent_chain(message, metadata=metadata)
    elif scenario == "retrieval":
        return retrieve(metadata)
    else:
        return chat_chain(message, metadata=metadata, streaming=streaming)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
