from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma

import os


def ask_question(query: str, project_id: str, base_dir="chroma_store"):
    embeddings = OpenAIEmbeddings()
    persist_dir = os.path.join(base_dir, project_id)
    vectordb = Chroma(persist_directory=persist_dir,
                      embedding_function=embeddings)
    retriever = vectordb.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    result = qa_chain.invoke(query)
    return result['result']
