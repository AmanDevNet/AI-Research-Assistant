import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from app.database.chroma import get_vector_store

def ask_question(question: str) -> Dict[str, Any]:
    """
    Performs similarity search to find relevant PDF chunks and uses Gemini 2.5 Flash
    to generate a response grounded in the retrieved context.

    Args:
        question (str): User's query.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - "answer": The grounded response.
            - "source_chunks": Chunks used to answer the question, including text and metadata.
    """
    try:
        # Load ChromaDB vector store
        try:
            vector_store = get_vector_store()
            db_data = vector_store.get(limit=1)
            has_docs = bool(db_data.get("ids"))
        except Exception:
            has_docs = False

        if not has_docs:
            return {
                "answer": "No documents have been uploaded to the knowledge base yet. Please upload a PDF before asking questions.",
                "citations": []
            }

        # Retrieve top 4 relevant chunks using similarity search
        relevant_docs = vector_store.similarity_search(question, k=4)

        # If similarity search yields no results
        if not relevant_docs:
            return {
                "answer": "I could not find any relevant information in the uploaded documents to answer your question.",
                "citations": []
            }

        # Build context from chunks and prepare source citations
        context_list = []
        citations = []
        
        for idx, doc in enumerate(relevant_docs):
            context_list.append(f"[Document Chunk {idx + 1}]\n{doc.page_content}")
            
            # Extract page number (typically 0-indexed in PyPDFLoader, so convert to 1-indexed)
            page_num = doc.metadata.get("page")
            if isinstance(page_num, int):
                page_num = page_num + 1
            else:
                page_num = 1
                
            # Create a concise excerpt
            clean_content = " ".join(doc.page_content.split())
            excerpt = clean_content[:150] + "..." if len(clean_content) > 150 else clean_content

            citations.append({
                "page": page_num,
                "excerpt": excerpt
            })

        context = "\n\n".join(context_list)

        # Construct system instructions and query prompt
        prompt = (
            "You are a helpful research assistant. Answer the user's question using only the provided context.\n"
            "If the context does not contain enough information to answer the question, say you cannot answer.\n"
            "Provide clean, concise answers and cite key facts from the context. Do not make up facts.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )

        # Initialize the Gemini 2.5 Flash model
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is missing.")

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.0
        )

        # Generate response
        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "citations": citations
        }

    except Exception as e:
        raise RuntimeError(f"Failed to retrieve context or generate response: {str(e)}")
