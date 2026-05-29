import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

def predict_health(glucose, haemoglobin, cholesterol):

    prompt = f"""
You are a healthcare assistant.

Patient Blood Test Results:

Glucose: {glucose}
Haemoglobin: {haemoglobin}
Cholesterol: {cholesterol}

Analyze these values and provide:

1. Possible health risks
2. Risk Level (Low / Moderate / High)
3. Recommendation

Keep the response under 80 words.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"AI Prediction Error: {str(e)}"