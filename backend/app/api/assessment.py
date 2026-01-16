from fastapi import APIRouter, Depends, HTTPException
from app.models.assessment import QuestionBase, AssessmentSubmission, AssessmentResult, RoadmapItem, Subtopic
from app.services.ai_analysis import analyze_skill_gaps
from app.api.profile import get_current_user_id
from app.core.database import db

from app.services.agents.student_llm import student_agent
from app.services.qstair_llm import qstair_llm

router = APIRouter()

@router.get("/diagnostic", response_model=list[QuestionBase])
async def get_diagnostic_questions(topic: str = None, user_id: str = Depends(get_current_user_id)):
    # Fetch profile for context
    profile = await db.client.edtech_platform.profiles.find_one({"user_id": user_id})
    if not profile:
        profile = {"career_goals": "Not set", "interests": [], "preferred_pace": "medium"}
    
    # Use QstairLLM if a topic is provided, otherwise fallback to generic StudentAgent logic
    if topic:
        questions = await qstair_llm.generate_questions(topic)
    else:
        questions = await student_agent.generate_diagnostic(profile)
        
    if not questions:
        # Fallback to defaults if logic fails
        return [
            QuestionBase(id="q1", text="What is the complexity of binary search?", type="mcq", options=["O(log n)", "O(n)", "O(1)", "O(n^2)"]),
            QuestionBase(id="q2", text="Which protocol is stateless?", type="mcq", options=["HTTP", "FTP", "SMTP", "SSH"]),
        ]
    return questions

from app.services.roadmap_llm import roadmap_llm

# ... imports ...

from fastapi.responses import JSONResponse

@router.post("/submit", response_model=AssessmentResult)
async def submit_assessment(submission: AssessmentSubmission, user_id: str = Depends(get_current_user_id)):
    try:
        profile = await db.client.edtech_platform.profiles.find_one({"user_id": user_id})
        
        # Analyze answers using RoadmapLLM (Real AI)
        analysis = await roadmap_llm.generate_roadmap(
            submission.answers, 
            profile or {}
        )
        
        # Convert LLM dicts to RoadmapItem objects
        # Validate that analysis['roadmap'] is actually a list of dicts
        llm_roadmap = analysis.get("roadmap")
        if not isinstance(llm_roadmap, list):
             llm_roadmap = []
             
        roadmap_items = []
        for m in llm_roadmap:
            if isinstance(m, dict):
                # Extract subtopics safely
                raw_subs = m.get("subtopics")
                if not isinstance(raw_subs, list):
                    raw_subs = []
                
                subtopics_list = []
                for s in raw_subs:
                    if isinstance(s, dict):
                         subtopics_list.append(Subtopic(
                             title=s.get("title", "Untitled"),
                             description=s.get("description", "")
                         ))
                
                roadmap_items.append(RoadmapItem(
                    title=m.get("title", "Untitled"),
                    description=m.get("description", ""),
                    duration=m.get("duration", "1 week"),
                    resources=m.get("resources") or [],
                    subtopics=subtopics_list
                ))
            else:
                 # Skip or handle malformed items (strings, etc) if necessary
                 pass
        
        result_data = AssessmentResult(
            user_id=user_id,
            score=analysis.get("estimated_score", 70),
            gap_analysis=analysis.get("explanation", "Analysis completed."),
            recommended_path=roadmap_items
        )
        
        # Store FULL analysis in DB for rich display
        db_record = result_data.dict()
        db_record['full_roadmap'] = analysis.get("roadmap", []) 
        
        await db.client.edtech_platform.assessment_results.insert_one(db_record)
        
        return result_data
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": f"Internal Server Error: {str(e)}"})

@router.get("/latest", response_model=AssessmentResult)
async def get_latest_assessment(user_id: str = Depends(get_current_user_id)):
    result = await db.client.edtech_platform.assessment_results.find_one(
        {"user_id": user_id},
        sort=[("timestamp", -1)]
    )
    if not result:
        raise HTTPException(status_code=404, detail="No assessment results found")
    return result
