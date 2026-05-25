from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline


def load_llm():

    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",
        max_new_tokens=300,
        temperature=0.5,
        repetition_penalty=1.1
    )

    llm = HuggingFacePipeline(
        pipeline=pipe
    )

    return llm