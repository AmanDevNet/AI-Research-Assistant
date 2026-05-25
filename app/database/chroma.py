import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables from .env
load_dotenv()

# Define the persistence directory relative to this project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "data", "chroma_db")

# Ensure the database directory exists
os.makedirs(PERSIST_DIRECTORY, exist_ok=True)

# Retrieve Google API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")

# Initialize the Google embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)

def get_vector_store(collection_name: str = "research_assistant") -> Chroma:
    """
    Initializes and returns the persistent Chroma vector store instance.

    Args:
        collection_name (str): The name of the collection in ChromaDB.

    Returns:
        Chroma: An instance of the LangChain Chroma vector store.
    """
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
