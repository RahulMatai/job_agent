## AI Scoring Logic
For each job, Groq AI will score:
- Role match (0-25)
- Skills match (0-25)
- Location match (0-25)
- Experience match (0-25)
Total = 0-100%

## Tech Stack
| Layer | Choice |
|-------|--------|
| Language | Python |
| Frontend | Streamlit |
| AI Scoring | Groq (Llama 3.3) |
| Database | Supabase |
| Scraping | BeautifulSoup + Selenium |
| Scheduling | APScheduler |
| Alerts | Gmail SMTP |
| Hosting | Streamlit Cloud |