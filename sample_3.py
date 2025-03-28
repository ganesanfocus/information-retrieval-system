import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyDjoGiu8hpmdFmoaR7G1qAqCC0-ofi9lO4")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction="gemini pro",
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("Hi are you to development")

print(response.text)