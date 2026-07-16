import streamlit as st
from components.charts import render_plotly_chart
import pandas as pd
import numpy as np
import plotly.express as px
from components.utils import load_css, render_page_header
from components.charts import create_kpi_card
import random

load_css()

render_page_header("Timeline Intelligence Explorer", "Filter and explore historical financial events chronologically. Insights update dynamically based on your selected time window.")

from data_loader.loader import load_timeline_data

@st.cache_data
def get_timeline_data():
    timeline_df = load_timeline_data()
    if timeline_df.empty:
        return pd.DataFrame(columns=['Date', 'Event Intensity', 'Category', 'Entity', 'Headline'])
        
    # Standardize column names
    rename_map = {
        'published_date': 'Date',
        'final_event': 'Category',
        'ticker': 'Entity',
        'headline': 'Headline'
    }
    
    # Rename matching columns
    timeline_df = timeline_df.rename(columns=lambda x: rename_map.get(x, x))
    
    # Ensure required columns exist
    if 'Date' in timeline_df.columns:
        timeline_df['Date'] = pd.to_datetime(timeline_df['Date']).dt.date
        
    # Map event importance to a 0-100 intensity scale
    if 'event_importance' in timeline_df.columns:
        timeline_df['Event Intensity'] = timeline_df['event_importance'] * 10
    
    # Fill defaults if missing
    if 'Category' not in timeline_df.columns:
        timeline_df['Category'] = "General"
    if 'Entity' not in timeline_df.columns:
        timeline_df['Entity'] = "Market"
    if 'Headline' not in timeline_df.columns:
        timeline_df['Headline'] = "No Headline"
    if 'Event Intensity' not in timeline_df.columns:
        timeline_df['Event Intensity'] = 50
        
    # Cap the total dataset size to avoid MessageSizeError when rendering the scatter plot
    # We take a random sample of 2000 events to show a representative spread of intensities over time
    if len(timeline_df) > 2000:
        timeline_df = timeline_df.sample(n=2000, random_state=42)
        
    return timeline_df

df = get_timeline_data()

# --- Interactive Filter ---
with st.container(border=True):
    st.markdown("#### Time Window Selection")
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    selected_dates = st.slider(
        "Slide to filter the Timeline and generate dynamic insights:", 
        min_value=min_date, 
        max_value=max_date, 
        value=(pd.to_datetime('2023-08-01').date(), pd.to_datetime('2023-12-31').date())
    )

st.divider()

# --- Filter Data ---
mask = (df['Date'] >= selected_dates[0]) & (df['Date'] <= selected_dates[1])
filtered_df = df.loc[mask]

# --- Dynamic KPIs ---
kpi1, kpi2, kpi3 = st.columns(3)

total_events = len(filtered_df)

if total_events > 0:
    most_active_cat = filtered_df['Category'].value_counts().index[0]
    avg_intensity = int(filtered_df['Event Intensity'].mean())
else:
    most_active_cat = "None"
    avg_intensity = 0

with kpi1:
    create_kpi_card("Events in Window", str(total_events), "Filtered", "normal")
with kpi2:
    create_kpi_card("Dominant Category", most_active_cat, "Most Frequent", "inverse")
with kpi3:
    create_kpi_card("Average Intensity", f"{avg_intensity}/100", "Market Impact", "normal")

st.divider()

# --- Layout: Chart and Insights ---
col_chart, col_insights = st.columns([1.8, 1.2])

with col_chart:
    with st.container(border=True):
        st.markdown(f"### Event Intensity Map")
        if total_events == 0:
            st.warning("No events found in this date range.")
        else:
            fig = px.scatter(
                filtered_df, 
                x='Date', 
                y='Event Intensity', 
                size='Event Intensity', 
                color='Category', 
                hover_name='Headline',
                
            )
            fig.update_traces(
                marker=dict(line=dict(width=1, color='var(--bg-primary)')),
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=30, b=60, l=50, r=20),
                height=500,
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor='var(--border-color)')
            )
            render_plotly_chart(fig, width='stretch')

with col_insights:
    st.markdown("### Dynamic Timeline Insights")
    
    if total_events == 0:
        st.info("Expand the date range to see insights.")
    else:
        feed_html = "<div style=\'padding: 10px; max-height: 550px; overflow-y: auto;\'>"
        feed_html += "<div style='display: flex; flex-direction: column; gap: 12px;'>"
        
        # Sort by most intense events in this window
        top_events = filtered_df.sort_values(by='Event Intensity', ascending=False).head(15)
        
        for _, row in top_events.iterrows():
            cat = row['Category']
            intensity = row['Event Intensity']
            
            # Color logic matching the chart
            if cat == 'Earnings':
                color, bg = "#ab63fa", "rgba(171, 99, 250, 0.15)"
            elif cat == 'M&A':
                color, bg = "#00cc96", "rgba(0, 204, 150, 0.15)"
            elif cat == 'Regulatory':
                color, bg = "#ef553b", "rgba(239, 85, 59, 0.15)"
            else: # Macro
                color, bg = "#636efa", "rgba(99, 110, 250, 0.15)"
                
            feed_html += f"<div class='headline-card' style='border-left: 4px solid {color}; padding: 16px;'>"
            feed_html += f"<div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;'>"
            feed_html += f"<div>"
            feed_html += f"<div style='font-size: 1.05rem; font-weight: 700; color: var(--text-bright); margin-bottom: 4px;'>{row['Headline']}</div>"
            feed_html += f"<div style='font-size: 0.85rem; color: var(--text-primary); font-weight: 500;'>Entity: <span style='color: var(--text-bright);'>{row['Entity']}</span></div>"
            feed_html += f"</div>"
            feed_html += f"<div style='font-size: 0.8rem; color: var(--text-primary); font-family: monospace; font-weight: 600; white-space: nowrap; margin-left: 10px;'>{row['Date']}</div>"
            feed_html += f"</div>"
            
            feed_html += f"<div style='display: flex; align-items: center; gap: 12px; font-size: 0.85rem;'>"
            feed_html += f"<span style='background: {bg}; color: {color}; padding: 4px 10px; border-radius: 20px; font-weight: 600; border: 1px solid {color};'>{cat}</span>"
            feed_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 6px; font-weight: 500; border: 1px solid var(--border-color);'>Intensity: <span style='color:#ff9900;'>{intensity}</span>/100</span>"
            feed_html += f"</div></div>"
            
        feed_html += "</div></div>"
        st.markdown(feed_html, unsafe_allow_html=True)
