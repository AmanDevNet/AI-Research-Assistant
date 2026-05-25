from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.services.retrieval_service import ask_question

router = APIRouter()

class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        description="The natural language query or question about the uploaded document content.",
        json_schema_extra={"examples": ["What is the main summary of this document?"]}
    )

@router.post(
    "/ask",
    summary="Query Document Knowledge Base",
    description="Takes a user query, retrieves relevant contexts from ChromaDB via similarity search, and answers using Gemini 2.5 Flash with page-level citations."
)
def query_documents(request: QueryRequest):
    """
    Submits a query, performs vector search, and returns a grounded AI response with citations.
    """
    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The question field cannot be empty."
        )

    try:
        # Get response and citations from retrieval service
        result = ask_question(request.question)
        
        return {
            "status": "success",
            "question": request.question,
            "answer": result["answer"],
            "citations": result["citations"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieval querying: {str(e)}"
        )
