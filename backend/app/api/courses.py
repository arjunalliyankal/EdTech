
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from app.api.profile import get_current_user_id
from app.services.pdf_service import pdf_service
from app.core.database import db
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class Subtopic(BaseModel):
    title: str
    description: str

class Module(BaseModel):
    title: str
    description: str
    subtopics: List[Subtopic]

class Course(BaseModel):
    id: Optional[str]
    title: str
    description: str
    modules: List[Module]
    instructor_id: str
    status: str = "active"

@router.post("/upload", response_model=Course)
async def upload_course(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
):
    """
    Uploads a PDF and converts it into a course structure.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        content = await file.read()
        
        # 1. Extract Text
        text = pdf_service.extract_text_from_pdf(content)
        
        # 2. Generate Course Structure via LLM
        course_data = await pdf_service.generate_course_from_content(text, file.filename)
        
        # 3. Save to Database
        course_doc = {
            "title": course_data.get("title", "Untitled Course"),
            "description": course_data.get("description", ""),
            "modules": course_data.get("modules", []),
            "instructor_id": user_id,
            "status": "draft", # Start as draft
            "source_file": file.filename
        }
        
        new_course = await db.client.edtech_platform.courses.insert_one(course_doc)
        
        return {
            "id": str(new_course.inserted_id),
            **course_doc
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"Course upload failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during course processing")

@router.get("/my-courses")
async def get_my_courses(user_id: str = Depends(get_current_user_id)):
    """
    Retrieves courses created by the current mentor.
    """
    cursor = db.client.edtech_platform.courses.find({"instructor_id": user_id})
    courses = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        courses.append(doc)
    return courses
