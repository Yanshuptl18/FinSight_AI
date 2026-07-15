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

pulse_html = render_template("pulse_card")
if pulse_html:
    st.markdown(pulse_html, unsafe_allow_html=True)

st.divider()

# --- System Health & Ingestion Stats ---
st.markdown("### System Diagnostics & NLP Engine")

sys_col1, sys_col2 = st.columns([2, 1])

with sys_col1:
    # Simulated Live Ingestion Chart
    st.markdown("<div style='font-size: 1.05rem; font-weight: 600; margin-bottom: 10px; color: var(--text-bright);'>Real-Time Data Ingestion Volume</div>", unsafe_allow_html=True)
    time_index = pd.date_range(end=pd.Timestamp.now(), periods=60, freq='min')
    
    # Generate smoother data
    np.random.seed(42) # For stability
    base_trend = np.sin(np.linspace(0, 10, 60)) * 20 + 50
    noise = np.random.normal(0, 5, 60)
    ingest_data = pd.DataFrame({
        'Time': time_index,
        'Articles Processed': (base_trend + noise).clip(min=10).astype(int)
    })
    
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
    status_html = render_template("system_status")
    if status_html:
        st.markdown(status_html, unsafe_allow_html=True)

st.divider()

# --- Quick Launch Modules ---
st.markdown("### Quick Launch Modules")

ql_html = render_template("quick_launch")
if ql_html:
    st.markdown(ql_html, unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: var(--text-primary); font-size: 0.9rem; margin-top: 10px;'><i>Navigate via the sidebar to access all 17 intelligence modules.</i></div>", unsafe_allow_html=True)
