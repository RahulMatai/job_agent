# job_agent
# 🤖 AI Job Alert Agent

> Get AI-scored job matches from LinkedIn delivered to a dashboard — automatically.

## 🔗 Live App
_(add Streamlit Cloud URL after deployment)_

## 🎯 What it does
- Fetches jobs from LinkedIn for India and Ireland
- AI scores each job against your profile (0-100%)
- Shows all matches in a clean dashboard
- Filter by location, score, source and application status
- Mark jobs as applied to track your search

## 📁 Project Structure

| File | What it does |
|------|-------------|
| `app.py` | Streamlit UI — dashboard, filters, job cards |
| `agent.py` | Main orchestrator — runs fetch → score → save pipeline |
| `fetcher.py` | Fetches jobs from LinkedIn via web scraping |
| `scorer.py` | Groq AI scores each job against Rahul's profile |
| `database.py` | Supabase CRUD — save jobs, get jobs, mark applied |
| `requirements.txt` | Python dependencies |
| `SYSTEM_DESIGN.md` | Architecture and design decisions |

## 🛠️ Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Frontend | Streamlit | Fast, Python native |
| AI Scoring | Groq (Llama 3.3 70B) | Free, fast, accurate |
| Data Source | LinkedIn scraping | Best job coverage |
| Database | Supabase (PostgreSQL) | Free, persistent |
| Hosting | Streamlit Cloud | Free, one click deploy |

## ⚙️ How it works