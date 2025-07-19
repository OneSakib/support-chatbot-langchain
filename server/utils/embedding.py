from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
from dotenv import load_dotenv
load_dotenv()


def store_embeddings(texts, project_id: str, base_dir="chroma_store"):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    docs = []
    for item in texts:
        chunks = splitter.create_documents([item['content']], metadatas=[{
            'source': item['url']
        }])
        docs.extend(chunks)
    embeddings = OpenAIEmbeddings()
    persist_dir = os.path.join(base_dir, project_id)
    if not os.path.exists(persist_dir):
        vectorstore = Chroma.from_documents(
            docs, embedding=embeddings, persist_directory=persist_dir)
        vectorstore.persist()
