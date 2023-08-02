import os
import tempfile
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

tmp_dir = tempfile.gettempdir() # -> /var/folders/gw/zwbjcgkj64b1srstp08g4yqh0000gn/T
DATABASE_PATH = tmp_dir + '/db/'

def get_chroma_instance():
  embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
  return Chroma(embedding_function=embeddings, persist_directory=DATABASE_PATH)

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


def chat_query(question):
  result = qa({"question": question})
  return result