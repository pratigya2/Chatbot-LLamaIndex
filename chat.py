from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from dotenv import load_dotenv
import os
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core import Settings
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.query_engine import RetrieverQueryEngine
from src.prompt import *
from llama_index.core import get_response_synthesizer
from store_index import load_index

# Load environment variables
load_dotenv()

def create_answering_model():
    """Initialize and return the HuggingFace model."""
    HuggingFace_api_key = os.environ.get('HuggingFace_api_key')
    return HuggingFaceInferenceAPI(
        model_name="HuggingFaceH4/zephyr-7b-alpha",
        token=HuggingFace_api_key
    )

def create_retriever(index):
    """Create and return a QueryFusionRetriever instance."""
    return QueryFusionRetriever(
        [index.as_retriever()],
        llm=create_answering_model(),
        similarity_top_k=2,
        num_queries=2,  # Set to 1 to disable query generation
        use_async=True,
        verbose=True,
        query_gen_prompt=query_generation_template
    )

def create_query_engine(retriever):
    """Create and return a RetrieverQueryEngine instance."""
    prompt_tmpl = PromptTemplate(answer_query_template)
    partial_prompt_tmpl = prompt_tmpl.partial_format(tone_name="Doctor")
    synth = get_response_synthesizer(
        llm=create_answering_model(),
        text_qa_template=partial_prompt_tmpl
    )
    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=synth,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.5)]
    )

def chatbot_query_engine():
    """Initialize and return the chatbot query engine."""
    index = load_index()
    Settings.llm = create_answering_model()
    retriever = create_retriever(index)
    return create_query_engine(retriever)

def question_answer(query_engine, question, conversation_history):
    """Process a question and return the chatbot's response."""
    # Build context from conversation history
    context = "\n".join(conversation_history) + f"\nYou: {question}"
    
    # Query the engine
    response = query_engine.query(context)
    
    # Update conversation history
    conversation_history.append(f"You: {question}")
    conversation_history.append(f"Bot: {response.response}")
    
    return response.response + " Thank you!"
