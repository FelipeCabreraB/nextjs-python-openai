import os
import shutil
import tempfile
import json
from dotenv import load_dotenv

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import JSONLoader
from langchain.prompts import PromptTemplate
from api.helpers.fetch_products import fetch_products

import pinecone

from langchain.vectorstores import Pinecone

load_dotenv()

################################################################################
# Initialize Pinecone instance
################################################################################
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV"),
)

################################################################################
# CONFIG
################################################################################
INDEX_NAME = "test-vector-db"

################################################################################
# Get pinecone instance
################################################################################
def get_pinecone_instance():
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
    return Pinecone.from_existing_index(INDEX_NAME, embeddings)

################################################################################
# Get Redis url
################################################################################
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_URL = f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

################################################################################
# Read documents from JSON file and add them to Pinecone index
################################################################################
tmp_dir = tempfile.gettempdir() # -> /var/folders/gw/zwbjcgkj64b1srstp08g4yqh0000gn/T
DATABASE_PATH = "/tmp"

def revalidate():
    if os.path.exists(DATABASE_PATH):
        shutil.rmtree(DATABASE_PATH)
        
    fetch_products()
    instance = get_pinecone_instance()
    data_file_path = os.path.join(DATABASE_PATH, 'data.json')

    loader = JSONLoader(
        file_path=data_file_path,
        jq_schema='.[]',
        text_content=False
    )
    if loader:
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separators= ["\n\n", "\n", ".", ";", ",", " ", ""])
        texts = text_splitter.split_documents(documents)
        instance.add_documents(texts)

################################################################################
# Related products
################################################################################
def related(query):
  instance = get_pinecone_instance()

  prompt_template = """You will receive a product object delimited with <>. Your task is to use the following pieces of context to find a maximum of three products that are related to the product delimited with <>.
  If you can not find any related products, just return an empty array.
  Don't return duplicated products.
  Don't return the product provided in the final result.
  Return an array of ids of the products.
  Don't return an object.

  {context}

  Product: <{question}>
  Answer in JSON format:"""

  PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

  chain_type_kwargs = {"prompt": PROMPT}

  qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0,openai_api_key=os.getenv('OPENAI_API_KEY')),
    chain_type="stuff",
    retriever=instance.as_retriever(),
    chain_type_kwargs=chain_type_kwargs
  )

  res = qa.run(query)
  return json.loads(res)

################################################################################
# Search products
################################################################################
def search(search_term):
  instance = get_pinecone_instance()

  prompt_template = """You are an optimized search engine.
  You will receive a search term delimited with <>.
  Your task is to use the following pieces of context to find a maximum of three products that match with the search term provided.
  Don't return duplicated products.
  Return an array of ids of the products.
  Don't return an object.

  {context}

  Search term: <{question}>
  Return an array of products.
  Answer in JSON format:"""

  PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

  chain_type_kwargs = {"prompt": PROMPT}

  qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0,openai_api_key=os.getenv('OPENAI_API_KEY')),
    chain_type="stuff",
    retriever=instance.as_retriever(),
    chain_type_kwargs=chain_type_kwargs
  )

  res = qa.run(search_term)
  return json.loads(res)

################################################################################
# Chat with OpenAI
################################################################################
def chat_query(input, cookie_value):
    instance = get_pinecone_instance()
    
    history = RedisChatMessageHistory(url=REDIS_URL, session_id=cookie_value, key_prefix='SUMMARY_BUFFER_TEST')
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0,openai_api_key=os.getenv('OPENAI_API_KEY')), chat_memory=history)
    
    _DEFAULT_TEMPLATE = """
    Your are a store assistant called Alexa.
    Use the following pieces of context and the chat history to answer.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Chat history: {chat_history}
    Context: {context}
    Question: {question}
    
    Tip: Your answers shouldn't start with "Alexa:" or "Human:".
    """

    PROMPT = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=_DEFAULT_TEMPLATE,
    )
    
    conversation = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0,openai_api_key=os.getenv('OPENAI_API_KEY')),
        verbose=True,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": PROMPT},
        retriever=instance.as_retriever()
    )
    result = conversation({"question": input})

    return result