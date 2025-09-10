import os
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env
client = OpenAI(api_key="sk-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")


 # Uses OPENAI_API_KEY from environment

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "skills_dataset.csv")


def load_role_skills():
    try:
        df = pd.read_csv(DATA_PATH)
        # Normalize columns
        df['role'] = df['role'].str.strip().str.lower()
        df['skills'] = df['skills'].fillna('').astype(str)
        return df
    except Exception as e:
        return pd.DataFrame(columns=["role","skills"])

def _chat(prompt: str, model: str = "gpt-4o-mini") -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role":"system","content":"You are an expert AI career mentor for students."},
                  {"role":"user","content":prompt}],
        temperature=0.4,
    )
    return resp.choices[0].message.content

def get_career_paths(skills: str, interests: str, education: str, experience: str) -> str:
    prompt = f"""
    Profile:
    - Education: {education}
    - Experience: {experience}
    - Skills: {skills}
    - Interests: {interests}

    Task: Suggest 4-6 high-demand career paths suitable for the profile in India, with for each:
    - What the role does (1-2 lines)
    - Why it's a fit for this profile
    - 3 must-have skills
    - Typical starter projects
    - Entry-level compensation range (INR, realistic)
    Format as markdown with headings and bullet points.
    """
    return _chat(prompt)

def analyze_skill_gaps(user_skills_csv: str, target_role: str, role_skills_df: pd.DataFrame):
    user = {s.strip().lower() for s in user_skills_csv.split(",") if s.strip()}
    role = (target_role or "data analyst").strip().lower()
    # find matching role rows and collect skills
    rows = role_skills_df[role_skills_df['role'] == role]
    required = set()
    for _, r in rows.iterrows():
        required.update({x.strip().lower() for x in str(r['skills']).split(",") if x.strip()})
    # If dataset has nothing, provide a minimal default
    if not required:
        required = {"python","sql","statistics","excel","data visualization","etl","power bi","tableau"}
    gaps = sorted(list(required - user))
    matches = sorted(list(required & user))
    coverage = 0 if not required else int((len(matches) / len(required)) * 100)
    return {
        "target_role": role,
        "have_skills": matches,
        "missing_skills": gaps,
        "coverage_percent": coverage
    }

def get_learning_plan(skills: str, interests: str, duration: str, target_role: str) -> str:
    prompt = f"""
    Create a step-by-step learning plan to become a strong {target_role or 'Data Analyst'} in {duration}.
    Student's current skills: {skills}
    Interests: {interests}
    Structure:
    - Phases with timelines (Week 1-2, etc.)
    - Exact outcomes and checkpoints
    - Free resources (YouTube, docs, datasets, practice sites)
    - 3 portfolio projects with acceptance criteria and how to present results
    Keep it concise, actionable, and India-centric.
    """
    return _chat(prompt)
