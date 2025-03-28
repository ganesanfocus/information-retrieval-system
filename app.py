import streamlit as st
import time
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

def main():
    st.set_page_config(page_title="Information Retrieval")
    st.header("Information Retrieval System")

    user_question = st.text_input("Ask a Question from the PDF Files")

    # Initialize session state variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None

    # Check if user_question is not empty and conversation exists
    if user_question.strip():
        if st.session_state.conversation:
            user_input(user_question)
        else:
            st.warning("Please upload and process a PDF first!")

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button", 
            accept_multiple_files=True
        )

        if st.button("Submit & Process"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF file.")
            else:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vector_store = get_vector_store(text_chunks)
                    
                    # Store conversation chain in session state
                    st.session_state.conversation = get_conversational_chain(vector_store)
                    
                    st.success("Processing Complete! You can now ask questions.")

# def user_input(user_question):
#     response = st.session_state.conversation.run(user_question)
#     print("================================")
#     print(response)
#     st.session_state.chatHistory = response["chat_history"]

#     for i, message in enumerate(st.session_state.chatHistory):
#         if i % 2 == 0:
#             st.write("User: ", message.content)
#         else:
#             st.write("Reply: ", message.content)

def user_input(user_question):
    response = st.session_state.conversation.run(user_question)  # Returns a string
    
    st.session_state.chatHistory = st.session_state.chatHistory or []  # Initialize if None
    st.session_state.chatHistory.append({"role": "user", "content": user_question})
    st.session_state.chatHistory.append({"role": "assistant", "content": response})
    
    for message in st.session_state.chatHistory:
        if message["role"] == "user":
            st.write("User:", message["content"])
        else:
            st.write("Reply:", message["content"])


if __name__ == "__main__":
    main()
