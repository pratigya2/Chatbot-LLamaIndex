from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings




def load_documents(datapath):
    documents = SimpleDirectoryReader(datapath).load_data()
    return documents

#Creating text chunks from the corpus
def splitter():
    splitter = SentenceSplitter(chunk_size=500, chunk_overlap=20) 
    return splitter

#embedding model for vector transformation
def load_embedding_model():
    embedding_model = FastEmbedEmbedding("BAAI/bge-small-en-v1.5")
    Settings.embed_model = embedding_model
    return embedding_model
