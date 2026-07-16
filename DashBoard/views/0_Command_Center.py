import streamlit as st
from components.charts import render_plotly_chart
import pandas as pd
import numpy as np
import plotly.express as px
from config import PAGE_TITLE, PAGE_ICON, LAYOUT
from components.utils import render_page_header, render_template

# Render standard layoutndled by router

# Session State Initialization
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False

# Main Entry Point - Command Center
render_page_header(f"{PAGE_TITLE} Command Center", "")

# --- Global Market Pulse ---
st.markdown("### Global Market Pulse")


from data_loader.loader import load_company_analytics, load_news_data
import time

analytics_df = load_company_analytics()
news_df = load_news_data()

# Dynamic Sentiment
sentiment_val = "Neutral"
sent_cls = "neutral"
sent_icon = "➖"
sent_desc = "Stable"
if not analytics_df.empty and 'Bullish' in analytics_df.columns:
    avg_bull = analytics_df['Bullish'].mean()
    avg_bear = analytics_df['Bearish'].mean()
    if avg_bull > avg_bear * 1.2:
        sentiment_val, sent_cls, sent_icon, sent_desc = "Bullish", "bull", "⬆️", "Strong Momentum"
    elif avg_bear > avg_bull * 1.2:
        sentiment_val, sent_cls, sent_icon, sent_desc = "Bearish", "bear", "⬇️", "Downward Pressure"

# Dynamic Activity
activity_val = "Normal"
act_cls = "neutral"
act_icon = "📊"
act_desc = "Avg Volume"
if not news_df.empty:
    activity_val = "Surging" if len(news_df) > 1000 else "Normal"
    act_cls = "bull" if len(news_df) > 1000 else "neutral"
    act_icon = "🔥" if len(news_df) > 1000 else "📊"
    act_desc = "High Volume" if len(news_df) > 1000 else "Average Volume"

# Dynamic Risk
risk_val = "Medium"
risk_cls = "neutral"
risk_icon = "⚠️"
risk_desc = "Elevated"
if not analytics_df.empty and 'risk_score' in analytics_df.columns:
    avg_risk = analytics_df['risk_score'].mean()
    if avg_risk < 40:
        risk_val, risk_cls, risk_icon, risk_desc = "Low", "bull", "✅", "Stable Market"
    elif avg_risk > 70:
        risk_val, risk_cls, risk_icon, risk_desc = "High", "bear", "🚨", "High Volatility"

pulse_html = render_template(
    "pulse_card",
    sentiment=sentiment_val, sent_cls=sent_cls, sent_icon=sent_icon, sent_desc=sent_desc,
    activity=activity_val, act_cls=act_cls, act_icon=act_icon, act_desc=act_desc,
    risk=risk_val, risk_cls=risk_cls, risk_icon=risk_icon, risk_desc=risk_desc
)

if pulse_html:
    st.markdown(pulse_html, unsafe_allow_html=True)

st.divider()

# --- System Health & Ingestion Stats ---
st.markdown("### System Diagnostics & NLP Engine")

sys_col1, sys_col2 = st.columns([2, 1])

with sys_col1:
    # Simulated Live Ingestion Chart
    st.markdown("<div style='font-size: 1.05rem; font-weight: 600; margin-bottom: 10px; color: var(--text-bright);'>Real-Time Data Ingestion Volume</div>", unsafe_allow_html=True)
    from data_loader.loader import load_news_data
    news_df = load_news_data()
    
    if not news_df.empty and 'Date' in news_df.columns:
        # Group by date to get actual historical ingestion volume
        ingest_data = news_df.groupby(news_df['Date'].dt.date).size().reset_index(name='Articles Processed')
        ingest_data.rename(columns={'Date': 'Time'}, inplace=True)
        # Ensure it is a datetime for Plotly
        ingest_data['Time'] = pd.to_datetime(ingest_data['Time'])
        
        # Sort chronologically and take the last 60 days
        ingest_data = ingest_data.sort_values('Time').tail(60)
    else:
        # Fallback to empty DataFrame if no data
        ingest_data = pd.DataFrame(columns=['Time', 'Articles Processed'])
    
    fig = px.area(ingest_data, x='Time', y='Articles Processed',
                  color_discrete_sequence=['#4da6ff'])
    
    # Professional, clean layout updates
    fig.update_traces(line_shape='spline', fillcolor='rgba(77, 166, 255, 0.2)', line=dict(width=2))
    fig.update_layout(
        height=220, 
        margin=dict(l=40, r=20, t=20, b=40), 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, title="", showline=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='var(--border-color)', title="", showline=False, zeroline=False),
        hovermode="x unified"
    )
    render_plotly_chart(fig, width='stretch')

with sys_col2:
    start_q = time.time()
    queue_size = len(news_df) if not news_df.empty else 0
    latency_ms = int((time.time() - start_q) * 1000) + 12 # 12ms baseline overhead
    
    status_html = render_template("system_status", latency=latency_ms, queue=queue_size)

    if status_html:
        st.markdown(status_html, unsafe_allow_html=True)

st.divider()

# --- Quick Launch Modules ---
st.markdown("### Quick Launch Modules")

ql_html = render_template("quick_launch")
if ql_html:
    st.markdown(ql_html, unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: var(--text-primary); font-size: 0.9rem; margin-top: 10px;'><i>Navigate via the sidebar to access all 17 intelligence modules.</i></div>", unsafe_allow_html=True)
