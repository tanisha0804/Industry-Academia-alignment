# AI-Driven Industry–Academia Curriculum Alignment System

## 📌 Problem Statement
Technologies used by industries evolve rapidly, while university curriculum are updated infrequently. This results in a significant skill gap where graduates are not fully prepared for industry expectations, especially during internships and placements.

This project aims to bridge the gap between **industry-required skills** and **university-taught curriculum** using **AI, NLP, and trend analysis**, enabling data-driven curriculum updates.

---

## 🎯 Objectives
1. Analyze industry job descriptions and university handbooks.
2. Identify skill gaps and syllabus misalignment (e.g., skills taught too late).
3. Quantify the impact of curriculum gaps on placements and companies.
4. Track emerging industry trends using company career pages.
5. Recommend priority topics based on trends.
6. Generate overview and full syllabi for new or updated courses.
7. Demonstrate benefits of syllabus updates in terms of placement readiness.

---

## 🧠 System Overview
The system consists of the following modules:

### 1️⃣ Industry Analysis Module
- Extracts skills from job descriptions
- Normalizes and clusters technologies
- Builds an industry skill knowledge base

### 2️⃣ University Curriculum Analysis Module
- Parses university handbooks (semester-wise)
- Extracts courses, topics, tools, and electives
- Builds a curriculum knowledge base

### 3️⃣ Skill Gap Analysis Engine
- Compares industry skills vs curriculum topics
- Identifies:
  - Missing skills
  - Partially covered skills
  - Skills taught too late

### 4️⃣ Trend Update Module (Company Career Pages)
- Periodically extracts skill signals from public career pages
- Detects trending, stable, and declining technologies
- Computes:
  - Skill Growth Rate
  - Skill Freshness Score
  - Industry Volatility Index

### 5️⃣ Curriculum Recommendation Engine
- Suggests:
  - New courses
  - Updated modules
  - Semester re-mapping
- Generates overview syllabus for faculty review
- Generates full syllabus upon approval

### 6️⃣ Visualization & Dashboard Module
- Skill coverage heatmaps
- Semester vs industry demand charts
- Trend timelines
- Curriculum alignment scores

---

