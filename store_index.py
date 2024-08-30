from src.document_ingestion import load_documents, splitter, load_embedding_model
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex

# Load environment variables
load_dotenv()

def create_qdrant_client():
    """Initialize and return the Qdrant client."""
    Qdrant_url = os.environ.get('Qdrant_url')
    Qdrant_api_key = os.environ.get('Qdrant_api_key')
    return QdrantClient(
        url=Qdrant_url,
        api_key=Qdrant_api_key,
        prefer_grpc=True
    )

def create_vector_store(client, collection_name):
    """Create and return a QdrantVectorStore instance."""
    return QdrantVectorStore(
        client=client,
        collection_name=collection_name
    )

def load_index():
    """Load or create a vector store index."""
    qdrant_client = create_qdrant_client()
    model = load_embedding_model()
    collection_name = "vectors_of_document"
    vector_store = create_vector_store(qdrant_client, collection_name)
    documents = load_documents("Data/")
    print("Creating the GPT Index...")
    splits = splitter()
    index = VectorStoreIndex.from_documents(
          documents,
          embed_model=model,
          vector_store=vector_store,
          transformations=[splits],
          show_progress=True

            )
    index.storage_context.persist(persist_dir="index")
    storage_context = StorageContext.from_defaults(persist_dir="index")
    index = load_index_from_storage(storage_context)
    
    return index
