from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class QuestionBase(BaseModel):
    id: str
    text: str
    type: str # 'mcq' or 'text'
    options: Optional[List[str]] = None

class AssessmentSubmission(BaseModel):
    answers: dict # {question_id: answer}
    text_input: str # Descriptive text about struggles

class Subtopic(BaseModel):
    title: str
    description: str

class Resource(BaseModel):
    title: str
    url: str

class RoadmapItem(BaseModel):
    title: str
    description: str
    duration: str = "1 week"
    resources: List[Resource] = []
    subtopics: List[Subtopic] = []

class AssessmentResult(BaseModel):
    user_id: str
    score: int
    gap_analysis: str
    recommended_path: List[RoadmapItem]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AssessmentResultInDB(AssessmentResult):
    pass
