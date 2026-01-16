from typing import Dict, List
from app.services.llm_provider import llm

class RoadmapLLM:
    """
    Service responsible for analyzing student answers and generating
    a detailed, personalized learning roadmap using Gemini LLM.
    """
    @staticmethod
    async def generate_roadmap(answers: Dict[str, str], profile: Dict) -> Dict:
        """
        Analyzes diagnostic answers and generates a detailed roadmap.
        """
        prompt = f"""
        Act as an expert Educational AI Mentor.
        Analyze the student's diagnostic answers and profile to create a personalized learning roadmap.
        
        Student Answers (Descriptive):
        {answers}
        
        Student Profile:
        {profile}
        
        Task:
        1. Evaluate the student's current understanding based on their detailed answers.
        2. Identify specific skill gaps or misconceptions.
        3. Create a detailed 5-step learning roadmap. 
        4. For each step, provide 2-3 specific subtopics to cover.
        
        Requirements:
        - The roadmap must be highly detailed and tailored to the specific gaps found in the answers.
        - Provide a 'gap_analysis' summary explaining what they missing.
        - Provide an 'estimated_score' (0-100) based on the depth of their descriptive answers.
        """
        
        schema = """
        {
          "identified_gaps": ["gap 1", "gap 2", "gap 3"],
          "estimated_score": 75,
          "explanation": "Detailed analysis of the student's performance...",
          "roadmap": [
            {
              "title": "Module 1: Title",
              "description": "Detailed description of what to learn...",
              "duration": "3 days",
              "resources": ["Topic A", "Topic B"],
              "subtopics": [
                  {"title": "Subtopic 1", "description": "What to cover..."},
                  {"title": "Subtopic 2", "description": "What to cover..."}
              ]
            }
          ]
        }
        """
        
        result = await llm.generate_structured(prompt, schema)
        
        # Validation/Fallback
        if isinstance(result, dict) and "roadmap" in result:
             return result
             
        # Fallback if LLM fails
        return {
            "identified_gaps": ["General Knowledge"],
            "estimated_score": 50,
            "explanation": "We couldn't generate a detailed analysis at this time. Here represents a general path.",
            "roadmap": [
                {
                    "title": "Foundations", 
                    "description": "Review core concepts.", 
                    "duration": "1 week", 
                    "resources": [],
                    "subtopics": [
                        {"title": "Basics", "description": "Core syntax and rules."},
                        {"title": "Setup", "description": "Environment configuration."}
                    ]
                },
                {
                    "title": "Practice", 
                    "description": "Build simple projects.", 
                    "duration": "2 weeks", 
                    "resources": [],
                    "subtopics": [
                        {"title": "Project 1", "description": "Small CLI tool."},
                        {"title": "Project 2", "description": "Basic script."}
                    ]
                }
            ]
        }

roadmap_llm = RoadmapLLM()
