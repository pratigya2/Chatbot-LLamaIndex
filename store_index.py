from src.document_ingestion import load_documents, splitter, load_embedding_model
import os
import time
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext, VectorStoreIndex



load_dotenv()
def load_index():
    Qdrant_url = os.environ.get('Qdrant_url')
    Qdrant_api_key = os.environ.get('Qdrant_api_key')
    qdrant_client = QdrantClient(
    url=Qdrant_url,
    api_key=Qdrant_api_key,
    )
    collection = "vectors_of_document"
    vector_store = QdrantVectorStore(client=qdrant_client, collection_name="vectors_of_document")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    splits = splitter()
    model = load_embedding_model()
    if vector_store._collection_exists('vectors_of_document'):
        print(f"Loading existing vector store for collection: {collection}")
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    else:
        documents = load_documents("Data/")
        print("Creating the GPT Index...")
        # Replace with your document source, e.g., directory path
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
                documents,
                embed_model=model,
                vector_store=vector_store,
                storage_context=storage_context,
                transformations=[splits],
                show_progress=True )

    return index







