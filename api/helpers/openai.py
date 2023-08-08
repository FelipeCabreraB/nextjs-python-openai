import os
import shutil
import tempfile
import json
from dotenv import load_dotenv

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import JSONLoader
from langchain.prompts import PromptTemplate
from api.helpers.fetch_products import fetch_products

import pinecone

from langchain.vectorstores import Pinecone

load_dotenv()

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

################################################################################
# Get pinecone instance
################################################################################
def get_pinecone_instance():
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
    return Pinecone.from_existing_index(INDEX_NAME, embeddings)

tmp_dir = tempfile.gettempdir() # -> /var/folders/gw/zwbjcgkj64b1srstp08g4yqh0000gn/T
DATABASE_PATH = tmp_dir + '/db/'

################################################################################
# Read documents from JSON file and add them to Chroma instance
################################################################################
def revalidate():
    if os.path.exists(DATABASE_PATH):
        shutil.rmtree(DATABASE_PATH)
        
    fetch_products()
  
    instance = get_pinecone_instance()
    loader = JSONLoader(
        file_path='./data.json',
        jq_schema='.[]',
        text_content=False
    )

    if loader:
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separators= ["\n\n", "\n", ".", ";", ",", " ", ""]) # se puede pasar regex a los separators
        texts = text_splitter.split_documents(documents)
        instance.add_documents(texts)

    # instance.persist()

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
# we defined memory outside of function so it does not reset on every request
memory = ConversationBufferMemory(
  memory_key="chat_history",
  return_messages=True
)

def clear_memory():
  memory.clear()

def chat_query(question):
    instance = get_pinecone_instance()
    
    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    Don't mention the given context in your answer.

        {context}

        Question: {question}"""
    
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0,openai_api_key=os.getenv('OPENAI_API_KEY')),
        retriever=instance.as_retriever(),
        combine_docs_chain_kwargs={"prompt": PROMPT},
        memory=memory,
        verbose=True
    )

    result = qa({"question": question})
    return result