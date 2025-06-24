from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
import os

def create_vector_store(data_path: str = "hotel_data.txt", vector_store_path: str = "faiss_index"):
    loader = TextLoader(data_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    db = FAISS.from_documents(docs, embeddings)
    db.save_local(vector_store_path)
    return db

def load_vector_store(vector_store_path: str = "faiss_index"):
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
    return db

def get_relevant_docs(query: str, db):
    docs = db.similarity_search(query)
    return docs 