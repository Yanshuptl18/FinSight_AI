import streamlit as st
from components.charts import render_plotly_chart
import pandas as pd
from data_loader.loader import load_mock_news_data, get_dashboard_metrics, load_mock_sector_data
from components.charts import create_kpi_card, plot_donut_chart, plot_bar_chart, plot_time_series

from components.utils import load_css, render_page_header
load_css()

render_page_header(" Executive Dashboard", "High-level overview of market intelligence, sentiment, and trending entities.")

# Load Data
with st.spinner("Loading intelligence..."):
    news_df = load_mock_news_data()
    metrics = get_dashboard_metrics()
    sector_df = load_mock_sector_data()

# --- KPI Section ---
st.markdown("### Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
with col1:
    create_kpi_card("Total News Analyzed", f"{metrics['Total News']:,}", "+124 today", "normal")
    create_kpi_card("Events Tracked", f"{metrics['Events']:,}", "+5 this week", "normal")
with col2:
    create_kpi_card("Companies Monitored", f"{metrics['Companies']:,}", "+2", "normal")
    create_kpi_card("Sectors Covered", f"{metrics['Sectors']:,}", None, "off")
with col3:
    create_kpi_card("Publishers", f"{metrics['Publishers']:,}", None, "off")
    create_kpi_card("Topics Extracted", f"{metrics['Topics']:,}", "+12", "normal")
with col4:
    create_kpi_card("Average AI Confidence", metrics['Average Confidence'], "+0.5%", "normal")
    create_kpi_card("Latest Ingestion", metrics['Latest Date'], None, "off")

st.divider()

# --- AI Insight Section ---
st.markdown("### FinSight AI Insight")

ai_html = """<style>.ai-insight-box { background: var(--card-bg); border: 1px solid var(--accent); border-radius: 12px; padding: 24px; box-shadow: 0 4px 20px rgba(77, 166, 255, 0.1); position: relative; overflow: hidden; } .ai-insight-box::before { content: ""; position: absolute; top: 0; left: -100%; width: 100%; height: 3px; background: linear-gradient(90deg, transparent, #4da6ff, transparent); animation: scanline 3s linear infinite; } @keyframes scanline { 0% { left: -100%; } 100% { left: 100%; } } .ai-header { font-size: 1.1rem; font-weight: 600; color: var(--accent); margin-bottom: 15px; display: flex; align-items: center; } .ai-pulse { height: 10px; width: 10px; background-color: var(--accent); border-radius: 50%; margin-right: 12px; box-shadow: 0 0 10px #4da6ff; animation: pulseAI 2s infinite; } @keyframes pulseAI { 0% { transform: scale(0.95); opacity: 0.8; box-shadow: 0 0 10px #4da6ff; } 50% { transform: scale(1.3); opacity: 1; box-shadow: 0 0 20px #4da6ff; } 100% { transform: scale(0.95); opacity: 0.8; box-shadow: 0 0 10px #4da6ff; } } .ai-list { list-style: none; padding-left: 0; margin: 0; } .ai-list li { margin-bottom: 12px; font-size: 0.95rem; color: var(--text-primary); padding-left: 20px; position: relative; line-height: 1.6; } .ai-list li::before { content: "►"; position: absolute; left: 0; color: var(--accent); font-size: 0.8rem; top: 3px; } .highlight-blue { color: var(--accent); font-weight: 600; } .highlight-green { color: var(--color-bull); font-weight: 600; } .highlight-red { color: #ff6b6b; font-weight: 600; }</style><div class="ai-insight-box"><div class="ai-header"><div class="ai-pulse"></div> FinSight AI Synthesis: Today's Market Summary</div><ul class="ai-list"><li><span class="highlight-blue">Technology</span> generated the highest news activity, primarily driven by <span class="highlight-blue">AI</span> and <span class="highlight-blue">NVIDIA</span>.</li><li><span class="highlight-blue">Financial Services</span> maintained strong confidence despite concerns over <span class="highlight-red">Interest Rates</span>.</li><li><span class="highlight-blue">Healthcare</span> became <span class="highlight-red">less active</span> compared to last week.</li><li><span class="highlight-blue">Apple</span> is currently showing <span class="highlight-green">bullish momentum</span> across multiple publishers.</li></ul></div>"""
st.markdown(ai_html, unsafe_allow_html=True)

st.divider()

# --- Charts Section ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    with st.container(border=True):
        # Sentiment Distribution
        sentiment_counts = news_df['Sentiment'].value_counts()
        fig_sentiment = plot_donut_chart(
            sentiment_counts.index, 
            sentiment_counts.values, 
            "Market Mood (Sentiment Distribution)"
        )
        render_plotly_chart(fig_sentiment, width='stretch')
    
    with st.container(border=True):
        # Sector Distribution
        sector_counts = news_df['Sector'].value_counts().reset_index()
        sector_counts.columns = ['Sector', 'Count']
        fig_sector = plot_bar_chart(sector_counts, 'Sector', 'Count', "News by Sector")
        render_plotly_chart(fig_sector, width='stretch')

with col_chart2:
    with st.container(border=True):
        # Timeline
        timeline_df = news_df.groupby(news_df['Date'].dt.date).size().reset_index(name='News Volume')
        fig_timeline = plot_time_series(timeline_df, 'Date', 'News Volume', "News Timeline (Last 30 Days)")
        render_plotly_chart(fig_timeline, width='stretch')
    
    with st.container(border=True):
        # Top Companies
        company_counts = news_df['Company'].value_counts().head(5).reset_index()
        company_counts.columns = ['Company', 'Count']
        fig_company = plot_bar_chart(company_counts, 'Count', 'Company', "Top Trending Companies")
        fig_company.update_layout(yaxis={'categoryorder':'total ascending'})
        render_plotly_chart(fig_company, width='stretch')

st.divider()

# --- Recent Headlines ---
# --- Recent Headlines ---
st.markdown("### Latest High-Confidence Headlines")



headlines = news_df[['Date', 'Headline', 'Company', 'Sentiment', 'Confidence']].head(10)

feed_html = "<div style=\'padding: 10px; max-height: 600px; overflow-y: auto;\'>"
feed_html += "<div style='display: flex; flex-direction: column; gap: 12px;'>"

for _, row in headlines.iterrows():
    sentiment = row['Sentiment']
    conf = float(row['Confidence']) if pd.notnull(row['Confidence']) else 0.85
    
    if sentiment == 'Bullish':
        s_color, s_bg = "var(--color-bull)", "var(--bg-bull)"
        border_left = f"4px solid {s_color}"
    elif sentiment == 'Bearish':
        s_color, s_bg = "var(--color-bear)", "var(--bg-bear)"
        border_left = f"4px solid {s_color}"
    else:
        s_color, s_bg = "var(--color-neutral)", "var(--bg-neutral)"
        border_left = f"4px solid {s_color}"
        
    date_str = str(row['Date'])[:16] # Truncate seconds if present
    
    feed_html += f"<div class='headline-card' style='border-left: {border_left};'>"
    feed_html += f"<div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;'>"
    feed_html += f"<div style='font-size: 1.05rem; font-weight: 600; color: var(--text-bright); line-height: 1.4;'>{row['Headline']}</div>"
    feed_html += f"<div style='font-size: 0.8rem; color: var(--text-primary); white-space: nowrap; margin-left: 16px; font-family: monospace;'>{date_str}</div>"
    feed_html += f"</div>"
    feed_html += f"<div style='display: flex; align-items: center; flex-wrap: wrap; gap: 10px; font-size: 0.85rem;'>"
    feed_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 20px; font-weight: 500; border: 1px solid var(--border-color);'>Company: {row['Company']}</span>"
    feed_html += f"<span style='background: {s_bg}; color: {s_color}; padding: 4px 10px; border-radius: 20px; font-weight: 600; border: 1px solid {s_color};'>{sentiment}</span>"
    feed_html += f"<span style='color: var(--accent); font-weight: 600; margin-left: auto; '>AI Confidence: {conf:.0%}</span>"
    feed_html += f"</div></div>"
feed_html += "</div></div>"

st.markdown(feed_html, unsafe_allow_html=True)
