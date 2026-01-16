import asyncio
from app.services.agents.student_agent import student_agent
from app.models.assessment import AssessmentResult

async def main():
    print("Testing Roadmap Generation...")
    
    # Mock data
    answers = {"q1": "O(n)", "q2": "HTTP"}
    text_input = "I struggle with understanding time complexity and recursion."
    profile = {"career_goals": "Backend Developer", "interests": ["Python", "API"], "preferred_pace": "medium"}
    
    try:
        analysis = await student_agent.analyze_and_roadmap(answers, text_input, profile)
        print("\nRaw LLM Output:")
        print(analysis)
        
        # Verify Pydantic validation
        result = AssessmentResult(
            user_id="test_user",
            score=analysis.get("estimated_score", 0),
            gap_analysis=analysis.get("explanation", ""),
            recommended_path=analysis.get("roadmap", [])
        )
        print("\nValidated AssessmentResult:")
        print(result.model_dump_json(indent=2))
        
        with open("test_result.txt", "w") as f:
            f.write("SUCCESS: Roadmap structure is valid.\n")
            f.write(result.model_dump_json(indent=2))
        print("\nSUCCESS: Roadmap structure is valid.")
        
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())
