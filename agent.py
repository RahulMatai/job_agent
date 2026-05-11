import logging
from dotenv import load_dotenv
from fetcher import fetch_all_jobs
from job_scorer import score_job
from database import save_job
import time


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

def run_agent():
    """
    Main agent function:
    1. Fetches jobs from all sources
    2. Scores each job against Rahul's profile
    3. Saves matches to Supabase
    4. Returns count of new jobs saved
    """
    logger.info("🤖 Job Alert Agent starting...")
    
    # Step 1 — Fetch jobs
    jobs = fetch_all_jobs()
    logger.info(f"Fetched {len(jobs)} total jobs")
    
    if not jobs:
        logger.warning("No jobs fetched — check sources")
        return 0
    
    # Step 2 — Score and save
    new_jobs = 0
    for i, job in enumerate(jobs):
        logger.info(f"Processing job {i+1}/{len(jobs)}: {job['title']}")
        
        # Score job against profile
        score = score_job(job)
        time.sleep(1)  # 1 second delay to avoid rate limiting

        # Save all jobs but highlight high matches
        saved = save_job(
            title=job['title'],
            company=job['company'],
            location=job['location'],
            url=job['url'],
            source=job['source'],
            posted_at=job['posted_at'],
            description=job['description'],
            score=score
        )
        
        if saved:
            new_jobs += 1
            if score >= 70:
                logger.info(f"✅ Strong match found: {job['title']} — Score: {score}")
    
    logger.info(f"Agent completed — {new_jobs} new jobs saved")
    return new_jobs

if __name__ == "__main__":
    run_agent()