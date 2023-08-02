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

load_dotenv()

tmp_dir = tempfile.gettempdir() # -> /var/folders/gw/zwbjcgkj64b1srstp08g4yqh0000gn/T
DATABASE_PATH = tmp_dir + '/db/'

################################################################################
# Generate new Chroma instance
################################################################################
def get_chroma_instance():
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
    return  Chroma(embedding_function=embeddings, persist_directory=DATABASE_PATH)

################################################################################
# Read documents from JSON file and add them to Chroma instance
################################################################################
def revalidate():
    if os.path.exists(DATABASE_PATH):
        shutil.rmtree(DATABASE_PATH)
        
    fetch_products()
  
    instance = get_chroma_instance()
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

    instance.persist()

################################################################################
# Make OpenAI query
################################################################################
def query(query):
    instance = get_chroma_instance()
    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Answer with a list of products in JSON format:"""

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
# Chat with OpenAI
################################################################################
def chat_query(question):
    memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
    )

    instance = get_chroma_instance()
    
    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}"""
    
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0,openai_api_key=os.getenv('OPENAI_API_KEY')),
        retriever=instance.as_retriever(),
        combine_docs_chain_kwargs={"prompt": PROMPT},
        memory=memory
    )

    result = qa({"question": question})
    return result