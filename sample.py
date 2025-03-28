import os

from dotenv import load_dotenv


load_dotenv()
print(os.getenv("GOOGLE_API_KEY"))


from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyDj*****************9lO4")
response = llm.invoke("Hello, how are you?")
print(response)
