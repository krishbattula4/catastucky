import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_chat_response(user_query):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_query)
    return response.text
