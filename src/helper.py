import os
import traceback
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = "AIzaSyDjoGiu8hpmdFmoaR7G1qAqCC0-ofi9lO4"

# Extract text from PDF
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""  # Ensure it doesn't break on NoneType
    return text

# Split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    return text_splitter.split_text(text)

# Create FAISS vector store
def get_vector_store(text_chunks):
    try:
        print("Inside vector store function ", os.getenv("GOOGLE_API_KEY"))
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Correct model
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        return vector_store
    except Exception as e:
        print("Error in get_vector_store: ", e)
        print(traceback.format_exc())
        return None

# Setup conversational chain
def get_conversational_chain(vector_store):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")  # Use the correct LLM
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vector_store.as_retriever(), memory=memory
    )
