from src.document_ingestion import load_documents, splitter, load_embedding_model
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext, VectorStoreIndex

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

def initialize_storage_context(vector_store):
    """Create and return a StorageContext instance."""
    return StorageContext.from_defaults(vector_store=vector_store)

def create_vector_store_index(vector_store, documents, model, transformations):
    """Create and return a VectorStoreIndex instance from documents."""
    return VectorStoreIndex.from_documents(
        documents,
        embed_model=model,
        vector_store=vector_store,
        storage_context=initialize_storage_context(vector_store),
        transformations=transformations,
        show_progress=True
    )

def load_index():
    """Load or create a vector store index."""
    qdrant_client = create_qdrant_client()
    model = load_embedding_model()
    collection_name = "vectors_of_document"
    vector_store = create_vector_store(qdrant_client, collection_name)
    
    if vector_store._collection_exists(collection_name):
        print(f"Loading existing vector store for collection: {collection_name}")
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    else:
        documents = load_documents("Data/")
        print("Creating the GPT Index...")
        splits = splitter()
        index = create_vector_store_index(
            vector_store,
            documents,
            model,
            transformations=[splits],
        )

    return index
