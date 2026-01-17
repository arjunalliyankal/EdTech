
import logging
from typing import Dict, List, Optional
from pypdf import PdfReader
from io import BytesIO
from app.services.llm_provider import llm

logger = logging.getLogger(__name__)

class PDFService:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """
        Extracts text from a PDF file content.
        """
        try:
            reader = PdfReader(BytesIO(file_content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise ValueError("Failed to process PDF file")

    @staticmethod
    async def generate_course_from_content(content: str, filename: str) -> Dict:
        """
        Generates a structured course from raw text content using LLM.
        """
        # Truncate content if too long (LLM context limits) - rudimentary check
        max_chars = 100000 
        if len(content) > max_chars:
            content = content[:max_chars] + "...[truncated]"

        prompt = f"""
        Act as an expert Educational Content Designer.
        Create a detailed, structured learning course based on the provided document content.
        
        Document Content (extracted from {filename}):
        {content}
        
        Task:
        1. Analyze the content to understand the main topic and key concepts.
        2. Structure this into a comprehensive course module.
        3. Create a title, description, and a list of modules/chapters.
        4. For each module, provide a list of subtopics and a brief summary of what should be covered (based on the content).
        
        Output Schema:
        {{
            "title": "Course Title",
            "description": "Course Description",
            "modules": [
                {{
                    "title": "Module 1",
                    "description": "Description...",
                    "subtopics": [
                        {{"title": "Subtopic 1", "description": "..."}}
                    ]
                }}
            ]
        }}
        """
        
        schema = """
        {
          "title": "Course Title",
          "description": "Course Description",
          "modules": [
            {
              "title": "Module Title",
              "description": "Module Description",
              "subtopics": [
                {"title": "Subtopic Title", "description": "Subtopic Description"}
              ]
            }
          ]
        }
        """
        
        try:
            result = await llm.generate_structured(prompt, schema)
            return result
        except Exception as e:
            logger.error(f"LLM Course Generation failed: {e}")
            # Fallback
            return {
                "title": f"Course from {filename}",
                "description": "Automated extraction failed. Raw content preserved.",
                "modules": []
            }

pdf_service = PDFService()
