import os
import shutil
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from app.services.pdf_service import process_pdf
from app.services.embedding_service import store_document_chunks

router = APIRouter()

# Get the path to the backend directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")

@router.post(
    "/upload-pdf",
    summary="Upload and Index PDF",
    description="Uploads a PDF document, extracts its text, splits it into semantic chunks, generates vector embeddings using Google Generative AI, and saves the vectors in ChromaDB."
)
def upload_pdf(
    file: UploadFile = File(
        ..., 
        description="The PDF file to upload and index (must have a .pdf file extension)."
    )
):
    """
    Saves the PDF to local storage, processes text into chunks, and stores embeddings.
    """
    # Validate file extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed."
        )

    # Ensure the upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Save the uploaded file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process PDF to get chunked document objects
        chunks = process_pdf(file_path)
        
        # Store chunks and their embeddings in ChromaDB
        stored_count = store_document_chunks(chunks)
        
        return {
            "status": "success",
            "filename": file.filename,
            "total_chunks": stored_count,
            "message": "File successfully uploaded, chunked, and stored in the vector database."
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the file: {str(e)}"
        )
