from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai import configure, list_models

configure(api_key="***********-ofi9lO4")

print(list_models())
for a in list_models():
    print(a)