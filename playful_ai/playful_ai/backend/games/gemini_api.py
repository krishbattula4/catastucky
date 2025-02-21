import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_poker_advice(hand):
    """Get poker advice using Gemini AI."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"My hand is {hand}. What should I do?")
        return response.text
    except Exception as e:
        return f"Error: {e}"
