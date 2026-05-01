from backend.database import fetch_all_jobs
from collections import Counter
import re


# =========================
# CLEAN JOB ACCESS
# =========================
def get_all_jobs():
    return fetch_all_jobs()


# =========================
# EXPERIENCE EXTRACTION
# =========================
def extract_experience(text):
    if not text:
        return "unknown"

    match = re.search(r"(\d+\+?\s*(years|yrs))", text.lower())
    return match.group(0) if match else "not specified"


# =========================
# ROLE CLASSIFICATION (CORE UPGRADE)
# =========================
def classify_role(text):
    text = text.lower()

    if "mern" in text:
        return "mern"
    if "full stack" in text:
        return "full_stack"
    if "frontend" in text or "react" in text or "vue" in text:
        return "frontend"
    if "backend" in text or "django" in text or "flask" in text or "fastapi" in text:
        return "backend"
    if "python" in text:
        return "python_dev"
    if "ai" in text or "ml" in text or "llm" in text:
        return "ai_ml"
    if "devops" in text or "docker" in text or "kubernetes" in text:
        return "devops"
    if "mobile" in text or "flutter" in text or "android" in text:
        return "mobile"

    return "other"


# =========================
# SKILL EXTRACTION (IMPROVED)
# =========================
def extract_skills(text):
    if not text:
        return []

    text = text.lower()

    skills = [
        "python", "django", "flask", "fastapi",
        "sql", "postgresql", "mysql",
        "docker", "kubernetes",
        "aws", "azure", "gcp",
        "react", "node", "javascript",
        "typescript",
        "pandas", "numpy",
        "nlp", "llm"
    ]

    return [skill for skill in skills if skill in text]


# =========================
# MARKET ANALYSIS
# =========================
def role_distribution(jobs):
    roles = []

    for job in jobs:
        text = f"{job.get('title','')} {job.get('description','')}"
        roles.append(classify_role(text))

    return Counter(roles).most_common()


def top_skills_in_market(jobs):
    skill_counter = Counter()

    for job in jobs:
        text = f"{job.get('title','')} {job.get('description','')}"
        skills = extract_skills(text)
        skill_counter.update(skills)

    return skill_counter.most_common(10)


def top_companies(jobs):
    companies = [job.get("company", "unknown") for job in jobs]
    return Counter(companies).most_common(10)


def top_locations(jobs):
    locations = [job.get("location", "unknown") for job in jobs]
    return Counter(locations).most_common(10)


def experience_distribution(jobs):
    exp = []

    for job in jobs:
        text = f"{job.get('title','')} {job.get('description','')}"
        exp.append(extract_experience(text))

    return Counter(exp).most_common()


def avg_ai_score(jobs):
    scores = [job.get("ai_score", 0) for job in jobs]

    if not scores:
        return 0

    return sum(scores) / len(scores)


# =========================
# TREND ANALYSIS (FIXED — LESS AI BIAS)
# =========================
def market_skill_trends(jobs):
    all_skills = Counter()

    for job in jobs:
        text = f"{job.get('title','')} {job.get('description','')}"
        all_skills.update(extract_skills(text))

    return all_skills.most_common(8)


# =========================
# FINAL INSIGHTS ENGINE
# =========================
def generate_insights():
    jobs = get_all_jobs()

    if not jobs:
        return {"message": "No jobs available for analysis"}

    return {
        "total_jobs": len(jobs),

        # ROLE LEVEL INSIGHTS (NEW)
        "role_distribution": role_distribution(jobs),

        # SKILLS
        "top_skills": top_skills_in_market(jobs),
        "hot_skills_trend": market_skill_trends(jobs),

        # MARKET STRUCTURE
        "top_companies": top_companies(jobs),
        "top_locations": top_locations(jobs),
        "experience_distribution": experience_distribution(jobs),

        # AI (still included but not dominant anymore)
        "average_ai_score": round(avg_ai_score(jobs), 2)
    }