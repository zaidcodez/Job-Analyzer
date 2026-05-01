from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import (
    initialize_database,
    bulk_insert_jobs,
    fetch_all_jobs,
    mark_applied
)

from backend.ai_matcher import analyze_job

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()


@app.get("/")
def home():
    return {"message": "PakTech Job Copilot Backend Running with AI Layer"}


from fastapi import Request

@app.post("/save-jobs")
async def save_jobs(request: Request):
    jobs = await request.json()

    enriched_jobs = []

    for job in jobs:
        # safe AI call (prevents crash if bad data comes in)
        try:
            ai_result = analyze_job(job)
            score = ai_result.get("score", 0)
            summary = ai_result.get("summary", "")
        except:
            score = 0
            summary = "No AI analysis"

        cleaned_job = {
            "source": job.get("source", "unknown"),
            "title": job.get("title", "No title"),
            "company": job.get("company", "Unknown"),
            "location": job.get("location", ""),
            "posted": job.get("posted", ""),
            "salary": job.get("salary", ""),
            "link": job.get("link", ""),
            "description": job.get("description", ""),
            "easy_apply": bool(job.get("easy_apply", False)),
            "scraped_at": job.get("scraped_at"),
            "market_priority": job.get("market_priority", 50),
            "ai_score": score,
            "ai_summary": summary
        }

        enriched_jobs.append(cleaned_job)

    result = bulk_insert_jobs(enriched_jobs)

    return {
        "status": "success",
        "inserted": result["inserted"],
        "duplicates": result["duplicates"]
    }


@app.get("/all-jobs")
def all_jobs():
    return fetch_all_jobs()


@app.post("/mark-applied/{job_id}")
def applied(job_id: int):
    mark_applied(job_id)
    return {"status": "updated", "job_id": job_id}