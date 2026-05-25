from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate

from llm import load_llm


def create_qa_chain(vectorstore):

    llm = load_llm()

    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 3,
            "score_threshold": 0.5
        }
    )

    template = """
    You are a helpful AI assistant.

    Use the retrieved PDF content below to answer the user question.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain