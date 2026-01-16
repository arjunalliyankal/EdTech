from google import genai
import json
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class GeminiProvider:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in settings")
            return
            
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = 'gemini-1.5-flash' # Switching to stable flash model to avoid 429s
        
    async def generate_structured(self, prompt: str, schema: str) -> dict:
        if not self.api_key:
            return {"error": "LLM API Key missing"}
            
        full_prompt = f"{prompt}\n\nOutput must strictly follow this JSON schema:\n{schema}\n\nReturn only valid JSON, no markdown formatting."
        
        try:
            # Using sync call for simplicity in this hackathon, usually would use a wrapper for async
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt
            )
            text = response.text.strip()
            
            # Clean up potential markdown code blocks
            if text.startswith("```json"):
                text = text.replace("```json", "", 1).replace("```", "", 1).strip()
            elif text.startswith("```"):
                text = text.replace("```", "", 1).replace("```", "", 1).strip()
                
            return json.loads(text)
        except Exception as e:
            logger.error(f"Gemini Error: {e}")
            return {"error": str(e)}

llm = GeminiProvider()
#print(llm.generate_structured("hello", "hello"))
