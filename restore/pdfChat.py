import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_GEMINI_API_KEY"))

def get_pdf_text(pdf_docs):
    """
    Returns the concatenated text extracted from each page of the PDF documents in pdf_docs.
    
    :param pdf_docs: A list of paths to the PDF documents.
    :return: A string containing the text extracted from the PDF documents.
    """
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text


def get_text_chunks(text):
    """
    Split the given text into chunks of 10000 characters with a 1000 character overlap.

    :param text: The input text to be split into chunks.
    :return: A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    """
    Get vector store from the given text chunks using GoogleGenerativeAIEmbeddings
    and save the vector store locally.
    
    :param text_chunks: List of text chunks for generating embeddings
    :return: None
    """
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",google_api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3,google_api_key= os.getenv("GOOGLE_GEMINI_API_KEY"))

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question):
    """
    This function takes a user question as input and uses GoogleGenerativeAIEmbeddings to 
    generate embeddings. It then loads a FAISS index and performs a similarity search 
    based on the user question. It retrieves a conversational chain and uses it to generate 
    a response based on the input documents and the user question. Finally, it prints and 
    writes the response to the streamlit interface.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",google_api_key= os.getenv("GOOGLE_GEMINI_API_KEY"))
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response)
    st.write("Reply: ", response["output_text"])


def main():
    """
    Main function to set page config, display header, get user input,
    handle user input, display sidebar menu, upload PDF files, process
    files, and display success message.
    """
    st.set_page_config("Chat PDF")
    st.header("Chat with PDF using Gemini💁")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")


if __name__ == "__main__":
    main()