import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_text(prompt):
    """Generates text using the Gemini API."""
    response = model.generate_content(prompt)
    return response.text
