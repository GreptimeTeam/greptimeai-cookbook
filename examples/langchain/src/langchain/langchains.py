import logging

from greptimeai.langchain.callback import GreptimeCallbackHandler

from langchain.agents import AgentExecutor, OpenAIFunctionsAgent, tool
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import SystemMessage

logging.basicConfig(level=logging.DEBUG)

# setup LangChain
greptime_callback = GreptimeCallbackHandler()

llm_chain = LLMChain(
    llm=OpenAI(),
    prompt=PromptTemplate.from_template("{text}"),
    callbacks=[greptime_callback],
)

stream_llm_chain = LLMChain(
    llm=OpenAI(streaming=True),
    prompt=PromptTemplate.from_template("{text}"),
    callbacks=[greptime_callback],
)

TEMPLATE = "You are a helpful assistant"
system_message_prompt = SystemMessagePromptTemplate.from_template(TEMPLATE)
HUMAN_TEMPLATE = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE)

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

chat_chain = LLMChain(
    llm=ChatOpenAI(),
    prompt=chat_prompt,
    callbacks=[greptime_callback],
)


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


system_message = SystemMessage(
    content="You are very powerful assistant, but bad at calculating lengths of words."
)

MEMORY_KEY = "chat_history"
prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=system_message,
    extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)],
)
memory = ConversationBufferMemory(memory_key=MEMORY_KEY, return_messages=True)
agent = OpenAIFunctionsAgent(
    llm=ChatOpenAI(temperature=0), tools=[get_word_length], prompt=prompt
)
agent_executor = AgentExecutor(
    agent=agent, tools=[get_word_length], memory=memory, verbose=True
)
