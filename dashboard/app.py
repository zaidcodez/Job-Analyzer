import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

from backend.insights import generate_insights

DB_PATH = Path(__file__).resolve().parent.parent / "backend" / "jobs.db"


def get_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM jobs ORDER BY market_priority DESC, id DESC", conn)
    conn.close()
    return df


def mark_applied(job_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET applied = 1 WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()


st.set_page_config(page_title="PakTech Job Copilot", layout="wide")

st.title("🇵🇰 PakTech Job Copilot")
st.caption("AI-powered job intelligence system for Pakistan tech market")

df = get_data()

if df.empty:
    st.warning("No jobs found. Start scraping using the extension.")
    st.stop()


# -------------------- INSIGHTS PANEL --------------------

st.header("📊 Market Intelligence Dashboard")

insights = generate_insights()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Jobs", insights.get("total_jobs", 0))
col2.metric("Avg AI Score", insights.get("average_ai_score", 0))
col3.metric("Top Skill", insights["top_skills"][0][0] if insights.get("top_skills") else "N/A")
hot = insights.get("hot_skills_trend", [])

top_skill = hot[0][0] if hot else "N/A"
top_count = hot[0][1] if hot else 0

col4.metric("Hot Skill Trend", top_skill, top_count)


st.subheader("🔥 Top Skills in Pakistan Tech Market")
st.write(pd.DataFrame(insights.get("top_skills", []), columns=["Skill", "Mentions"]))

st.subheader("🏢 Top Hiring Companies")
st.write(pd.DataFrame(insights.get("top_companies", []), columns=["Company", "Jobs"]))

st.subheader("📍 Job Locations Distribution")
st.write(pd.DataFrame(insights.get("top_locations", []), columns=["Location", "Jobs"]))


st.markdown("---")


# -------------------- JOB FILTERING --------------------

st.header("📌 Job Listings")

st.sidebar.header("Filters")

sources = st.sidebar.multiselect(
    "Source",
    options=df["source"].unique(),
    default=df["source"].unique()
)

show_applied = st.sidebar.checkbox("Show Applied Jobs", value=True)

min_priority = st.sidebar.slider("Minimum Market Priority", 0, 100, 0)

filtered = df[
    (df["source"].isin(sources)) &
    (df["market_priority"] >= min_priority)
]

if not show_applied:
    filtered = filtered[filtered["applied"] == 0]

filtered = filtered.sort_values(by=["ai_score", "market_priority"], ascending=False)


st.write(f"Showing {len(filtered)} jobs")

for _, row in filtered.iterrows():
    with st.container():
        st.markdown("---")

        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader(row["title"])
            st.write(f"**Company:** {row['company']}")
            st.write(f"**Location:** {row['location']}")
            st.write(f"**Source:** {row['source']}")

            st.write(f"**Market Priority:** {row['market_priority']}")
            st.write(f"**AI Score:** {row['ai_score']}")

            if row["ai_summary"]:
                st.info(row["ai_summary"])

        with col2:
            st.metric("AI Score", row["ai_score"])

            st.link_button("Open Job", row["link"])

            if row["applied"] == 0:
                if st.button(f"Mark Applied #{row['id']}"):
                    mark_applied(row["id"])
                    st.success("Marked as applied")
                    st.rerun()
            else:
                st.success("Applied")