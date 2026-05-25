import streamlit as st
import os
from rag import load_pdf, split_documents
from embeddings import create_vectorstore
from retrieval import create_qa_chain
from storage import save_chat


st.title("GenAI Assistant with RAG")

# SESSION HISTORY
if "history" not in st.session_state:
    st.session_state.history = []

# FILE UPLOAD
uploaded_file = st.file_uploader(
    "Upload a PDF",
    type="pdf"
)

if uploaded_file:

    # SAVE PDF
    file_path = os.path.join(
        "uploaded_docs",
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF Uploaded Successfully!")

    # LOAD PDF
    documents = load_pdf(file_path)

    # SPLIT DOCUMENTS
    chunks = split_documents(documents)

    # CREATE VECTOR STORE
    vectorstore = create_vectorstore(chunks)

    # CREATE QA CHAIN
    qa_chain = create_qa_chain(vectorstore)

    st.success("RAG Pipeline Ready!")

    # USER QUESTION
    question = st.text_input(
        "Ask a question from the PDF"
    )

    # ONLY RUN IF QUESTION EXISTS
    if question:

        response = qa_chain.run(question)

        docs = vectorstore.similarity_search(
            question,
            k=2
        )

        st.write("### Retrieved Chunks")

        for doc in docs:
            st.write(doc.page_content[:1000])

        # CLEAN RESPONSE
        if "Answer:" in response:
            response = response.split("Answer:")[-1].strip()
            save_chat(question, response)

        # STORE CHAT HISTORY
        st.session_state.history.append(
            {
                "question": question,
                "answer": response
            }
        )

        # SHOW ANSWER
        st.write("### Answer:")

        if (
            len(response.strip()) < 5
            or response.lower().startswith("i could not")
        ):

            st.write("Here are the most relevant details found in the PDF:")

            for i, doc in enumerate(docs, 1):

                st.write(f"{i}. {doc.page_content[:500]}")

        else:
            st.write(response)

        