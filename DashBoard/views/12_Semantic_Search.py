import streamlit as st
import pandas as pd
import random
import time
from components.utils import load_css, render_page_header
from components.charts import create_kpi_card

load_css()

render_page_header("Semantic Intelligence Search", "Use natural language to query our entire vector database of financial intelligence, filings, and news.")

# --- Session State for Search ---
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "trigger_search" not in st.session_state:
    st.session_state.trigger_search = False

# --- Mock Database ---
mock_db = {
    "ai regulations": [
        ("The EU AI Act is expected to increase compliance costs for tech firms by 15%...", "Reuters", "98%", "2023-10-12"),
        ("European startups are pivoting to open-source models to bypass stringent...", "Bloomberg", "91%", "2023-10-10"),
        ("Investment in EU tech has slowed pending regulatory clarity...", "Financial Times", "87%", "2023-10-05")
    ],
    "nvidia earnings": [
        ("NVIDIA blows past Q3 expectations driven by unprecedented data center demand...", "CNBC", "99%", "2023-11-21"),
        ("Semiconductor supply chain tightens as NVIDIA secures additional TSMC capacity...", "WSJ", "94%", "2023-11-20"),
        ("Analysts upgrade NVDA price target, citing sustainable AI infrastructure spend...", "MarketWatch", "89%", "2023-11-18")
    ],
    "ev market": [
        ("Global EV sales growth decelerates as price wars squeeze legacy automaker margins...", "Bloomberg", "95%", "2024-01-15"),
        ("Chinese EV manufacturer BYD overtakes Tesla in quarterly deliveries...", "Reuters", "92%", "2024-01-02"),
        ("Battery raw material prices hit 3-year lows, providing tailwinds for EV startups...", "Financial Times", "88%", "2023-12-28")
    ],
    "rate cuts": [
        ("Federal Reserve signals three potential rate cuts in 2024 amid cooling inflation...", "WSJ", "97%", "2023-12-13"),
        ("Treasury yields slide as bond markets aggressively price in a dovish pivot...", "Bloomberg", "93%", "2023-12-14"),
        ("Real estate stocks rally on hopes of lower mortgage rates heading into spring...", "CNBC", "86%", "2023-12-15")
    ],
    "renewable energy": [
        ("Wind and solar capacity additions hit record highs despite supply chain bottlenecks...", "Reuters", "94%", "2023-11-05"),
        ("Major oil firms scale back green investments to focus on core dividend growth...", "Financial Times", "91%", "2023-11-02"),
        ("New government subsidies accelerate utility-scale battery storage deployments...", "WSJ", "85%", "2023-10-28")
    ],
    "inflation": [
        ("Core CPI rises unexpectedly, throwing cold water on early rate cut hopes...", "Bloomberg", "96%", "2024-02-13"),
        ("Consumer spending remains resilient despite lingering inflation pressures...", "Reuters", "90%", "2024-02-10"),
        ("Retailers warn of margin compression as input costs remain elevated...", "WSJ", "85%", "2024-02-05")
    ],
    "commercial real estate": [
        ("Regional banks increase provisions for commercial real estate loan defaults...", "Financial Times", "98%", "2024-01-30"),
        ("Office vacancy rates hit all-time highs in major metropolitan areas...", "WSJ", "92%", "2024-01-25"),
        ("Distressed commercial properties present new opportunities for private equity...", "Bloomberg", "88%", "2024-01-20")
    ],
    "semiconductor supply": [
        ("Global foundry capacity remains tight as AI chip demand outpaces production...", "Reuters", "95%", "2024-02-01"),
        ("New US export controls on advanced semiconductors reshape global supply chains...", "Financial Times", "93%", "2024-01-15"),
        ("Memory chip prices rebound following aggressive production cuts by major suppliers...", "CNBC", "87%", "2024-01-10")
    ],
    "default": [
        ("Global equities experience heightened volatility amid shifting macroeconomic indicators...", "Reuters", "82%", "2024-02-10"),
        ("Supply chain normalization leads to improved corporate margins across industrial sectors...", "Bloomberg", "78%", "2024-02-08"),
        ("Tech sector valuations stretch as investors continue to crowd into mega-cap names...", "WSJ", "75%", "2024-02-05")
    ]
}

# --- Suggested Queries Section ---
st.markdown("##### Quick Suggestions:")

# Larger pool of queries to randomly pick from
query_pool = [
    "AI regulations in Europe",
    "NVIDIA data center earnings",
    "Global EV market trends",
    "Federal Reserve rate cuts",
    "Renewable energy investments",
    "Inflation and consumer spending",
    "Commercial real estate risks",
    "Semiconductor supply chain"
]

# Randomly select 5 suggestions on every reload
if "random_suggestions" not in st.session_state:
    st.session_state.random_suggestions = random.sample(query_pool, 5)

# Custom CSS for Streamlit buttons to look like pills
st.markdown("""
<style>
div.stButton > button {
    border-radius: 20px;
    border: 1px solid var(--border-color);
    background-color: var(--card-bg);
    color: #ffffff !important;
    padding: 2px 15px;
    transition: all 0.3s ease;
}
div.stButton > button p {
    color: #ffffff !important;
}
div.stButton > button:hover {
    border: 1px solid var(--accent);
    color: #ffffff !important;
    background-color: var(--bg-secondary);
}
div.stButton > button:hover p {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(5)
for i, sug in enumerate(st.session_state.random_suggestions):
    if cols[i].button(sug, use_container_width=True, key=f"sug_{i}"):
        st.session_state.search_query = sug
        st.session_state.trigger_search = True
        # Randomize for next time
        st.session_state.random_suggestions = random.sample(query_pool, 5)
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- Main Search Bar ---
with st.container(border=True):
    # If a button was clicked, we pre-fill the text input with session state
    query = st.text_input(
        "Semantic Search Query:", 
        value=st.session_state.search_query,
        placeholder="e.g., How will AI regulations affect European tech companies?"
    )
    
    # Update state if user types manually
    if query != st.session_state.search_query:
        st.session_state.search_query = query
        st.session_state.trigger_search = True

st.divider()

# --- Search Execution ---
if query:
    if st.session_state.trigger_search:
        with st.spinner("Searching millions of vectors..."):
            time.sleep(0.5) # Simulate search time
        st.session_state.trigger_search = False
        
    # Match query to mock db
    q_lower = query.lower()
    results = mock_db["default"]
    for key in mock_db.keys():
        if key in q_lower:
            results = mock_db[key]
            break
            
    # --- KPIs ---
    k1, k2, k3 = st.columns(3)
    with k1:
        create_kpi_card("Documents Scanned", "2.4M", "Live Database", "normal")
    with k2:
        create_kpi_card("Vector Dimensions", "1,536", "OpenAI Ada-002", "inverse")
    with k3:
        retrieval_time = f"{random.uniform(0.1, 0.4):.2f}s"
        create_kpi_card("Retrieval Time", retrieval_time, "Ultra Low Latency", "normal")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Results HTML Feed ---
    st.markdown(f"#### Found {len(results)} highly relevant insights for: *'{query}'*")
    
    feed_html = "<div style='display: flex; flex-direction: column; gap: 15px; margin-top: 15px;'>"
    
    for snippet, source, score, date in results:
        # Determine color based on score
        score_val = int(score.replace('%', ''))
        if score_val >= 95:
            color, bg = "var(--color-bull)", "var(--bg-bull)"
        elif score_val >= 90:
            color, bg = "#4da6ff", "rgba(77, 166, 255, 0.1)"
        else:
            color, bg = "#ffbb33", "rgba(255, 187, 51, 0.1)"
            
        # Build HTML without multiline indentation to prevent Markdown code block parsing
        feed_html += f"<div class='headline-card' style='border-left: 4px solid {color}; padding: 20px; background: var(--card-bg);'>"
        feed_html += f"<div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;'>"
        feed_html += f"<div style='display: flex; align-items: center; gap: 10px;'>"
        feed_html += f"<span style='background: {bg}; color: {color}; padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 0.9rem; border: 1px solid {color};'>Match: {score}</span>"
        feed_html += f"<span style='color: var(--text-primary); font-size: 0.9rem; font-weight: 600;'>{source}</span>"
        feed_html += f"</div>"
        feed_html += f"<div style='color: var(--text-primary); font-size: 0.85rem; font-family: monospace;'>{date}</div>"
        feed_html += f"</div>"
        feed_html += f"<div style='font-size: 1.1rem; color: var(--text-bright); line-height: 1.5; font-weight: 500;'>\"{snippet}\"</div>"
        feed_html += f"</div>"
        
    feed_html += "</div>"
    st.markdown(feed_html, unsafe_allow_html=True)
