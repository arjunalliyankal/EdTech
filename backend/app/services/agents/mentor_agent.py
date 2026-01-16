# from app.services.llm_provider import llm
from typing import Dict

class MentorAgent:
    @staticmethod
    async def evaluate_answer(question: str, answer: str) -> Dict:
        """
        Evaluates a descriptive answer for conceptual correctness.
        RETURNING MOCK DATA.
        """
        return {
          "correctness_score": 85,
          "feedback": "Good answer! You captured the main concept well.",
          "missing_concepts": []
        }

    @staticmethod
    async def generate_mentee_summary(assessment_history: list) -> Dict:
        """
        Summarizes student progress for the mentor.
        RETURNING MOCK DATA.
        """
        return { 
            'summary': 'Student is making steady progress but struggles with advanced algorithms.', 
            'areas_to_focus': ['Dynamic Programming', 'Graph Theory'] 
        }

mentor_agent = MentorAgent()
