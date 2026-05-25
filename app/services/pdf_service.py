import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def process_pdf(file_path: str) -> List[Document]:
    """
    Loads a PDF file, extracts its text, and splits it into chunked documents.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        List[Document]: List of split LangChain Document chunks.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at path: {file_path}")

    try:
        # Load PDF and extract pages
        loader = PyPDFLoader(file_path)
        pages = loader.load()

        # Define text splitter settings
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        # Chunk the loaded pages
        chunked_docs = text_splitter.split_documents(pages)
        return chunked_docs

    except Exception as e:
        raise RuntimeError(f"Error processing PDF '{file_path}': {str(e)}")
