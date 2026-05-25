from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    """
    Simple health check endpoint to verify backend status.
    """
    return {
        "status": "success",
        "message": "AI Research Assistant API is running",
        "version": "1.0.0"
    }
