import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Job search preferences
SEARCH_QUERIES = [
    "python backend developer",
    "AI ML engineer",
]

LOCATIONS = ["India", "Ireland"]

def fetch_linkedin_jobs(query, location, hours=8):
    """
    Fetch jobs from LinkedIn via web scraping.
    Returns jobs posted in last X hours.
    
    Args:
        query: job title e.g. "python developer"
        location: e.g. "India" or "Ireland"
        hours: only fetch jobs posted in last X hours
    """
    logger.info(f"Fetching LinkedIn jobs — query: {query}, location: {location}")
    
    seconds = hours * 3600
    
    url = (
        f"https://www.linkedin.com/jobs/search/"
        f"?keywords={query.replace(' ', '%20')}"
        f"&location={location.replace(' ', '%20')}"
        f"&f_TPR=r{seconds}"
        f"&position=1&pageNum=0"
    )
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        jobs = []
        job_cards = soup.find_all("div", class_="base-card")
        
        for card in job_cards[:50]:
            title = card.find("h3", class_="base-search-card__title")
            company = card.find("h4", class_="base-search-card__subtitle")
            location_el = card.find("span", class_="job-search-card__location")
            link = card.find("a", class_="base-card__full-link")
            
            if title and link:
                jobs.append({
                    "title": title.get_text(strip=True),
                    "company": company.get_text(strip=True) if company else "Unknown",
                    "location": location_el.get_text(strip=True) if location_el else location,
                    "url": link.get("href", ""),
                    "source": "LinkedIn",
                    "posted_at": "",
                    "description": ""
                })
        
        logger.info(f"Found {len(jobs)} jobs from LinkedIn")
        return jobs
        
    except Exception as e:
        logger.error(f"Failed to fetch LinkedIn jobs: {e}")
        return []

def fetch_all_jobs():
    """
    Fetches jobs from LinkedIn for all queries and locations.
    Deduplicates by URL.
    """
    logger.info("Starting job fetch...")
    all_jobs = []
    seen_urls = set()

    for query in SEARCH_QUERIES:
        for location in LOCATIONS:
            jobs = fetch_linkedin_jobs(query, location)
            for job in jobs:
                if job["url"] not in seen_urls and job["url"]:
                    seen_urls.add(job["url"])
                    all_jobs.append(job)

    logger.info(f"Total unique jobs fetched: {len(all_jobs)}")
    return all_jobs