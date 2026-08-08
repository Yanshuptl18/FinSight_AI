import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader.loader import load_news_data
from components.utils import load_css, render_page_header, render_template, clean_html
from components.charts import create_kpi_card, plot_donut_chart, plot_bar_chart, plot_time_series, render_plotly_chart

load_css()

render_page_header("News Intelligence Explorer", "Search headlines, filter by publisher, sentiment, and date range across 3.2M+ financial news records.")

news_df = load_news_data()

if news_df.empty:
    st.warning("News data is currently loading or unavailable.")
    st.stop()

# --- Search & Filter Section ---
with st.container(border=True):
    st.markdown("#### Search & Filter Market News")

    
    # Row 1: Search Query Input
    search_query = st.text_input("Keyword / Headline Search", placeholder="e.g. Earnings, Acquisition, Semiconductor, Dividend, Federal Reserve")
    
    # Row 2: Selectboxes
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        comp_list = ["All Companies"] + sorted(list(news_df["Company"].dropna().unique()))
        selected_company = st.selectbox("Company", comp_list)
    with col2:
        sec_list = ["All Sectors"] + sorted(list(news_df["Sector"].dropna().unique()))
        selected_sector = st.selectbox("Sector", sec_list)
    with col3:
        sent_list = ["All Sentiments"] + sorted(list(news_df["Sentiment"].dropna().unique()))
        selected_sentiment = st.selectbox("Sentiment", sent_list)
    with col4:
        pub_list = ["All Publishers"] + sorted(list(news_df["Publisher"].dropna().unique()))
        selected_publisher = st.selectbox("Publisher", pub_list)
    with col5:
        min_confidence = st.slider("Min AI Confidence", 0.0, 1.0, 0.70, 0.05)

# --- Apply Filters ---
filtered_df = news_df.copy()

if search_query:
    filtered_df = filtered_df[filtered_df["Headline"].str.contains(search_query, case=False, na=False)]
if selected_company != "All Companies":
    filtered_df = filtered_df[filtered_df["Company"] == selected_company]
if selected_sector != "All Sectors":
    filtered_df = filtered_df[filtered_df["Sector"] == selected_sector]
if selected_sentiment != "All Sentiments":
    filtered_df = filtered_df[filtered_df["Sentiment"] == selected_sentiment]
if selected_publisher != "All Publishers":
    filtered_df = filtered_df[filtered_df["Publisher"] == selected_publisher]

if 'Confidence' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Confidence"] >= min_confidence]

st.divider()

# --- 4 Structured KPI Cards ---
kpi1, kpi2, kpi3, k4 = st.columns(4)

with kpi1:
    create_kpi_card("Matching Articles", f"{len(filtered_df):,}", "Filtered News Items", "normal")

with kpi2:
    avg_conf = filtered_df['Confidence'].mean() if len(filtered_df) > 0 and 'Confidence' in filtered_df.columns else 0.85
    create_kpi_card("Average AI Confidence", f"{avg_conf:.1%}", "High Precision AI", "normal")

with kpi3:
    if len(filtered_df) > 0 and 'Company' in filtered_df.columns:
        top_comp = filtered_df['Company'].mode()
        top_comp_name = str(top_comp[0]) if not top_comp.empty else "N/A"
        comp_count = len(filtered_df[filtered_df['Company'] == top_comp_name])
        create_kpi_card("Top Mentioned Org", top_comp_name, f"{comp_count:,} Articles", "normal")
    else:
        create_kpi_card("Top Mentioned Org", "N/A", "0 Articles", "normal")

with k4:
    if len(filtered_df) > 0 and 'Publisher' in filtered_df.columns:
        top_pub = filtered_df['Publisher'].mode()
        top_pub_name = str(top_pub[0]) if not top_pub.empty else "N/A"
        pub_count = len(filtered_df[filtered_df['Publisher'] == top_pub_name])
        create_kpi_card("Leading Publisher", top_pub_name, f"{pub_count:,} Articles", "normal")
    else:
        create_kpi_card("Leading Publisher", "N/A", "0 Articles", "normal")

st.divider()

# --- Multi-Tab Analytics & Feed ---
tab1, tab2, tab3 = st.tabs([
    "Live News Intelligence Feed",
    "Sentiment Mood & Publisher Share",
    "Temporal Activity Trajectory"
])

with tab1:
    st.markdown("### Search Results & Intelligence Feed")
    if len(filtered_df) == 0:
        st.warning("No articles match the selected filters.")
    else:
        cards_html = ""
        # Display top 50 filtered headlines for 60fps performance
        for _, row in filtered_df.head(50).iterrows():
            sentiment = str(row['Sentiment'])
            conf = float(row['Confidence']) if pd.notnull(row['Confidence']) else 0.85
            pub_name = str(row.get('Publisher', 'Global News'))
            company_name = str(row.get('Company', 'N/A'))
            sector_name = str(row.get('Sector', 'General'))
            headline_text = str(row.get('Headline', 'Market Update'))
            
            if sentiment == 'Bullish':
                s_color, s_bg = "var(--color-bull)", "var(--bg-bull)"
                border_left = f"4px solid {s_color}"
            elif sentiment == 'Bearish':
                s_color, s_bg = "var(--color-bear)", "var(--bg-bear)"
                border_left = f"4px solid {s_color}"
            else:
                s_color, s_bg = "var(--color-neutral)", "var(--bg-neutral)"
                border_left = f"4px solid {s_color}"
                
            date_str = str(row['Date'])[:16] if 'Date' in row else '2026-08-08'
            
            entities_html = f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;'>Publisher: {pub_name}</span>"
            entities_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;'>Company: {company_name}</span>"
            entities_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;'>Sector: {sector_name}</span>"
            
            card = render_template(
                "news_card",
                border_left=border_left,
                headline=headline_text,
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
            st.markdown(clean_html(feed_html), unsafe_allow_html=True)

with tab2:
    if len(filtered_df) > 0:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                sentiment_counts = filtered_df['Sentiment'].value_counts()
                fig_sent = plot_donut_chart(
                    sentiment_counts.index,
                    sentiment_counts.values,
                    "Sentiment Distribution"
                )
                render_plotly_chart(fig_sent, width='stretch')
                
        with c2:
            with st.container(border=True):
                pub_counts = filtered_df['Publisher'].value_counts().head(10)
                fig_pub = plot_bar_chart(
                    pd.DataFrame({'Publisher': pub_counts.index, 'Volume': pub_counts.values}),
                    'Volume',
                    'Publisher',
                    "Top 10 Publishers by Article Volume"
                )
                fig_pub.update_layout(yaxis=dict(autorange="reversed"))
                render_plotly_chart(fig_pub, width='stretch')
    else:
        st.info("No analytics available for current filters.")

with tab3:
    if len(filtered_df) > 0 and 'Date' in filtered_df.columns:
        with st.container(border=True):
            timeline_agg = filtered_df.groupby(filtered_df['Date'].dt.date).size().reset_index(name='News Volume')
            fig_time = plot_time_series(timeline_agg, 'Date', 'News Volume', "Daily News Activity Trajectory")
            render_plotly_chart(fig_time, width='stretch')
    else:
        st.info("No timeline activity available for current filters.")
