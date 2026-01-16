# from app.services.llm_provider import llm
from typing import List, Dict

class StudentAgent:
    @staticmethod
    async def generate_diagnostic(profile_context: Dict, topic: str = None) -> List[Dict]:
        """
        Generates personalized MCQs and Descriptive questions based on student profile and optional topic.
        RETURNING MOCK DATA.
        """
        # Mock response based on topic
        if topic and "python" in topic.lower():
             return [
                {"id": "q1", "text": "Which method adds an element to the end of a list?", "type": "mcq", "options": ["append()", "extend()", "insert()", "add()"]},
                {"id": "q2", "text": "What is the output of print(2 ** 3)?", "type": "mcq", "options": ["6", "8", "9", "5"]},
                {"id": "q3", "text": "Explain the difference between a list and a tuple.", "type": "text"}
             ]
        
        return [
            {"id": "q1", "text": "What is the time complexity of binary search?", "type": "mcq", "options": ["O(log n)", "O(n)", "O(n^2)", "O(1)"]},
            {"id": "q2", "text": "Which approach is used in Merge Sort?", "type": "mcq", "options": ["Divide and Conquer", "Greedy", "Dynamic Programming", "Backtracking"]},
            {"id": "q3", "text": "Describe a situation where you would use a hash map.", "type": "text"}
        ]

    @staticmethod
    async def analyze_and_roadmap(answers: Dict, text_input: str, profile: Dict) -> Dict:
        """
        Performs gap analysis and generates a structured roadmap.
        RETURNING MOCK DATA.
        """
        return {
            "identified_gaps": ["Data Structures", "Algorithm Analysis", "System Design"],
            "roadmap": [
                {"title": "Module 1: Core Concepts", "description": "Master lists, dictionaries, and basic complexity analysis.", "duration": "2 days"},
                {"title": "Module 2: Advanced Algorithms", "description": "Deep dive into sorting, searching, and recursion.", "duration": "1 week"},
                {"title": "Module 3: Real-world Applications", "description": "Apply your knowledge to build simple systems.", "duration": "5 days"}
            ],
            "explanation": "Great start! You have a good grasp of the basics, but delving deeper into algorithmic efficiency will help you write better code.",
            "estimated_score": 70
        }

student_agent = StudentAgent()
