import streamlit as st
from components.charts import render_plotly_chart
import pandas as pd
from components.utils import load_css, render_page_header
from components.charts import create_kpi_card, plot_bar_chart, plot_donut_chart

load_css()

render_page_header("Event Intelligence Explorer")

# --- Mock Data ---
events = pd.DataFrame({
    'Date': pd.date_range('today', periods=5).strftime('%Y-%m-%d'),
    'Event Type': ['Earnings Call', 'Fed Meeting', 'Product Launch', 'Regulatory Ruling', 'M&A Announcement'],
    'Primary Entity': ['NVIDIA', 'Federal Reserve', 'Apple', 'SEC', 'Microsoft'],
    'Expected Impact': ['High', 'Critical', 'Medium', 'High', 'High'],
    'Sentiment Forecast': ['Bullish', 'Bearish', 'Bullish', 'Neutral', 'Bullish']
})

hist_df = pd.DataFrame({
    'Event Category': ['Earnings', 'Macro', 'Geopolitical', 'M&A', 'Regulatory'],
    'Average Price Swing (%)': [5.2, 3.8, 4.1, 8.5, 2.1]
})

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Event Filtering")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        impact_filter = st.selectbox("Impact Level", ["All Levels", "Critical", "High", "Medium"])
    with col_f2:
        sentiment_filter = st.selectbox("Sentiment Forecast", ["All", "Bullish", "Bearish", "Neutral"])

st.divider()

# --- KPI Section ---
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    create_kpi_card("Critical Upcoming Events", "1", "This Week", "inverse")
with kpi2:
    create_kpi_card("Most Volatile Category", "M&A", "8.5% Swing", "normal")
with kpi3:
    create_kpi_card("Avg Market Swing", "4.74%", "+1.2%", "normal")

st.divider()

# Apply Filters
filtered_events = events.copy()
if impact_filter != "All Levels":
    filtered_events = filtered_events[filtered_events['Expected Impact'] == impact_filter]
if sentiment_filter != "All":
    filtered_events = filtered_events[filtered_events['Sentiment Forecast'] == sentiment_filter]

col1, col2 = st.columns([2, 1.2])

with col1:
    with st.container(border=True):
        st.markdown("### Historical Event Impact")
        fig_bar = plot_bar_chart(hist_df, 'Event Category', 'Average Price Swing (%)', "Avg Price Swing by Category")
        render_plotly_chart(fig_bar, width='stretch')
        
    with st.container(border=True):
        st.markdown("### Impact Distribution")
        impact_counts = events['Expected Impact'].value_counts()
        fig_donut = plot_donut_chart(impact_counts.index, impact_counts.values, "Expected Impact")
        render_plotly_chart(fig_donut, width='stretch')

with col2:
    st.markdown("### Upcoming Major Market Events")
    
    if filtered_events.empty:
        st.warning("No events match the selected filters.")
    else:
        feed_html = "<div style=\'padding: 10px; max-height: 800px; overflow-y: auto;\'>"
        feed_html += "<div style='display: flex; flex-direction: column; gap: 12px;'>"
        
        for _, row in filtered_events.iterrows():
            impact = row['Expected Impact']
            sentiment = row['Sentiment Forecast']
            
            # Impact Colors
            if impact == 'Critical':
                i_color, i_bg = "#ff4d4d", "rgba(255, 77, 77, 0.15)"
            elif impact == 'High':
                i_color, i_bg = "#ff9900", "rgba(255, 153, 0, 0.15)"
            else:
                i_color, i_bg = "var(--color-bull)", "var(--bg-bull)"
                
            # Sentiment Colors
            if sentiment == 'Bullish':
                s_color, s_bg = "var(--color-bull)", "var(--bg-bull)"
            elif sentiment == 'Bearish':
                s_color, s_bg = "var(--color-bear)", "var(--bg-bear)"
            else:
                s_color, s_bg = "var(--color-neutral)", "var(--bg-neutral)"
                
            feed_html += f"<div class='headline-card' style='border-left: 4px solid {i_color}; padding: 16px;'>"
            feed_html += f"<div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;'>"
            feed_html += f"<div>"
            feed_html += f"<div style='font-size: 1.1rem; font-weight: 700; color: var(--text-bright); margin-bottom: 4px;'>{row['Event Type']}</div>"
            feed_html += f"<div style='font-size: 0.9rem; color: var(--text-primary); font-weight: 500;'>Entity: <span style='color: var(--text-bright);'>{row['Primary Entity']}</span></div>"
            feed_html += f"</div>"
            feed_html += f"<div style='font-size: 0.85rem; color: var(--text-primary); font-family: monospace; font-weight: 600;'>{row['Date']}</div>"
            feed_html += f"</div>"
            
            feed_html += f"<div style='display: flex; align-items: center; flex-wrap: wrap; gap: 8px; font-size: 0.85rem;'>"
            feed_html += f"<span style='background: {i_bg}; color: {i_color}; padding: 4px 10px; border-radius: 20px; font-weight: 600; border: 1px solid {i_color};'>Impact: {impact}</span>"
            feed_html += f"<span style='background: {s_bg}; color: {s_color}; padding: 4px 10px; border-radius: 20px; font-weight: 600; border: 1px solid {s_color};'>Forecast: {sentiment}</span>"
            feed_html += f"</div></div>"
            
        feed_html += "</div></div>"
        st.markdown(feed_html, unsafe_allow_html=True)
