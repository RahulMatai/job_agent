import streamlit as st
from database import get_jobs, mark_applied
from agent import run_agent

st.set_page_config(
    page_title="Job Alert Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Job Alert Agent")
st.caption("Real-time job matches from LinkedIn, Indeed and Naukri — scored by AI")

# Controls
col1, col2, col3, col4 = st.columns([2,1,1,1])

with col1:
    min_score = st.slider("Minimum Match Score", 0, 100, 70)

with col2:
    source_filter = st.selectbox("Source", 
        ["All", "LinkedIn", "Indeed", "Naukri"])

with col3:
    location_filter = st.selectbox("Location",
        ["All", "India", "Ireland"])

with col4:
    show_applied = st.selectbox("Status",
        ["All", "Not Applied", "Applied"])
# Run agent button
if st.button("🔄 Fetch New Jobs Now", use_container_width=True, type="primary"):
    with st.spinner("Fetching and scoring jobs..."):
        new_jobs = run_agent()
    st.success(f"✅ Found {new_jobs} new jobs!")
    st.rerun()
# Fetch jobs from database
applied_filter = None
if show_applied == "Not Applied":
    applied_filter = False
elif show_applied == "Applied":
    applied_filter = True

jobs = get_jobs(
    min_score=min_score,
    source=source_filter,
    applied=applied_filter,
    location=location_filter
)

# Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Jobs", len(jobs))
m2.metric("Strong Matches (70+)", len([j for j in jobs if j['score'] >= 70]))
m3.metric("Applied", len([j for j in jobs if j['applied']]))
m4.metric("Pending", len([j for j in jobs if not j['applied']]))

st.divider()

# Jobs list
if not jobs:
    st.info("No jobs found. Click 'Fetch New Jobs Now' to start!")
else:
    for job in jobs:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Score color
                if job['score'] >= 70:
                    score_color = "🟢"
                elif job['score'] >= 40:
                    score_color = "🟡"
                else:
                    score_color = "🔴"
                
                st.markdown(f"### {score_color} {job['title']}")
                st.markdown(f"**{job['company']}** · {job['location']} · `{job['source']}`")
                
                if job['description']:
                    st.caption(job['description'][:200] + "...")
                
                st.markdown(f"[Apply →]({job['url']})")
            
            with col2:
                st.markdown(f"### {job['score']}%")
                st.caption("Match Score")
                
                if not job['applied']:
                    if st.button("✅ Mark Applied", key=f"apply_{job['id']}"):
                        mark_applied(job['id'])
                        st.rerun()
                else:
                    st.success("Applied ✓")
                    