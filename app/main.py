from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.upload import router as upload_router
from app.routes.query import router as query_router
from app.routes.summary import router as summary_router

app = FastAPI(
    title="AI Research Assistant MVP",
    description="A lightweight, modular API for RAG-based document intelligence and research workflows."
)

# Include routes
app.include_router(health_router)
app.include_router(upload_router)
app.include_router(query_router)
app.include_router(summary_router)

@app.get("/")
def home():
    """
    Root endpoint returning API metadata and a list of available endpoints.
    """
    return {
        "project_name": app.title,
        "description": app.description,
        "available_endpoints": {
            "GET /": "API metadata and available routes description",
            "GET /health": "Verify backend API status and version",
            "POST /upload-pdf": "Accept and parse a PDF, store chunks and embeddings",
            "POST /ask": "Submit questions to retrieve grounded answers with citations",
            "GET /summarize": "Generate a concise bulleted summary of document contents"
        }
    }