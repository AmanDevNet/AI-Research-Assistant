from fastapi import APIRouter, HTTPException, status
from app.services.summary_service import generate_summary

router = APIRouter()

@router.get(
    "/summarize",
    summary="Summarize Document Collection",
    description="Retrieves all stored document chunks from ChromaDB, combines them, and generates a structured summary highlighting main goals and findings using Gemini 2.5 Flash."
)
def summarize_documents():
    """
    Generates and returns a concise, business-oriented summary of all uploaded documents.
    """
    try:
        summary_text = generate_summary()
        return {
            "status": "success",
            "summary": summary_text
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while generating the summary: {str(e)}"
        )
