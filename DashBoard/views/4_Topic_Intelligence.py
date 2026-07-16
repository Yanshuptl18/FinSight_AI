import streamlit as st
from components.charts import render_plotly_chart
import pandas as pd
import numpy as np
import plotly.express as px
from components.utils import load_css, render_page_header
from components.charts import create_kpi_card

load_css()

render_page_header("Topic Intelligence Explorer")

import os
from data_loader.loader import get_real_data, DATA_PATH

get_real_data()

try:
    timeline_df = pd.read_parquet(os.path.join(DATA_PATH, "topic_timeline.parquet"))
    df = timeline_df.rename(columns={'month': 'Date', 'topic_name': 'Topic', 'articles': 'Volume'})
    df['Date'] = pd.to_datetime(df['Date'])
    
    profiles_df = pd.read_parquet(os.path.join(DATA_PATH, "topic_profiles.parquet"))
    growth_df = pd.read_parquet(os.path.join(DATA_PATH, "topic_growth.parquet"))
    
    profiles = pd.merge(profiles_df, growth_df[['topic_id', 'avg_growth']], on='topic_id', how='left')
    
    topics = profiles.rename(columns={
        'topic_name': 'Topic', 
        'articles': 'Mentions', 
        'avg_growth': 'Momentum',
        'keywords': 'Keywords'
    })
    
    # Clean topic names by stripping trailing digits (e.g. "Market Movement 1" -> "Market Movement")
    topics['Topic'] = topics['Topic'].str.replace(r' \d+$', '', regex=True)
    df['Topic'] = df['Topic'].str.replace(r' \d+$', '', regex=True)
    
    # Aggregate duplicate topics after cleaning
    topics = topics.groupby('Topic').agg({
        'Mentions': 'sum',
        'Momentum': 'mean',
        'Keywords': 'first'
    }).reset_index()
    
    df = df.groupby(['Date', 'Topic'])['Volume'].sum().reset_index()
    
    topics['Momentum'] = topics['Momentum'].fillna(0.0).round(1)
    
    # Required for rendering later
    topic_df = topics.rename(columns={'Topic': 'topic_name', 'Keywords': 'keywords'})
except Exception as e:
    st.error(f"Error loading topic intelligence data: {e}")
    df = pd.DataFrame(columns=['Date', 'Topic', 'Volume'])
    topics = pd.DataFrame(columns=['Topic', 'Mentions', 'Momentum', 'Keywords'])
    topic_df = pd.DataFrame()

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Topic Filtering")
    selected_topic = st.selectbox("Focus Topic", ["All Topics"] + list(topics['Topic']))

st.divider()

# --- KPI Section ---
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    create_kpi_card("Total Monitored Topics", str(len(topics)) if not topics.empty else "0", "Discovered", "normal")
with kpi2:
    if not topics.empty:
        top_momentum = topics.loc[topics['Momentum'].idxmax()]
        create_kpi_card("Highest Momentum", top_momentum['Topic'], f"+{top_momentum['Momentum']}%", "normal")
    else:
        create_kpi_card("Highest Momentum", "N/A", "+0%", "normal")
with kpi3:
    if not topics.empty:
        lowest_momentum = topics.loc[topics['Momentum'].idxmin()]
        create_kpi_card("Most Volatile", lowest_momentum['Topic'], f"{lowest_momentum['Momentum']}%", "inverse")
    else:
        create_kpi_card("Most Volatile", "N/A", "0%", "inverse")

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    with st.container(border=True):
        if selected_topic == "All Topics":
            # For "All Topics", only show top 10 by volume to avoid messy chart
            top_10 = topics['Topic'].head(10).tolist()
            filtered_df = df[df['Topic'].isin(top_10)]
        else:
            filtered_df = df[df['Topic'] == selected_topic]
            
        fig = px.line(filtered_df, x='Date', y='Volume', color='Topic')
        fig.update_traces(
            line=dict(width=3, shape='linear'),
            mode='lines+markers',
            marker=dict(size=6, line=dict(width=2, color='var(--bg-primary)')),
            selected=dict(marker=dict(opacity=1)),
            unselected=dict(marker=dict(opacity=0.2))
        )
        fig.update_layout(
            title=dict(text="Topic Trends over Time (Top 10)", font=dict(size=16, color='#ffffff')),
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
            
        # Try to get keywords if available
        keywords_html = ""
        if not topic_df.empty and 'topic_name' in topic_df.columns and 'keywords' in topic_df.columns:
            topic_match = topic_df[topic_df['topic_name'] == row['Topic']]
            if not topic_match.empty:
                kw = str(topic_match.iloc[0]['keywords'])
                keywords_html = f"<div style='margin-top: 4px; font-size: 0.75rem; color: #a0a0a0; font-style: italic;'>{kw[:60]}...</div>"
            
        feed_html += f"<div class='headline-card' style='border-left: 4px solid {color}; padding: 12px;'>"
        feed_html += f"<div style='display: flex; justify-content: space-between; align-items: center;'>"
        feed_html += f"<div style='font-size: 1.05rem; font-weight: 600; color: var(--text-bright);'>{row['Topic']}</div>"
        feed_html += f"<span style='background: {bg}; color: {color}; padding: 4px 10px; border-radius: 20px; font-weight: 600; border: 1px solid {color}; font-size: 0.8rem;'>{indicator}</span>"
        feed_html += f"</div>"
        feed_html += keywords_html
        feed_html += f"<div style='margin-top: 8px; font-size: 0.85rem; color: var(--text-primary); font-weight: 500;'>Total Mentions: <span style='color: var(--accent);'>{row['Mentions']:,}</span></div>"
        feed_html += f"</div>"
        
    feed_html += "</div></div>"
    st.markdown(feed_html, unsafe_allow_html=True)



