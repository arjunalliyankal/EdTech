from typing import List, Dict
from app.services.llm_provider import llm

class QstairLLM:
    """
    Service responsible for processing user topics and generating
    diagnostic questions (QS-Staircase logic) using Gemini LLM.
    """
    @staticmethod
    async def generate_questions(topic: str) -> List[Dict]:
        """
        Generates diagnostic questions based on the provided topic.
        """
        prompt = f"""
        Act as a strict Assessment AI.
        Generate 3 diagnostic questions for the topic: '{topic}'.
        
        Requirements:
        1. All 3 questions must be DESCRIPTIVE (open-ended).
        2. NO Multiple Choice Questions (MCQs).
        3. Questions should assess fundamental understanding and practical application of {topic}.
        """
        
        schema = """
        [
          {"id": "q1", "text": "Question 1 text...", "type": "text"},
          {"id": "q2", "text": "Question 2 text...", "type": "text"},
          {"id": "q3", "text": "Question 3 text...", "type": "text"}
        ]
        """
        
        result = await llm.generate_structured(prompt, schema)
        
        # Validation/Fallback if LLM fails or returns error
        if isinstance(result, list):
            return result
        
        print(f"QstairLLM Fallback triggered. Reason: Result is not a list. Result: {result}")
            
        # Basic Fallback if LLM fails
        return [
            {"id": "q1", "text": f"Explain the core concept of {topic} in your own words.", "type": "text"},
            {"id": "q2", "text": f"Describe a real-world use case where you would apply {topic}.", "type": "text"},
            {"id": "q3", "text": f"What are the main challenges you face when learning {topic}?", "type": "text"}
        ]

qstair_llm = QstairLLM()
