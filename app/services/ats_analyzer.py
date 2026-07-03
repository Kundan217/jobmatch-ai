import re


def calculate_ats_score(resume_text: str, matching_skills: list[str], missing_skills: list[str]) -> tuple[int, list[str]]:
    score = 40
    suggestions: list[str] = []
    words = resume_text.split()
    lowered = resume_text.lower()

    if 350 <= len(words) <= 1200:
        score += 15
    else:
        suggestions.append("Keep the resume between 1 and 2 focused pages with concise role details.")

    if re.search(r"[\w.-]+@[\w.-]+\.\w+", resume_text) and re.search(r"\+?\d[\d\s().-]{8,}", resume_text):
        score += 10
    else:
        suggestions.append("Add clear contact details including email and phone number.")

    for section in ("education", "experience", "projects"):
        if section in lowered:
            score += 7
        else:
            suggestions.append(f"Add a dedicated {section.title()} section.")

    if matching_skills:
        score += min(14, len(matching_skills) * 3)
    if missing_skills:
        suggestions.append("Add relevant missing skills where you have real experience: " + ", ".join(missing_skills[:6]) + ".")

    if not re.search(r"\b\d+%|\b\d+\+|\b\d+x\b", lowered):
        suggestions.append("Mention quantified achievements such as percentages, scale, revenue, latency, or users.")

    return max(0, min(100, score)), suggestions[:6]
