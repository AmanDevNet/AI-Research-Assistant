# AI Research Assistant MVP

A lightweight, production-aware Retrieval-Augmented Generation (RAG) backend built for document intelligence and AI-powered research workflow automation. 

This repository implements a modular, service-oriented architecture designed to extract document contents, chunk texts semantically, index them using Google Vector Embeddings, persist them locally via ChromaDB, and generate grounded answers or summaries using Gemini 2.5 Flash.

---

## Architecture Workflow

![Architecture Diagram](../screenshots/architecture_diagram.png)

```
User Uploads PDF
       ↓
[FastAPI Backend]
       ↓
[PDF Service] (via PyPDFLoader)
       ↓
[Recursive Text Splitter] (chunk_size=1000, overlap=200)
       ↓
[Embedding Service] (via Google gemini-embedding-001)
       ↓
[ChromaDB Store] (local persist_directory)
       ↓
Similarity Retrieval (k=4) → Context Construction
       ↓
[Gemini 2.5 Flash] → Grounded Answer & Citations (Page + Excerpt)
```

---

## Screenshots

### Swagger API Overview

![Swagger Overview](../screenshots/swagger_home.png)

### PDF Upload & Processing

![Upload Endpoint](../screenshots/upload_endpoint.png)

### Question Answering with Citations

![Question Answering](../screenshots/question_answering.png)

### Document Summarization

![Summarization](../screenshots/summary_endpoint.png)

---

## Core Features

- **Document Ingestion & Parsing**: Uploads PDF files, validates extensions, and extracts page-wise text and metadata using LangChain's `PyPDFLoader`.
- **Semantic Chunking**: Splits extracted documents into configurable text chunks using `RecursiveCharacterTextSplitter`.
- **Vector Search & Persistence**: Generates text embeddings using `GoogleGenerativeAIEmbeddings` (`models/gemini-embedding-001`) and indexes them in a persistent local ChromaDB instance.
- **Grounded Q&A with Citations**: Performs similarity search to retrieve the top 4 matching contexts, feeds them to Gemini 2.5 Flash, and returns answers along with concise page-level excerpts and citations.
- **Document Summarization**: Aggregates all document chunks stored in ChromaDB and constructs a comprehensive, structured summary highlighting key takeaways.
- **Error Handling**: Gracefully handles uninitialized collections or empty database queries by returning clear, user-friendly fallback messages.
- **Interactive Documentation**: Auto-generates fully documented Swagger / OpenAPI schemas with endpoint-specific metadata.

---

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Orchestration**: [LangChain](https://www.langchain.com/) (langchain-core, langchain-chroma, langchain-google-genai)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/) (Local persistent storage)
- **LLM & Embeddings**: [Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) / Google Embeddings API
- **PDF Extraction**: [PyPDF](https://pypdf.readthedocs.io/)
- **Environment**: Python 3.10+ & dotenv

---

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # Application initialization & router inclusions
│   ├── database/
│   │   └── chroma.py           # ChromaDB client & embedding model config
│   ├── routes/
│   │   ├── health.py           # Health check endpoint
│   │   ├── upload.py           # PDF upload and vector storage route
│   │   ├── query.py            # Question answering endpoint
│   │   └── summary.py          # Document summarization endpoint
│   ├── services/
│   │   ├── pdf_service.py      # PDF parsing and character chunking
│   │   ├── embedding_service.py # Vector embedding storage wrapper
│   │   ├── retrieval_service.py # Similarity search and Gemini generation
│   │   └── summary_service.py  # Map-reduce context summarization
│   └── models/                 # Request/Response schemas (Pydantic)
├── data/
│   ├── uploads/                # Local cache of uploaded PDF documents
│   └── chroma_db/              # Persistent SQLite ChromaDB database
├── .env                        # Local credentials & environment variables
└── requirements.txt            # Project dependencies
```

---

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/upload-pdf` | POST | Upload and process PDF |
| `/ask` | POST | Ask questions from uploaded documents |
| `/summarize` | GET | Generate document summary |
| `/health` | GET | API health check |

---

## Environment Variables

Create a `.env` file inside `backend/`

```env
GOOGLE_API_KEY=your_api_key_here
```

---

## Setup & Installation

> [!NOTE]
> Python 3.11 is recommended for running this project.

### 1. Clone & Navigate to Backend
```bash
cd backend
```

### 2. Install Dependencies
It is recommended to run this in a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Dev Server
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`. You can access the interactive Swagger UI at `http://127.0.0.1:8000/docs`.

---

## API Payload Reference

### 1. Health Check
* **Endpoint**: `GET /health`
* **Description**: Verifies backend service status.
* **Response**:
```json
{
  "status": "success",
  "message": "AI Research Assistant API is running",
  "version": "1.0.0"
}
```

### 2. Upload and Index PDF
* **Endpoint**: `POST /upload-pdf`
* **Description**: Uploads a PDF file, parses its text, chunks the pages, and indexes them in ChromaDB.
* **Payload**: Form-data with key `file` containing a `.pdf` file.
* **Response**:
```json
{
  "status": "success",
  "filename": "transformer_paper.pdf",
  "total_chunks": 42,
  "message": "File successfully uploaded, chunked, and stored in the vector database."
}
```

### 3. Query Knowledge Base
* **Endpoint**: `POST /ask`
* **Description**: Submits a natural language query, performs vector similarity search, and outputs a grounded response with citations.
* **Payload**:
```json
{
  "question": "What is the core mechanism of the Transformer architecture?"
}
```
* **Response**:
```json
{
  "status": "success",
  "question": "What is the core mechanism of the Transformer architecture?",
  "answer": "The core mechanism of the Transformer architecture is self-attention, specifically Multi-Head Attention...",
  "citations": [
    {
      "page": 3,
      "excerpt": "Multi-head attention allows the model to jointly attend to information from different representation subspaces..."
    }
  ]
}
```

### 4. Summarize Document
* **Endpoint**: `GET /summarize`
* **Description**: Aggregates all uploaded document text and uses Gemini to generate a high-level summary.
* **Response**:
```json
{
  "status": "success",
  "summary": "- **Main Goal**: Introduces the Transformer model...\n- **Key Takeaway**: Relies entirely on attention mechanisms to enable full parallelization..."
}
```

---

## Future Scope

- **Document Metadata Filtering**: Allow querying based on specific uploaded files or tags.
- **Hybrid Search**: Combine keyword-based BM25 searching with dense vector retrieval.
- **History & Sessions**: Introduce thread context or memory for continuous conversational querying.
- **Asynchronous Task Workers**: Integrate background ingestion queues for processing exceptionally large documents.
