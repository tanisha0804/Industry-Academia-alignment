import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Industry–Academia Alignment Dashboard",
    layout="wide"
)

DATA_DIR = Path("outputs/processed_data")

# ---------------- HELPERS ----------------
def load_json(name):
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(skill: str) -> str:
    return skill.lower().strip()

# ---------------- LOAD DATA ----------------
industry_raw = load_json("industry_skill_universe.json")
university_raw = load_json("university_skill_universe_v2.json")
priority_raw = load_json("skill_priority_scores.json")
courses = load_json("course_proposals.json")

# ---------------- NORMALIZE SKILLS ----------------
industry_map = {normalize(s): s for s in industry_raw}
university_map = {normalize(s): s for s in university_raw}

industry_norm = set(industry_map.keys())
university_norm = set(university_map.keys())

missing_norm = industry_norm - university_norm
covered_norm = industry_norm & university_norm

missing_skills = [industry_map[s] for s in sorted(missing_norm)]
covered_skills = [industry_map[s] for s in sorted(covered_norm)]

# ---------------- PRIORITY ----------------
priority_norm = {
    normalize(k): v for k, v in priority_raw.items()
}

missing_priority = {
    industry_map[s]: priority_norm.get(s, 0)
    for s in missing_norm
}

coverage_pct = round(
    (len(covered_norm) / len(industry_norm)) * 100, 2
)

# ---------------- SIDEBAR STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "Skill Gap Analysis"

page = st.sidebar.radio(
    "Navigation",
    ["Skill Gap Analysis", "Course Proposals", "Course Overview"],
    index=["Skill Gap Analysis", "Course Proposals", "Course Overview"].index(st.session_state.page)
)

st.session_state.page = page

# ==================================================
# 📊 SKILL GAP ANALYSIS
# ==================================================
if page == "Skill Gap Analysis":
    st.title("📊 Industry–Academia Skill Gap Analysis")

    c1, c2, c3 = st.columns(3)
    c1.metric("Industry Skills", len(industry_norm))
    c2.metric("University Skills", len(university_norm))
    c3.metric("Coverage %", f"{coverage_pct}%")

    st.divider()

    # ---- PIE (FIXED) ----
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        [len(covered_norm), len(missing_norm)],
        labels=["Covered", "Missing"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title("Industry Skill Coverage")
    st.pyplot(fig)

    st.divider()

    # ---- PRIORITY BAR (FIXED) ----
    df = (
        pd.DataFrame(missing_priority.items(), columns=["Skill", "Priority"])
        .sort_values("Priority", ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(df["Skill"], df["Priority"])
    ax.set_title("Top Missing Industry Skills (Priority)")
    ax.invert_yaxis()
    st.pyplot(fig)

    with st.expander("📌 View Missing Skills"):
        st.write(missing_skills)

# ==================================================
# 📚 COURSE PROPOSALS
# ==================================================
elif page == "Course Proposals":
    st.title("📚 Proposed Courses")

    courses_sorted = sorted(
        courses, key=lambda c: int(c["course_id"].replace("C", ""))
    )

    df = []
    for c in courses_sorted:
        df.append({
            "Course ID": c["course_id"],
            "Target Year": c["target_year"],
            "Skills": ", ".join(s["skill"] for s in c["skills"]),
            "Status": c["status"]
        })

    st.dataframe(pd.DataFrame(df), use_container_width=True)

    st.divider()

    for idx, c in enumerate(courses_sorted):
        cols = st.columns([2, 1, 1, 1])

        cols[0].markdown(f"**{c['course_id']}**")

        if cols[1].button("View Description", key=f"view_{idx}"):
            st.session_state.selected_course = c
            st.session_state.page = "Course Overview"
            st.rerun()

        if cols[2].button("Accept", key=f"accept_{idx}"):
            c["status"] = "accepted"
            json.dump(courses, open(DATA_DIR / "course_proposals.json", "w"), indent=2)
            st.success("Course Accepted")

        if cols[3].button("Reject", key=f"reject_{idx}"):
            c["status"] = "rejected"
            json.dump(courses, open(DATA_DIR / "course_proposals.json", "w"), indent=2)
            st.error("Course Rejected")

# ==================================================
# 📖 COURSE OVERVIEW
# ==================================================
elif page == "Course Overview":
    if "selected_course" not in st.session_state:
        st.warning("Select a course from Course Proposals")
    else:
        c = st.session_state.selected_course

        st.title(f"📖 {c['course_id']}")
        st.markdown(f"**Target Year:** {c['target_year']}")

        st.markdown("**Skills Covered**")
        st.write([s["skill"] for s in c["skills"]])

        st.divider()

        st.markdown("**Course Objectives**")
        st.markdown(c["overview"]["raw_text"])
