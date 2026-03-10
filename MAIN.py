from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from google import genai
from google.genai import types

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key="YOUR_API_KEY"
)

retriever = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="my_first_vector_db",
    embedding=embeddings
)

user_query = "YOUR QUERY ABOUT THE PDF"

result_query = retriever.similarity_search(query=user_query)

chunks = [f"Page: {i.metadata.get('page', 'Unknown')} \n{i.page_content}" for i in result_query]
result = "\n\n".join(chunks)

SYSTEM_PROMPT = f"""
YOU ARE A AI AGENT WHICH HANDLES USER QUERY WITH THE HELP OF THE GIVEN DATA BELOW:

{result}

- RULE FOR FINAL OUTPUT: the Content MUST be formatted as clean, readable Markdown text (using bullet points). DO NOT output nested JSON, dictionaries, or raw arrays in the final content.
"""

client = genai.Client(api_key="YOUR_API_KEY")

content = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=user_query,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.2,
    ),
)

with open("sample.md", "w") as file:
    file.write(content.text)

print("Response generated and saved to sample.md")

