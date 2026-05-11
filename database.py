import os
import logging

logger = logging.getLogger(__name__)

def get_supabase_client():
    """
    Returns Supabase client
    """
    try:
        import streamlit as st
        url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
    except Exception:
        from dotenv import load_dotenv
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
    
    from supabase import create_client
    return create_client(url, key)

supabase = get_supabase_client()

def save_job(title,company,location,url,source,posted_at,description,score):
    """
    for keeping track of jobs
    
    """
    try:
        supabase.table("jobs").insert({
            "title": title,
            "company": company,
            "location": location,
            "url": url,
            "source": source,
            "posted_at": posted_at,
            "description": description,
            "score": score,
        }).execute()
        logger.info(f"Saved job: {title} at {company}")
        return True
    except Exception as e:
        # URL unique constraint — job already exists
        logger.debug(f"Job already exists: {title}")
        return False

def get_jobs(min_score=0, source=None, applied=None, location=None):
    query = supabase.table("jobs")\
        .select("*")\
        .gte("score", min_score)\
        .order("score", desc=True)\
        .order("created_at", desc=True)
    
    if source and source != "All":
        query = query.eq("source", source)
    
    if applied is not None:
        query = query.eq("applied", applied)
    
    if location and location != "All":
        query = query.ilike("location", f"%{location}%")
    
    response = query.execute()
    return response.data

def mark_applied(job_id):
    """Mark a job as applied"""
    supabase.table("jobs")\
        .update({"applied": True})\
        .eq("id", job_id)\
        .execute()
    logger.info(f"Marked job {job_id} as applied")

        
    
    