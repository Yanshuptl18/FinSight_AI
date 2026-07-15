import streamlit as st
from components.charts import render_plotly_chart
import pandas as pd
import numpy as np
import plotly.express as px
from components.utils import load_css, render_page_header
from components.charts import create_kpi_card

load_css()

render_page_header("Topic Intelligence Explorer")

# --- Mock Data Generation ---
dates = pd.date_range('2023-01-01', periods=30)
df = pd.DataFrame({
    'Date': np.tile(dates, 3),
    'Topic': ['Inflation']*30 + ['Supply Chain']*30 + ['AI Innovation']*30,
    'Volume': np.random.randint(10, 100, 90) + np.repeat([50, 20, 80], 30)
})

topics = pd.DataFrame({
    'Topic': ['AI Innovation', 'Inflation', 'Interest Rates', 'Supply Chain', 'ESG'],
    'Mentions': [2450, 1890, 1650, 1200, 980],
    'Momentum': [15.2, -2.5, 5.0, -10.1, 1.4] 
})

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Topic Filtering")
    selected_topic = st.selectbox("Focus Topic", ["All Topics"] + list(topics['Topic']))

st.divider()

# --- KPI Section ---
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    create_kpi_card("Total Monitored Topics", "35", "+3 new", "normal")
with kpi2:
    top_momentum = topics.loc[topics['Momentum'].idxmax()]
    create_kpi_card("Highest Momentum", top_momentum['Topic'], f"+{top_momentum['Momentum']}%", "normal")
with kpi3:
    create_kpi_card("Most Volatile", "Supply Chain", "-10.1%", "inverse")

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    with st.container(border=True):
        filtered_df = df if selected_topic == "All Topics" else df[df['Topic'] == selected_topic]
        fig = px.line(filtered_df, x='Date', y='Volume', color='Topic')
        fig.update_traces(
            line=dict(width=3, shape='spline'),
            mode='lines+markers',
            marker=dict(size=6, line=dict(width=2, color='var(--bg-primary)')),
            selected=dict(marker=dict(opacity=1)),
            unselected=dict(marker=dict(opacity=0.2))
        )
        fig.update_layout(
            title=dict(text="Topic Trends over Time", font=dict(size=16, color='#ffffff')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=60, l=50, r=20),
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor='var(--border-color)', title=""),
            hovermode="x unified",
            hoverlabel=dict(bgcolor="var(--bg-secondary)", bordercolor="rgba(255,255,255,0.2)")
        )
        render_plotly_chart(fig, width='stretch')

with col2:
    st.markdown("### Top Active Topics")
    
    feed_html = "<div style=\'padding: 10px; max-height: 500px; overflow-y: auto;\'>"
    feed_html += "<div style='display: flex; flex-direction: column; gap: 12px;'>"
    
    for _, row in topics.iterrows():
        mom = row['Momentum']
        if mom > 0:
            color, bg = "var(--color-bull)", "var(--bg-bull)"
            indicator = f"↑ +{mom}%"
        elif mom < 0:
            color, bg = "var(--color-bear)", "var(--bg-bear)"
            indicator = f"↓ {mom}%"
        else:
            color, bg = "var(--color-neutral)", "var(--bg-neutral)"
            indicator = f"- {mom}%"
            
        feed_html += f"<div class='headline-card' style='border-left: 4px solid {color}; padding: 12px;'>"
        feed_html += f"<div style='display: flex; justify-content: space-between; align-items: center;'>"
        feed_html += f"<div style='font-size: 1.05rem; font-weight: 600; color: var(--text-bright);'>{row['Topic']}</div>"
        feed_html += f"<span style='background: {bg}; color: {color}; padding: 4px 10px; border-radius: 20px; font-weight: 600; border: 1px solid {color}; font-size: 0.8rem;'>{indicator}</span>"
        feed_html += f"</div>"
        feed_html += f"<div style='margin-top: 8px; font-size: 0.85rem; color: var(--text-primary); font-weight: 500;'>Total Mentions: <span style='color: var(--accent);'>{row['Mentions']:,}</span></div>"
        feed_html += f"</div>"
        
    feed_html += "</div></div>"
    st.markdown(feed_html, unsafe_allow_html=True)
