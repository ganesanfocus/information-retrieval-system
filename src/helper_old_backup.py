import os
from PyPDF2 import PdfReader, PdfFileReader, PdfFileWriter

# from langchain.text_splitter import  RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter


from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI  # Correct import

from langchain_google_genai import GoogleGenerativeAIEmbeddings


import traceback

from dotenv import load_dotenv


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print(GOOGLE_API_KEY)

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# embeddings = GooglePalmEmbeddings()



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store

# def get_vector_store(text_chunks):
#     try:
#         print("Inside vector store function ", GOOGLE_API_KEY)
#         embeddings = GooglePalmEmbeddings()
#         vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
#         return vector_store
#     except Exception as e:
#         print("Error in get_vector_store: ", e)
#         print(traceback.format_exc())
#         return None
    
    
# def get_conversational_chain(vector_store):
#     llm = GooglePalm()
#     memory = ConversationBufferMemory(memory_key = "chat_history", return_messages=True)
#     conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)
#     return conversation_chain

def get_conversational_chain(vector_store):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")  # Corrected model usage
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vector_store.as_retriever(), memory=memory
    )
    
    return conversation_chain
    
