import os
from dotenv import load_dotenv

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from langchain.memory import RedisChatMessageHistory
import logging
import os
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from fastapi import FastAPI, HTTPException, Cookie

import pinecone

from langchain.vectorstores import Pinecone

load_dotenv()

REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_URL = f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

history = RedisChatMessageHistory(url=REDIS_URL, session_id="2", key_prefix='SUMMARY_BUFFER_TEST')
memory = ConversationSummaryBufferMemory(memory_key="chat_history_lines", llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0,openai_api_key=os.getenv('OPENAI_API_KEY')), max_token_limit=10, chat_memory=history)

################################################################################
# CONFIG
################################################################################
INDEX_NAME = "test-vector-db"

################################################################################
# Initialize Pinecone instance
################################################################################
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV"),
)

def get_pinecone_instance():
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
    return Pinecone.from_existing_index(INDEX_NAME, embeddings)

def chat_test(input, cookie_value):
    instance = get_pinecone_instance()
    
    print(cookie_value)
    
    history = RedisChatMessageHistory(url=REDIS_URL, session_id=cookie_value, key_prefix='SUMMARY_BUFFER_TEST')
    memory = ConversationSummaryBufferMemory(memory_key="chat_history_lines", llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0,openai_api_key=os.getenv('OPENAI_API_KEY')), max_token_limit=10, chat_memory=history)
    
    _DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

    Current conversation:
    {chat_history_lines}
    Human: {input}
    AI:"""
    PROMPT = PromptTemplate(
        input_variables=["input", "chat_history_lines"],
        template=_DEFAULT_TEMPLATE,
    )
    
    conversation = ConversationChain(llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0,openai_api_key=os.getenv('OPENAI_API_KEY')), verbose=True, memory=memory, prompt=PROMPT)
    result = conversation.run(input)

    return result

def read_cookie(my_cookie: str = Cookie(None)):
    return {"message": f"Cookie value: {my_cookie}"}
    