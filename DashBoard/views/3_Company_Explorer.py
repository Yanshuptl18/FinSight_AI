import streamlit as st
from components.charts import render_plotly_chart
import pandas as pd
from data_loader.loader import load_news_data
from components.charts import plot_time_series, plot_donut_chart, create_kpi_card

from components.utils import load_css, render_page_header
load_css()

render_page_header("Company Intelligence Explorer")

news_df = load_news_data()
companies = sorted(news_df["Company"].unique())

# --- Search ---
with st.container(border=True):
    col_search, col_space = st.columns([1, 2])
    with col_search:
        selected_company = st.selectbox("Search Company", companies)

company_data = news_df[news_df["Company"] == selected_company]

st.divider()

# --- Company Overview ---

if company_data.empty:
    recommendation, rec_delta, rec_trend = "N/A", None, "off"
    risk_score, risk_delta, risk_trend = "N/A", None, "off"
    top_event = "N/A"
else:
    sentiment_counts = company_data['Sentiment'].value_counts()
    bullish = sentiment_counts.get('Bullish', 0)
    bearish = sentiment_counts.get('Bearish', 0)
    total = len(company_data)
    
    score = (bullish - bearish) / total if total > 0 else 0
    if score >= 0.3:
        recommendation, rec_delta, rec_trend = "Strong Buy", "Upgraded", "normal"
    elif score >= 0.1:
        recommendation, rec_delta, rec_trend = "Buy", "Positive", "normal"
    elif score <= -0.3:
        recommendation, rec_delta, rec_trend = "Strong Sell", "Downgraded", "inverse"
    elif score <= -0.1:
        recommendation, rec_delta, rec_trend = "Sell", "Negative", "inverse"
    else:
        recommendation, rec_delta, rec_trend = "Hold", "Stable", "off"

    risk = int((bearish / total) * 100) if total > 0 else 50
    risk_score = f"{risk}/100"
    
    if risk < 30:
        risk_delta, risk_trend = "-5", "inverse"
    elif risk > 60:
        risk_delta, risk_trend = "+8", "inverse"
    else:
        risk_delta, risk_trend = "+2", "inverse"
        
    event_mode = company_data["Event"].mode()
    top_event = str(event_mode[0]) if not event_mode.empty else "N/A"

col1, col2, col3, col4 = st.columns(4)
with col1:
    create_kpi_card("Recommendation", recommendation, rec_delta, rec_trend)
with col2:
    create_kpi_card("Risk Score", risk_score, risk_delta, risk_trend)
with col3:
    create_kpi_card("Total Articles", str(len(company_data)), None, "off")
with col4:
    create_kpi_card("Top Event", top_event, None, "off")

st.divider()

# --- Charts ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    with st.container(border=True):
        sentiment_counts = company_data['Sentiment'].value_counts()
        if not sentiment_counts.empty:
            fig_sentiment = plot_donut_chart(sentiment_counts.index, sentiment_counts.values, f"{selected_company} Sentiment")
            render_plotly_chart(fig_sentiment, width='stretch')
        else:
            st.info("No sentiment data available.")

with col_chart2:
    with st.container(border=True):
        timeline_df = company_data.groupby(company_data['Date'].dt.date).size().reset_index(name='News Volume')
        if not timeline_df.empty:
            fig_timeline = plot_time_series(timeline_df, 'Date', 'News Volume', f"{selected_company} Activity")
            render_plotly_chart(fig_timeline, width='stretch')
        else:
            st.info("No timeline data available.")

st.divider()

# --- Related News ---
st.markdown(f"### Latest News for {selected_company}")

if len(company_data) == 0:
    st.warning("No articles found.")
else:
    feed_html = "<div style='padding: 10px; max-height: 800px; overflow-y: auto;'>"
    feed_html += "<div style='display: flex; flex-direction: column; gap: 12px;'>"
    
    for _, row in company_data.head(50).iterrows():
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
            
        date_str = str(row['Date'])[:16] 
        
        feed_html += f"<div class='headline-card' style='border-left: {border_left};'>"
        feed_html += f"<div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;'>"
        feed_html += f"<div style='font-size: 1.05rem; font-weight: 600; color: var(--text-bright); line-height: 1.4;'>{row['Headline']}</div>"
        feed_html += f"<div style='font-size: 0.8rem; color: var(--text-primary); white-space: nowrap; margin-left: 16px; font-family: monospace;'>{date_str}</div>"
        feed_html += f"</div>"
        feed_html += f"<div style='display: flex; align-items: center; flex-wrap: wrap; gap: 10px; font-size: 0.85rem;'>"
        feed_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 20px; font-weight: 500; border: 1px solid var(--border-color);'>Publisher: {row['Publisher']}</span>"
        feed_html += f"<span style='background: {s_bg}; color: {s_color}; padding: 4px 10px; border-radius: 20px; font-weight: 600; border: 1px solid {s_color};'>{sentiment}</span>"
        feed_html += f"<span style='color: var(--accent); font-weight: 600; margin-left: auto; '>AI Confidence: {conf:.0%}</span>"
        feed_html += f"</div></div>"
        
    feed_html += "</div></div>"
    st.markdown(feed_html, unsafe_allow_html=True)
