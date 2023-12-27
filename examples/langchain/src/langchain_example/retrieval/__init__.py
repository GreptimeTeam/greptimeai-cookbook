import os
import random
from typing import Dict

from greptimeai.langchain.callback import GreptimeCallbackHandler

from langchain.agents.agent_toolkits import (
    create_conversational_retrieval_agent,
    create_retriever_tool,
)
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

# setup LangChain
callbacks = [GreptimeCallbackHandler()]

address_dir = os.getenv("ADDRESS_DIR") or os.path.dirname(__file__)
address_path = os.path.join(address_dir, "state_of_the_union.txt")
loader = TextLoader(address_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)
retriever = db.as_retriever()

tool = create_retriever_tool(
    retriever,
    "search_state_of_union",
    "Searches and returns documents regarding the state-of-the-union.",
)
tools = [tool]


llm = ChatOpenAI(temperature=0)
agent_executor = create_conversational_retrieval_agent(llm, tools, verbose=True)


questions = [
    "what did the president say about kentaji brown jackson in the most recent state of the union?",
    "what did the president say about ukraine and russia?",
    "what dit the president say about the inflation?",
    "what dit the president say about the economy?",
    "what did the president say about the life after COVID?",
]


def retrieve(metadata: Dict[str, str]) -> str:
    question = random.choice(questions)
    result = agent_executor.invoke(
        input={"input": question},
        config={"metadata": metadata, "callbacks": callbacks},
    )
    return str(result.get("output") or result)
