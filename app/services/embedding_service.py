from typing import List
from langchain_core.documents import Document
from app.database.chroma import get_vector_store

def store_document_chunks(chunks: List[Document]) -> int:
    """
    Embeds and stores document chunks in the persistent ChromaDB vector store
    configured via langchain_chroma.

    Args:
        chunks (List[Document]): List of LangChain Document chunks.

    Returns:
        int: The total number of chunks stored.
    """
    if not chunks:
        return 0

    try:
        # Load the persistent Chroma vector store
        vector_store = get_vector_store()
        
        # Add the documents to the vector store (which triggers embedding and persistent saving)
        vector_store.add_documents(chunks)
        
        return len(chunks)
        
    except Exception as e:
        raise RuntimeError(f"Error storing document chunks in ChromaDB: {str(e)}")
