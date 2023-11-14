from flask import Flask, request

from langchain_example.langchains import agent_chain, callbacks, chat_chain, llm_chain

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
        chain = llm_chain(streaming=streaming)
        return chain.run(message, callbacks=callbacks, metadata=metadata)
    elif scenario == "agent":
        return agent_chain().run(message, callbacks=callbacks, metadata=metadata)
    else:
        chain = chat_chain(streaming=streaming)
        return chain.run(message, callbacks=callbacks, metadata=metadata)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
