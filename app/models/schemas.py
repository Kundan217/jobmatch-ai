from pydantic import BaseModel


class AnalysisResult(BaseModel):
    id: int
    resume_name: str
    job_title: str
    match_score: int
    ats_score: int
    matching_skills: list[str]
    missing_skills: list[str]
    resume_summary: str
    suggestions: list[str]
    created_at: str
