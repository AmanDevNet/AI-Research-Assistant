import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.database.chroma import get_vector_store

def generate_summary() -> str:
    """
    Retrieves all stored document chunks from ChromaDB, combines them, and
    generates a concise, business-friendly summary using Gemini 2.5 Flash.

    Returns:
        str: The generated summary of the document.
    """
    try:
        # Load ChromaDB vector store and retrieve all documents
        try:
            vector_store = get_vector_store()
            db_data = vector_store.get()
            documents = db_data.get("documents", [])
        except Exception:
            documents = []

        if not documents:
            return "No document content has been uploaded to the database yet. Please upload a PDF before requesting a summary."

        # Combine all document chunks into a single context block
        full_context = "\n\n".join(documents)

        # Construct prompt for the summary task
        prompt = (
            "You are a professional research assistant. Write a concise, business-friendly, "
            "and technically accurate summary of the document content provided below.\n"
            "Ensure the summary highlights key takeaways and is organized into logical bullet points.\n\n"
            f"Document Content:\n{full_context}\n\n"
            "Summary:"
        )

        # Initialize the Gemini 2.5 Flash model
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is missing.")

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3
        )

        # Generate summary response
        response = llm.invoke(prompt)

        return response.content

    except Exception as e:
        raise RuntimeError(f"Error generating document summary: {str(e)}")
