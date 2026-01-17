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
        - For each module, provide 2-3 specific learning resources (articles, documentation, or tutorials) with valid URLs.
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
              "resources": [
                  {"title": "MDN Web Docs - Topic", "url": "https://developer.mozilla.org"},
                  {"title": "W3Schools - Topic", "url": "https://www.w3schools.com"}
              ],
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
                    "resources": [
                        {"title": "Official Documentation", "url": "https://docs.python.org/3/"}
                    ],
                    "subtopics": [
                        {"title": "Basics", "description": "Core syntax and rules."},
                        {"title": "Setup", "description": "Environment configuration."}
                    ]
                },
                {
                    "title": "Practice", 
                    "description": "Build simple projects.", 
                    "duration": "2 weeks", 
                    "resources": [
                        {"title": "Github Learning Lab", "url": "https://lab.github.com/"}
                    ],
                    "subtopics": [
                        {"title": "Project 1", "description": "Small CLI tool."},
                        {"title": "Project 2", "description": "Basic script."}
                    ]
                }
            ]
        }

    @staticmethod
    async def generate_roadmap_from_topic(topic: str, profile: Dict) -> Dict:
        """
        Generates a detailed, step-by-step descriptive course roadmap directly from a topic.
        """
        prompt = f"""
        Act as an expert Educational AI Mentor.
        The student wants to learn about: "{topic}"
        
        Student Profile:
        {profile}
        
        Task:
        1. Design a comprehensive, step-by-step descriptive course for this topic.
        2. Create a detailed 5-step learning roadmap that covers everything from basics to advanced concepts.
        3. For each step, provide 2-3 specific subtopics with detailed descriptions.
        4. Provide an 'explanation' of why this path is best for them.
        
        Requirements:
        - The roadmap must be highly detailed and professional.
        - Ensure the progression is logical and pedagogical.
        - For each module, provide 2-3 specific learning resources (articles, documentation, or tutorials) with valid URLs.
        """
        
        schema = """
        {
          "estimated_score": 0,
          "explanation": "Detailed explanation of the course structure...",
          "roadmap": [
            {
              "title": "Module 1: Title",
              "description": "Detailed description of what this module covers and why it is important...",
              "duration": "1 week",
              "resources": [
                  {"title": "GeeksforGeeks - Topic", "url": "https://www.geeksforgeeks.org"},
                  {"title": "Official Guide", "url": "https://docs.example.com"}
              ],
              "subtopics": [
                  {"title": "Subtopic 1", "description": "Detailed explanation of this subtopic..."},
                  {"title": "Subtopic 2", "description": "Detailed explanation of this subtopic..."}
              ]
            }
          ]
        }
        """
        
        result = await llm.generate_structured(prompt, schema)
        
        if isinstance(result, dict) and "roadmap" in result:
             # Ensure gap_analysis exists for the UI
             if "gap_analysis" not in result:
                 result["gap_analysis"] = "Personalized course generated for your interest."
             return result
             
        # Fallback
        return {
            "gap_analysis": "Interest-based learning path",
            "estimated_score": 0,
            "explanation": "A general path for " + topic,
            "roadmap": [
                {
                    "title": "Introduction to " + topic,
                    "description": "Foundational concepts and overview.",
                    "duration": "1 week",
                    "resources": [
                        {"title": f"{topic} Overview", "url": "https://en.wikipedia.org/wiki/" + topic.replace(' ', '_')}
                    ],
                    "subtopics": [
                        {"title": "History & Context", "description": "How this field evolved."},
                        {"title": "Key Terminology", "description": "Essential vocabulary."}
                    ]
                }
            ]
        }

roadmap_llm = RoadmapLLM()
