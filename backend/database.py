import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "jobs.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        title TEXT,
        company TEXT,
        location TEXT,
        posted TEXT,
        salary TEXT,
        link TEXT UNIQUE,
        description TEXT,
        easy_apply INTEGER,
        scraped_at TEXT,
        market_priority INTEGER,
        ai_score REAL DEFAULT 0,
        ai_summary TEXT DEFAULT '',
        applied INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def insert_job(job):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO jobs (
            source, title, company, location, posted, salary,
            link, description, easy_apply, scraped_at, market_priority
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job.get("source", ""),
            job.get("title", ""),
            job.get("company", ""),
            job.get("location", ""),
            job.get("posted", ""),
            job.get("salary", ""),
            job.get("link", ""),
            job.get("description", ""),
            int(job.get("easy_apply", False)),
            job.get("scraped_at", ""),
            int(job.get("market_priority", 0))
        ))

        conn.commit()
        inserted = True

    except sqlite3.IntegrityError:
        inserted = False

    conn.close()
    return inserted


def bulk_insert_jobs(job_list):
    inserted_count = 0
    duplicate_count = 0

    for job in job_list:
        if insert_job(job):
            inserted_count += 1
        else:
            duplicate_count += 1

    return {
        "inserted": inserted_count,
        "duplicates": duplicate_count
    }


def fetch_all_jobs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM jobs
    ORDER BY market_priority DESC, id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def mark_applied(job_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE jobs SET applied = 1 WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()