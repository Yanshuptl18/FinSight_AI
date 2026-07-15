import streamlit as st
import pandas as pd
from data_loader.loader import load_mock_news_data
from components.utils import load_css, render_page_header, render_template

load_css()

render_page_header(" News Intelligence Explorer", "Advanced filtering and semantic search for market news.")

news_df = load_mock_news_data()

from components.charts import create_kpi_card

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Advanced Search & Filters")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_company = st.selectbox("Company", ["All"] + list(news_df["Company"].unique()))
    with col2:
        selected_sector = st.selectbox("Sector", ["All"] + list(news_df["Sector"].unique()))
    with col3:
        selected_sentiment = st.selectbox("Sentiment", ["All", "Bullish", "Bearish", "Neutral", "Mixed"])
    with col4:
        min_confidence = st.slider("Min AI Confidence", 0.0, 1.0, 0.7)

# --- Apply Filters ---
filtered_df = news_df.copy()
if selected_company != "All":
    filtered_df = filtered_df[filtered_df["Company"] == selected_company]
if selected_sector != "All":
    filtered_df = filtered_df[filtered_df["Sector"] == selected_sector]
if selected_sentiment != "All":
    filtered_df = filtered_df[filtered_df["Sentiment"] == selected_sentiment]
filtered_df = filtered_df[filtered_df["Confidence"] >= min_confidence]

st.divider()

# --- KPI Summary ---
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
with kpi_col1:
    create_kpi_card("Matching Articles", f"{len(filtered_df):,}", None, "off")
with kpi_col2:
    avg_conf = filtered_df['Confidence'].mean() if len(filtered_df) > 0 else 0
    create_kpi_card("Average Confidence", f"{avg_conf:.1%}", None, "off")
with kpi_col3:
    top_company = filtered_df['Company'].mode()[0] if len(filtered_df) > 0 else "N/A"
    create_kpi_card("Top Mentioned", top_company, None, "off")

st.markdown("### Search Results")

if len(filtered_df) == 0:
    st.warning("No articles match the selected filters.")
else:
    # --- HTML Feed (Using Templates) ---
    cards_html = ""
    for _, row in filtered_df.head(50).iterrows(): # Show up to 50 results
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
        
        entities_html = f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 20px; font-weight: 500; border: 1px solid var(--border-color);'>Company: {row['Company']}</span>"
        entities_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 20px; font-weight: 500; border: 1px solid var(--border-color);'>Sector: {row['Sector']}</span>"
        
        card = render_template(
            "news_card",
            border_left=border_left,
            headline=row['Headline'],
            date_str=date_str,
            entities_html=entities_html,
            s_bg=s_bg,
            s_color=s_color,
            sentiment=sentiment,
            conf=f"{conf:.0%}"
        )
        cards_html += card + "\n"
        
    feed_html = render_template("feed_container", max_height="800px", cards_html=cards_html)
    if feed_html:
        st.markdown(feed_html, unsafe_allow_html=True)
