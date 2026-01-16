import random

def analyze_skill_gaps(answers: dict, text_input: str) -> dict:
    # MOCK AI ANALYSIS
    # In real implementation, use BERT/TF-IDF here
    
    gaps = []
    if "python" in text_input.lower():
        gaps.append("Advanced Python Concepts")
    if "deployment" in text_input.lower():
        gaps.append("CI/CD Pipelines")
        
    if not gaps:
        gaps = ["General Fundamentals"]
        
    return {
        "identified_gaps": gaps,
        "recommendation": f"Focus on {', '.join(gaps)} based on your input.",
        "roadmap": ["Module 1: " + g for g in gaps]
    }
