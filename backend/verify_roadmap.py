import asyncio
from app.services.roadmap_llm import roadmap_llm

async def main():
    print("Testing RoadmapLLM generation...")
    
    answers = {
        "q1": "I understand that React components are functions that return JSX, but I struggle with when to use state vs props.",
        "q2": "I know basic hooks like useState, but useEffect dependencies confuse me sometimes.",
        "q3": "I want to build a full-stack app but don't know how to connect React to a backend API securely."
    }
    
    profile = {
        "career_goals": "Full Stack Developer",
        "interests": ["Web Development", "AI"],
        "preferred_pace": "Fast"
    }
    
    try:
        result = await roadmap_llm.generate_roadmap(answers, profile)
        import json
        print(json.dumps(result, indent=2))
        
        if "roadmap" in result and len(result["roadmap"]) > 0:
            first_item = result["roadmap"][0]
            if "description" in first_item and "resources" in first_item:
                print("\n[SUCCESS] Roadmap generated with detailed descriptive items!")
            else:
                 print("\n[WARN] Roadmap items missing detailed fields.")
        else:
             print("\n[FAIL] No roadmap generated.")
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
