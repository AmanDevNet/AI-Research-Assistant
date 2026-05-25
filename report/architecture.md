# System Architecture

## Overview

The AI Research Assistant is designed as a lightweight Retrieval-Augmented Generation (RAG) system for document intelligence and automated research workflows.

The architecture focuses on:

- Fast document ingestion
- Semantic retrieval
- AI-powered question answering
- Citation-grounded responses
- Low-cost local deployment

The system follows a modular architecture where document processing, embeddings generation, retrieval, and response generation are separated into independent workflow stages.

---

# Core Workflow

1. User uploads a PDF document
2. System extracts text from the document
3. Text is divided into semantic chunks
4. Embeddings are generated for each chunk
5. Chunks are stored inside ChromaDB
6. User submits a natural language query
7. Relevant chunks are retrieved using similarity search
8. Retrieved context is sent to Gemini
9. Gemini generates a grounded response
10. System returns answer with citations

---

# Architecture Components

## 1. FastAPI Backend

Handles:
- API routing
- File uploads
- Query endpoints
- Response handling

FastAPI was selected for:
- fast development speed
- async support
- automatic Swagger documentation
- clean API structure

---

## 2. PDF Processing Layer

Responsible for:
- PDF loading
- text extraction
- preprocessing

PyPDFLoader from LangChain is used for lightweight PDF ingestion.

---

## 3. Chunking Layer

Document text is split into smaller overlapping chunks.

Configuration:
- Chunk Size: 1000
- Chunk Overlap: 200

This improves:
- retrieval quality
- semantic relevance
- response grounding

---

## 4. Embedding Layer

Embeddings are generated using Google's embedding model.

Embeddings convert text chunks into vector representations for semantic similarity search.

---

## 5. ChromaDB Vector Database

Stores:
- embeddings
- metadata
- document chunks

ChromaDB enables:
- semantic retrieval
- lightweight local storage
- persistent vector indexing

---

## 6. Retrieval Layer

When a user submits a query:
- relevant chunks are retrieved using vector similarity search
- top matching chunks are selected
- retrieved context is passed to Gemini

---

## 7. Gemini Response Generation

Gemini 2.5 Flash generates:
- grounded answers
- summaries
- insights

Responses are generated only using retrieved context to reduce hallucinations.

---

# Production Scaling Considerations

For production deployment, the architecture could be extended using:

- Pinecone or Weaviate for distributed vector search
- Redis caching layer
- Background task queues
- Cloud object storage
- Authentication systems
- Containerized deployment using Docker
- GPU inference infrastructure for high throughput

The current MVP prioritizes:
- rapid experimentation
- low infrastructure complexity
- fast prototype delivery

---

# Architecture Diagram

The following diagram illustrates the complete workflow architecture of the AI Research Assistant system.

(Architecture diagram attached in submission assets)