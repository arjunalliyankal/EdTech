import google.generativeai as genai
import os
from app.core.config import settings

def main():
    if not settings.GEMINI_API_KEY:
        print("No API Key found.")
        return

    print(f"GenAI Version: {genai.__version__}")
    print("Listing available models...")
    try:
        for m in genai.list_models():
            print(f"Found model: {m.name}")
            if 'generateContent' in m.supported_generation_methods:
                print(f" -> SUPPORTED: {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    main()
