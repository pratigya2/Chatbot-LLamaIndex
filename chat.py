from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from dotenv import load_dotenv
import os
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core import Settings
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.query_engine import RetrieverQueryEngine
from src.prompt import *
from llama_index.core import get_response_synthesizer
from store_index import *


load_dotenv()
def chatbot_query_engine():

    HuggingFace_api_key = os.environ.get('HuggingFace_api_key')
    answering_model = HuggingFaceInferenceAPI(
                    model_name="HuggingFaceH4/zephyr-7b-alpha", token = HuggingFace_api_key
                    )
    index = load_index()
    Settings.llm = answering_model

    retriever = QueryFusionRetriever(
        [index.as_retriever()],
        llm=answering_model,
        similarity_top_k=2,
        num_queries=2,  # set this to 1 to disable query generation
        use_async=True,
        verbose=True,
        query_gen_prompt=query_generation_template,  # we could override the query generation prompt here
        )
# query_engine = RetrieverQueryEngine.from_args(retriever)
    prompt_tmpl = PromptTemplate(answer_query_template)
    partial_prompt_tmpl = prompt_tmpl.partial_format(tone_name="Doctor")
    synth = get_response_synthesizer(
                llm = answering_model,
                text_qa_template=partial_prompt_tmpl,
            )
    query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=synth,
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.5)],
        )
    return query_engine

def question_answer(query_engine, question, conversation_history):
    # Context contains all previous conversations
    context = "\n".join(conversation_history) + f"\nYou: {question}"

    response = query_engine.query(context)
    
    # Storing the conversations
    conversation_history.append(f"You: {question}")
    conversation_history.append(f"Bot: {response.response} Thank you!")
    
    return response.response + " Thank you!"
