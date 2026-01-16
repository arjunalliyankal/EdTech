import asyncio
from app.services.qstair_llm import qstair_llm

async def main():
    print("Testing QstairLLM with topic 'Docker'...")
    try:
        questions = await qstair_llm.generate_questions("Docker")
        print("Received questions:")
        import json
        print(json.dumps(questions, indent=2))
        
        # Check if it's fallback
        if questions and questions[0]['text'].startswith("What is a core concept of"):
             print("\n[WARN] This looks like the FALLBACK response.")
        else:
             print("\n[SUCCESS] This looks like a REAL LLM response.")
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
