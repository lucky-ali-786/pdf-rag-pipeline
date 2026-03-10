import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

def ingest_document():
    print("Starting data ingestion...")
    
    file_path = Path(__file__).parent / "Interupts-1.pdf"
    loader = PyPDFLoader(file_path=file_path)
    docs = loader.load()
    print(f"Loaded {len(docs)} pages from {file_path.name}")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(documents=docs)
    print(f"Split document into {len(split_docs)} chunks.")
    
    api_key = os.getenv("GEMINI_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )
    
    print("Uploading vector embeddings to Qdrant...")
    vector_store = QdrantVectorStore.from_documents(
        documents=split_docs,
        url="http://localhost:6333",
        collection_name="my_first_vector_db",
        embedding=embeddings
    )
    
    print("Ingestion complete! Vector database is populated and ready for queries.")

if __name__ == "__main__":
    ingest_document()
