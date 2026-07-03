import re


SKILLS = {
    "python",
    "fastapi",
    "flask",
    "django",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "node",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "linux",
    "rest api",
    "machine learning",
    "nlp",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "faiss",
    "redis",
    "ci/cd",
    "testing",
    "pytest",
}


def extract_skills(text: str) -> set[str]:
    normalized = text.lower()
    found = set()
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9+#.-])" + re.escape(skill) + r"(?![a-z0-9+#.-])"
        if re.search(pattern, normalized):
            found.add(skill)
    return found


def analyze_skill_gap(resume_text: str, job_description: str) -> tuple[list[str], list[str]]:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    matching = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    return matching, missing
