import json
import logging
from typing import Dict

from greptimeai.langchain.callback import GreptimeCallbackHandler

from langchain.agents import AgentExecutor, tool
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.tools.render import format_tool_to_openai_function

logging.basicConfig(level=logging.DEBUG)

# setup LangChain
callbacks = [GreptimeCallbackHandler()]


def llm_chain(message: str, metadata: Dict[str, str], stream: bool = False) -> str:
    llm = OpenAI(streaming=stream)
    prompt = PromptTemplate.from_template("{text}")
    runnable = prompt | llm
    return runnable.invoke(
        input={"text": message},
        config={"metadata": metadata, "callbacks": callbacks},
    )


def chat_chain(message: str, metadata: Dict[str, str], stream: bool = False) -> str:
    TEMPLATE = "You are a helpful assistant"
    system_message_prompt = SystemMessagePromptTemplate.from_template(TEMPLATE)
    HUMAN_TEMPLATE = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(
        llm=ChatOpenAI(streaming=stream),
        prompt=chat_prompt,
        callbacks=callbacks,
    )
    return chain.run(message, metadata=metadata, callbacks=callbacks)


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


tools = [get_word_length]


def agent_chain(message: str, metadata: Dict[str, str]) -> str:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    llm_with_tools = llm.bind(
        functions=[format_tool_to_openai_function(t) for t in tools]
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are very powerful assistant, but bad at calculating lengths of words.",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    executor = AgentExecutor(
        agent=agent,
        tools=[get_word_length],
        metadata=metadata,
        callbacks=callbacks,
        verbose=True,
    )
    return json.dumps(executor.invoke({"input": message}))
