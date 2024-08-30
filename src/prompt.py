from llama_index.core import PromptTemplate
query_generation_template = (
    "You are a helpful assistant that generates multiple search queries based on a "
    "single input query. Generate {num_queries} search queries, one on each line, "
    "related to the following input query:\n"
    "Query: {query}\n"
    "Queries:\n"
)
answer_query_template = """\
Context information is below.
---------------------
{context_str}
---------------------
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Say Thank You at the end of answer.
Please write the answer in the style of {tone_name}
Query: {query_str}
Answer: \
"""
