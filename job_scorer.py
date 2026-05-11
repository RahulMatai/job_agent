import os
import json
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Rahul's profile — AI uses this to score jobs
RAHUL_PROFILE = """
Name: Rahul Matai
Experience: 4+ years
Current Location: Vadodara, India
Open to: India (any city) and Ireland 

Target Roles:
- Backend Engineer (Python)
- Software Developer
- ML/AI Engineer
- Agentic AI Developer

Core Skills:
- Python (Advanced) — FastAPI, Flask, Django
- AI/ML — RAG, LangChain, FAISS, LLMs, Groq
- Cloud — AWS, Azure, GCP
- Databases — PostgreSQL, SQLite, Supabase, MongoDB
- DevOps — Docker, Git
- JavaScript, Java

Education:
- MSc Computer Science — University College Dublin (2022-2023)
- Masters Computer Science — Symbiosis Institute (2019-2021)

Experience:
- Contract Software Engineer — 2 years (Dublin, Ireland)
- Microsoft Software Developer — 4 months (Dublin)
- Innovate Tax Software Developer — 2 years (UK)
"""

def get_groq_client():
    """Get Groq client"""
    try:
        import streamlit as st
        key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    except Exception:
        key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=key)

def score_job(job):
    """
     Score a job against Rahul's profile using Groq AI.
    
    Returns a score from 0-100:
    - 0-40: Poor match
    - 41-70: Moderate match  
    - 71-100: Strong match
    
    Uses structured JSON response for reliable parsing.
    """
    logger.info(f"Scoring job: {job['title']} at {job['company']}")
    client = get_groq_client()
    prompt = f"""
    You are a job matching expert. Score how well this job matches the candidate profile.
    
    CANDIDATE PROFILE:
    {RAHUL_PROFILE}
    
    JOB:
    Title: {job['title']}
    Company: {job['company']}
    Location: {job['location']}
    Description: {job['description'][:500] if job['description'] else 'Not provided'}
    
    Score this job from 0-100 based on:
    - Role match (0-25): Does the role match target roles?
    - Skills match (0-25): Do required skills match candidate skills?
    - Location match (0-25): Is location India or Ireland?
    - Experience match (0-25): Does experience level match?
    
    Return ONLY this JSON:
    {{
        "score": <total 0-100>,
        "role_match": <0-25>,
        "skills_match": <0-25>,
        "location_match": <0-25>,
        "experience_match": <0-25>,
        "reason": "<one line explanation>"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        
        content = response.choices[0].message.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()
        result = json.loads(content)
        
        logger.info(f"Score: {result['score']} — {result['reason']}")
        return result['score']
        
    except Exception as e:
        logger.error(f"Failed to score job: {e}")
        return 0