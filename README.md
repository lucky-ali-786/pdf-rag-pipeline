# 📄 Document RAG Pipeline Architecture

## 🚀 Overview
This repository contains the architecture and implementation of a **Retrieval-Augmented Generation (RAG)** system. It is designed to efficiently ingest PDF documents, process the text into vector embeddings, and leverage a Large Language Model (LLM) to answer user queries based strictly on the provided document context, eliminating hallucinations.

## ⚙️ System Architecture 

The system operates in two distinct phases:

### Phase 1: Data Ingestion
1. **Document Loader:** Utilizes `PyPDF` to extract raw text from PDF files.
2. **Text Splitter (Chunking):** Breaks down large text blocks into smaller, context-rich chunks to respect the LLM's token limits.
3. **Embedding Model:** Converts the text chunks into high-dimensional vector representations.
4. **Vector Database:** Stores the embeddings and original text metadata in **Qdrant** for highly efficient similarity search.

### Phase 2: Query & Generation
1. **User Query Processing:** The user's natural language question is passed through the same embedding model.
2. **Similarity Search:** The system queries Qdrant to retrieve the top mathematically similar text chunks (Cosine Similarity).
3. **Prompt Construction:** The original query and the retrieved context chunks are merged into a unified prompt.
4. **LLM Generation:** The enriched prompt is sent to the LLM to generate an accurate, context-aware response.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Orchestration:** LangChain / LlamaIndex (Adjust based on what you used)
* **Document Processing:** PyPDF
* **Vector Database:** Qdrant
* **Embeddings & LLM:** [e.g., OpenAI API / Google Gemini / HuggingFace]

## 💻 Getting Started

### Prerequisites
- Python 3.8+
- [Docker](https://www.docker.com/) (to run Qdrant locally)
- Google Gemini API Key

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
   cd your-repo-name
   
2.**Set up a virtual environment:**
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

3.**Install dependencies:**
pip install -r requirements.txt

4.**Environment Variables:**
Create a .env file in the root directory and securely add your API key:
GEMINI_API_KEY=your_api_key_here

5.**Start Qdrant (Local Vector DB):**
Run Qdrant via Docker. This keeps your database running in the background:
docker run -p 6333:6333 -p 6334:6334 \-v $(pwd)/qdrant_storage:/qdrant/storage:z \qdrant/qdrant

6.**Run Data Ingestion:**
Process the PDF and store the vector embeddings in Qdrant:
python ingest.py
