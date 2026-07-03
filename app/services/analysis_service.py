from app.services.ats_analyzer import calculate_ats_score
from app.services.embedding_service import similarity_service
from app.services.skill_analyzer import analyze_skill_gap


def infer_job_title(job_description: str) -> str:
    for line in job_description.splitlines():
        clean = line.strip(" :-\t")
        if clean and len(clean.split()) <= 8:
            return clean[:80]
    return "Untitled Role"


def summarize_resume(resume_text: str) -> str:
    sentences = [part.strip() for part in resume_text.replace("\n", " ").split(".") if part.strip()]
    if not sentences:
        return "No readable resume summary could be extracted."
    return ". ".join(sentences[:2])[:420] + ("..." if len(". ".join(sentences[:2])) > 420 else ".")


def analyze_resume(resume_name: str, resume_text: str, job_description: str) -> dict:
    match_score = similarity_service.score(resume_text, job_description)
    matching_skills, missing_skills = analyze_skill_gap(resume_text, job_description)
    ats_score, suggestions = calculate_ats_score(resume_text, matching_skills, missing_skills)
    return {
        "resume_name": resume_name,
        "job_title": infer_job_title(job_description),
        "match_score": match_score,
        "ats_score": ats_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "resume_summary": summarize_resume(resume_text),
        "suggestions": suggestions,
    }
