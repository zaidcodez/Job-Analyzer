import re


def load_resume(path="resume/my_resume.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().lower()
    except FileNotFoundError:
        return ""


def extract_keywords(text):
    text = text.lower()

    keywords = [
        "python", "django", "flask", "fastapi",
        "machine learning", "ai", "data science",
        "sql", "postgresql", "mysql",
        "docker", "kubernetes",
        "aws", "azure", "gcp",
        "react", "node", "javascript",
        "pandas", "numpy",
        "nlp", "llm"
    ]

    found = []
    for kw in keywords:
        if kw in text:
            found.append(kw)

    return set(found)


def score_job(job_description, resume_text):
    if not job_description:
        return 0, "No description available"

    job_text = job_description.lower()
    resume_text = resume_text.lower()

    job_keywords = extract_keywords(job_text)
    resume_keywords = extract_keywords(resume_text)

    if not job_keywords:
        return 10, "No clear technical keywords detected in job"

    matches = job_keywords.intersection(resume_keywords)

    score = int((len(matches) / len(job_keywords)) * 100)

    # boost for Pakistan-friendly signals
    if any(x in job_text for x in ["remote", "karachi", "lahore", "islamabad"]):
        score += 10

    if "junior" in job_text or "entry" in job_text:
        score += 5

    score = min(score, 100)

    missing = job_keywords - resume_keywords

    summary = f"""
Matched skills: {', '.join(matches) if matches else 'None'}
Missing skills: {', '.join(list(missing)[:5]) if missing else 'None'}
"""

    return score, summary.strip()


def analyze_job(job):
    resume_text = load_resume()

    score, summary = score_job(
        job.get("description", ""),
        resume_text
    )

    return {
        "score": score,
        "summary": summary
    }