
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
]


def ask_gemini(question):
    if not client:
        return "API key not found. Please check your .env file."

    errors = []

    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=question,
            )

            if response.text:
                return response.text

            errors.append(f"{model}: Empty response")

        except Exception as error:
            errors.append(f"{model}: {error}")

    return (
        "Gemini is temporarily unavailable. "
        "Please try again in a little while.\n\n"
        + "\n".join(errors)
    )
