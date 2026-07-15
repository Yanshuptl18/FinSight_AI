import streamlit as st
from components.charts import render_plotly_chart
import pandas as pd
import plotly.graph_objects as go
from components.utils import load_css, render_page_header, THEMES
from components.charts import create_kpi_card

load_css()

render_page_header("Event Propagation Explorer", "Visualize how specific events cascade across sectors, industries, and companies.")

# --- Event Database ---
event_data = {
    "NVIDIA Earnings Surprise": {
        "kpis": {"total": "6 Entities", "primary_sector": "Technology", "confidence": "92%"},
        "nodes": ["NVIDIA Earnings", "Technology Sector", "Semiconductors", "Consumer Electronics", "Automotive", "S&P 500"],
        "node_colors": ["#00e676", "#4da6ff", "#4da6ff", "#ff9900", "#ff5252", "#808080"],
        "links": {"source": [0, 0, 1, 1, 2, 2], "target": [1, 5, 2, 3, 4, 5], "value": [10, 5, 6, 4, 2, 3]}
    },
    "Fed Rate Hike (+0.25%)": {
        "kpis": {"total": "7 Entities", "primary_sector": "Financials", "confidence": "98%"},
        "nodes": ["Fed Rate Hike", "Financials", "Real Estate", "Tech Sector", "Regional Banks", "Mortgage Lenders", "S&P 500"],
        "node_colors": ["#ff5252", "#4da6ff", "#ff9900", "#ff5252", "#ff5252", "#ff9900", "#808080"],
        "links": {"source": [0, 0, 0, 1, 2, 3], "target": [1, 2, 3, 4, 5, 6], "value": [8, 6, 4, 5, 4, 3]}
    },
    "Suez Canal Blockage": {
        "kpis": {"total": "5 Entities", "primary_sector": "Logistics", "confidence": "85%"},
        "nodes": ["Canal Blockage", "Global Shipping", "Retail Supply Chain", "Oil & Gas", "European Markets"],
        "node_colors": ["#ff9900", "#4da6ff", "#ff5252", "#00e676", "#808080"],
        "links": {"source": [0, 0, 1, 1], "target": [1, 3, 2, 4], "value": [10, 5, 7, 4]}
    },
    "Apple Vision Pro Launch": {
        "kpis": {"total": "6 Entities", "primary_sector": "Consumer Tech", "confidence": "89%"},
        "nodes": ["Vision Pro", "Consumer Electronics", "AR/VR Hardware", "App Developers", "Component Suppliers", "Gaming Sector"],
        "node_colors": ["#00e676", "#4da6ff", "#4da6ff", "#00e676", "#ff9900", "#00e676"],
        "links": {"source": [0, 0, 1, 1, 2], "target": [1, 2, 3, 4, 5], "value": [9, 7, 5, 4, 3]}
    },
    "OPEC Production Cut": {
        "kpis": {"total": "5 Entities", "primary_sector": "Energy", "confidence": "95%"},
        "nodes": ["OPEC Cut", "Energy Sector", "Airlines", "Logistics", "Consumer Inflation"],
        "node_colors": ["#ff4d4d", "#00e676", "#ff4d4d", "#ff9900", "#ff4d4d"],
        "links": {"source": [0, 0, 1, 1], "target": [1, 2, 3, 4], "value": [10, 6, 5, 4]}
    }
}

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Event Selection")
    selected_event = st.selectbox("Select Event Origin to trace its propagation path:", list(event_data.keys()))

st.divider()

# Get data for selected event
data = event_data[selected_event]

# --- KPI Section ---
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    create_kpi_card("Impacted Entities", data['kpis']['total'], "Across Network", "normal")
with kpi2:
    create_kpi_card("Primary Sector", data['kpis']['primary_sector'], "Highest Exposure", "inverse")
with kpi3:
    create_kpi_card("Cascade Confidence", data['kpis']['confidence'], "AI Predicted", "normal")

st.divider()

# --- Propagation Chart ---
with st.container(border=True):
    st.markdown(f"### Propagation Ripple Effect: {selected_event}")
    
    # Get current theme for dynamic chart colors
    _active_theme = THEMES.get(st.session_state.get('active_theme', 'Dark Cyan'), THEMES['Dark Cyan'])
    _is_light = st.session_state.get('active_theme', 'Dark Cyan') in ('Light Blue', 'Cool Gray')
    _link_color = "rgba(17, 45, 78, 0.25)" if _is_light else "rgba(255, 255, 255, 0.15)"
    
    # Sankey diagram for propagation
    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 20,
          thickness = 25,
          line = dict(color = _active_theme['--bg-primary'], width = 1.5),
          label = data['nodes'],
          color = data['node_colors']
        ),
        link = dict(
          source = data['links']['source'],
          target = data['links']['target'],
          value = data['links']['value'],
          color = _link_color
        )
    )])
    
    fig.update_layout(
        font_size=12,
        font_color=_active_theme['--text-primary'],
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=30, b=60, l=50, r=20),
        height=500
    )
    render_plotly_chart(fig, width='stretch')
