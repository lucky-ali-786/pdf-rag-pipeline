from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from google import genai
import json
from google.genai import types
file_path = Path(__file__).parent / "YOUR_PDF"
loader = PyPDFLoader(file_path=file_path)
docs=loader.load()
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",api_key="YOUR_API_KEY")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs=text_splitter.split_documents(documents=docs)
vector_store=QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="my_first_vector_db",
    embedding=embeddings
)
vector_store.add_documents(documents=split_docs)
# ingestion done
retreiver=QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name="my_first_vector_db",
        embedding=embeddings
)
result_query=retreiver.similarity_search(
    query="USER'S QUERY"
)
chunks = [f"Page: {i.metadata.get('page', 'Unknown')} \n{i.page_content}" for i in result_query]
result = "\n\n".join(chunks)
print(result)
SYSTEM_PROMPT=f""
"YOU ARE A AI AGENT WHICH HANDLES USER QUERY WITH THE HELP OF THE GIVEN DATA BELOW"
{result}
"-  RULE FOR FINAL OUTPUT: the Content MUST be formatted as clean, readable Markdown text (using bullet points). DO NOT output nested JSON, dictionaries, or raw arrays in the final content."
""
client = genai.Client(api_key="YOUR_API_KEY")
content=client.models.generate_content(
     model="gemini-2.5-flash-lite",
     contents="YOUR QUERY ABOUT THE PDF",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.2,
    ),
)
# WRITING IN SOME EXTERNAL FILE (OPTIONAL)!
with open(f"sample.md", "w") as file:
            file.write(f"{content.text}")
