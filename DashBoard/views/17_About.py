import streamlit as st
from components.utils import load_css, render_page_header

load_css()

render_page_header("About FinSight AI")

st.markdown("""
<style>
@keyframes slideUpFade {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.about-intro {
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--text-primary);
    margin-bottom: 30px;
    animation: slideUpFade 0.8s ease-out forwards;
}

.guide-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.guide-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 25px;
    animation: slideUpFade 0.8s ease-out forwards;
    opacity: 0;
    transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
    position: relative;
    overflow: hidden;
}

.guide-card:nth-child(1) { animation-delay: 0.2s; }
.guide-card:nth-child(2) { animation-delay: 0.4s; }
.guide-card:nth-child(3) { animation-delay: 0.6s; }
.guide-card:nth-child(4) { animation-delay: 0.8s; }

.guide-card:hover {
    transform: translateX(10px) translateY(-2px);
    box-shadow: -4px 8px 25px rgba(0,0,0,0.15);
    border-color: var(--accent);
}

.guide-title {
    color: var(--text-bright);
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 8px;
    border-bottom: 2px solid var(--accent);
    display: inline-block;
    padding-bottom: 4px;
}

.guide-text {
    color: var(--text-primary);
    font-size: 1rem;
    line-height: 1.5;
}

.version-footer {
    margin-top: 40px;
    text-align: center;
    color: var(--text-primary);
    font-size: 0.9rem;
    opacity: 0.7;
    animation: slideUpFade 1s ease-out 1s forwards;
    opacity: 0;
}
</style>

<div class="about-intro">
<strong style="color: var(--text-bright); font-size: 1.3rem;">The Premium Financial Intelligence Platform</strong><br><br>
FinSight AI is a next-generation dashboard designed for hedge funds, equity researchers, and corporate strategists. 
It aggregates real-time news, extracts entities and topics using advanced NLP, and provides actionable insights.
<br><br>
<strong style="color: var(--text-bright); font-size: 1.2rem;">How to Use FinSight AI (A Quick Guide):</strong>
</div>

<div class="guide-container">
<div class="guide-card">
<div class="guide-title">Entity Extraction & Intelligence</div>
<div class="guide-text">
<strong>What it is:</strong> We automatically read through massive walls of text to find important companies, people, and locations.<br>
<strong>How to use it:</strong> Go to the <em>Company Explorer</em> or <em>Sector Intelligence</em> pages to instantly see who is making headlines and dominating the market right now.
</div>
</div>

<div class="guide-card">
<div class="guide-title">Sentiment Analysis</div>
<div class="guide-text">
<strong>What it is:</strong> We analyze the hidden emotions inside news articles to tell you if the market is feeling optimistic (Bullish) or pessimistic (Bearish).<br>
<strong>How to use it:</strong> Check the <em>News Explorer</em> to quickly gauge market reactions without having to read a single article yourself!
</div>
</div>

<div class="guide-card">
<div class="guide-title">Knowledge Graphs</div>
<div class="guide-text">
<strong>What it is:</strong> A visual web that maps out complex supply chains and competitor networks.<br>
<strong>How to use it:</strong> Open the <em>Knowledge Graph</em> or <em>Company Network</em> page. You can drag, zoom, and interact with the bubbles to discover secret connections between different organizations!
</div>
</div>

<div class="guide-card">
<div class="guide-title">Semantic Search</div>
<div class="guide-text">
<strong>What it is:</strong> A highly advanced search engine that understands <em>meaning</em>, not just keywords.<br>
<strong>How to use it:</strong> Go to <em>Semantic Search</em> and ask a question in plain English (like "Which companies are investing in AI?"). The system will find the exact insights you need.
</div>
</div>
</div>

<div class="version-footer">
<strong>Version: 1.0.0-beta</strong><br>
Developed by FinSight AI Labs.
</div>
""", unsafe_allow_html=True)
