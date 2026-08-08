import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from components.charts import render_plotly_chart, create_kpi_card
from components.utils import load_css, render_page_header, clean_html
from data_loader.loader import (
    load_topic_profiles,
    load_topic_timeline,
    load_clustered_topics,
    load_topic_similarity,
    get_dataset_row_count
)

load_css()

render_page_header(
    "Topic Intelligence Explorer",
    "In-depth analysis of market topics, sub-clusters, sentiment trends, and sector relevance across 3.2M+ financial news records."
)


master_topic_df = load_topic_profiles()
timeline_df = load_topic_timeline()

if master_topic_df.empty and timeline_df.empty:
    st.warning("Topic intelligence data is loading or unavailable.")
    st.stop()

# Clean topic names for display
if not master_topic_df.empty and 'topic_name' in master_topic_df.columns:
    master_topic_df['display_name'] = master_topic_df['topic_name'].str.replace(r' \d+$', '', regex=True)
else:
    master_topic_df['display_name'] = master_topic_df.get('topic_name', '')

if not timeline_df.empty and 'topic_name' in timeline_df.columns:
    timeline_df['display_name'] = timeline_df['topic_name'].str.replace(r' \d+$', '', regex=True)
    if 'month' in timeline_df.columns:
        timeline_df['Date'] = pd.to_datetime(timeline_df['month'])

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Filter Topics")

    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        top_list = ["All Topics"]
        if 'display_name' in master_topic_df.columns:
            top_list += sorted(list(master_topic_df['display_name'].dropna().unique()))
        selected_topic = st.selectbox("Focus Topic", top_list)
        
    with f_col2:
        lifecycles = ["All"]
        if 'lifecycle' in master_topic_df.columns:
            lifecycles += sorted([str(l) for l in master_topic_df['lifecycle'].dropna().unique()])
        selected_lifecycle = st.selectbox("Lifecycle Stage", lifecycles)
        
    with f_col3:
        diversity_cats = ["All"]
        if 'diversity_category' in master_topic_df.columns:
            diversity_cats += sorted([str(d) for d in master_topic_df['diversity_category'].dropna().unique()])
        selected_diversity = st.selectbox("Diversity Category", diversity_cats)

# Apply Filters to Master Topics
filtered_topics = master_topic_df.copy()
if selected_topic != "All Topics":
    filtered_topics = filtered_topics[filtered_topics['display_name'] == selected_topic]
if selected_lifecycle != "All" and 'lifecycle' in filtered_topics.columns:
    filtered_topics = filtered_topics[filtered_topics['lifecycle'] == selected_lifecycle]
if selected_diversity != "All" and 'diversity_category' in filtered_topics.columns:
    filtered_topics = filtered_topics[filtered_topics['diversity_category'] == selected_diversity]

st.divider()

# --- Top Key Performance Indicators ---
k1, k2, k3, k4 = st.columns(4)
total_news_corpus = get_dataset_row_count("financial_intelligence_dataset.parquet") or 3215296
total_subclusters = get_dataset_row_count("clustered_topics.parquet") or 2913

with k1:
    create_kpi_card("Monitored Topics", "20 Core Topics", f"{total_subclusters:,} Sub-Clusters", "normal")

with k2:
    create_kpi_card("Corpus Mentions", f"{total_news_corpus:,}", "Full News Coverage", "normal")

with k3:
    if not filtered_topics.empty and 'avg_growth' in filtered_topics.columns:
        top_growth = filtered_topics.loc[filtered_topics['avg_growth'].idxmax()]
        create_kpi_card("Highest Momentum", str(top_growth.get('display_name', 'Topic')), f"+{top_growth.get('avg_growth', 0):.1f}%", "normal")
    else:
        create_kpi_card("Highest Momentum", "N/A", "+0%", "normal")

with k4:
    if not filtered_topics.empty and 'company_diversity' in filtered_topics.columns:
        top_div = filtered_topics.loc[filtered_topics['company_diversity'].idxmax()]
        create_kpi_card("Broadest Coverage", str(top_div.get('display_name', 'Topic')), f"{top_div.get('company_diversity', 0):,} Orgs", "normal")
    else:
        create_kpi_card("Broadest Coverage", "N/A", "0 Orgs", "normal")

st.divider()

# --- Multi-Tab Analytics ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Monthly Trends & Momentum",
    "Popularity vs Diversity Matrix",
    "Topic Cross-Similarity",
    "2,913 Sub-Cluster Explorer"
])

with tab1:
    if not timeline_df.empty:
        if selected_topic == "All Topics":
            timeline_filtered = timeline_df
        else:
            timeline_filtered = timeline_df[timeline_df['display_name'] == selected_topic]
            
        # Group by Date & display_name
        timeline_agg = timeline_filtered.groupby(['Date', 'display_name'])['articles'].sum().reset_index()
        
        fig_time = px.line(
            timeline_agg,
            x='Date',
            y='articles',
            color='display_name',
            title="Monthly Topic Volume & Trajectory"
        )
        fig_time.update_traces(mode='lines+markers', marker=dict(size=5))
        fig_time.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=60, l=50, r=20),
            xaxis=dict(showgrid=False, title="Timeline Month"),
            yaxis=dict(gridcolor='var(--border-color)', title="Article Count")
        )
        render_plotly_chart(fig_time, width='stretch')
    else:
        st.info("Timeline trend data unavailable.")

with tab2:
    if not filtered_topics.empty and 'popularity_score' in filtered_topics.columns and 'company_diversity' in filtered_topics.columns:
        fig_matrix = px.scatter(
            filtered_topics,
            x='company_diversity',
            y='popularity_score',
            size='articles',
            color='lifecycle' if 'lifecycle' in filtered_topics.columns else None,
            hover_name='display_name',
            title="Topic Strategic Matrix: Popularity vs Corporate Coverage"
        )
        fig_matrix.update_traces(marker=dict(line=dict(width=2, color='var(--bg-primary)')))
        fig_matrix.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=60, l=50, r=20),
            xaxis=dict(gridcolor='var(--border-color)', title="Company Diversity (Unique Orgs)"),
            yaxis=dict(gridcolor='var(--border-color)', title="Popularity Score")
        )
        render_plotly_chart(fig_matrix, width='stretch')
    else:
        st.info("Popularity vs diversity matrix metrics unavailable.")

with tab3:
    similarity_df = load_topic_similarity()
    if not similarity_df.empty:
        fig_sim = px.bar(
            similarity_df.sort_values(by='similarity', ascending=True).tail(15),
            y='topic_1',
            x='similarity',
            color='topic_2',
            orientation='h',
            title="Top Inter-Topic Embedding Similarities"
        )
        fig_sim.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=60, l=150, r=20),
            xaxis=dict(gridcolor='var(--border-color)', title="Cosine Similarity Score"),
            yaxis=dict(showgrid=False, title="Primary Topic")
        )
        render_plotly_chart(fig_sim, width='stretch')
    else:
        st.info("Topic similarity matrix unavailable.")

with tab4:
    st.markdown("### Topic Sub-Clusters (2,913 Groups)")

    clustered_df = load_clustered_topics()
    if not clustered_df.empty:

        search_kw = st.text_input("Search Sub-Cluster Keywords / Headlines", placeholder="e.g. Dividend, Semiconductor, CEO, Acquisition")
        
        clust_view = clustered_df.copy()
        if search_kw:
            mask = (
                clust_view['topic_name'].str.contains(search_kw, case=False, na=False) |
                clust_view['keywords'].str.contains(search_kw, case=False, na=False) |
                clust_view['headline'].str.contains(search_kw, case=False, na=False)
            )
            clust_view = clust_view[mask]
            
        st.dataframe(
            clust_view[['cluster', 'topic_name', 'keywords', 'headline_count', 'avg_confidence', 'headline']].head(100),
            column_config={
                "cluster": "Cluster ID",
                "topic_name": "Sub-Topic Name",
                "keywords": "Extracted Keywords",
                "headline_count": "Articles",
                "avg_confidence": st.column_config.NumberColumn("Model Confidence", format="%.2f"),
                "headline": "Sample Representative Headline"
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Sub-cluster dataset unavailable.")

st.divider()

# --- Topic Briefs & Profiles ---
st.markdown("### Topic Insights & Briefs")


if filtered_topics.empty:
    st.warning("No topics match the selected filters.")
else:
    feed_html = "<div style='padding: 10px; max-height: 800px; overflow-y: auto;'>"
    feed_html += "<div style='display: flex; flex-direction: column; gap: 16px;'>"
    
    for _, row in filtered_topics.iterrows():
        name = str(row.get('display_name', row.get('topic_name', 'Topic')))
        growth = row.get('avg_growth', row.get('growth_score', 0))
        articles = row.get('articles', row.get('Mentions', 0))
        lifecycle = str(row.get('lifecycle', 'Active'))
        summary = str(row.get('summary', f"AI intelligence summary and key drivers for {name}."))
        keywords = str(row.get('keywords', 'market, intelligence, trends'))

        if growth > 40:
            color, bg = "var(--color-bull)", "var(--bg-bull)"
            badge = f"↑ +{growth:.1f}% Growth"
        elif growth < 0:
            color, bg = "var(--color-bear)", "var(--bg-bear)"
            badge = f"↓ {growth:.1f}% Contraction"
        else:
            color, bg = "var(--color-neutral)", "var(--bg-neutral)"
            badge = f"~ {growth:.1f}% Stable"

        feed_html += f"<div class='headline-card' style='border-left: 5px solid {color}; padding: 20px;'>"
        feed_html += f"<div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;'>"
        feed_html += f"<div>"
        feed_html += f"<div style='font-size: 1.25rem; font-weight: 700; color: var(--text-bright); margin-bottom: 4px;'>{name}</div>"
        feed_html += f"<div style='font-size: 0.9rem; color: var(--text-primary);'>Total Mentions: <strong style='color: var(--accent);'>{articles:,}</strong> | Lifecycle Stage: <strong style='color: var(--text-bright);'>{lifecycle}</strong></div>"
        feed_html += f"</div>"
        feed_html += f"<span style='background: {bg}; color: {color}; padding: 6px 14px; border-radius: 20px; font-weight: 700; border: 1px solid {color};'>{badge}</span>"
        feed_html += f"</div>"
        
        feed_html += f"<p style='color: var(--text-primary); font-size: 0.92rem; line-height: 1.5; margin-bottom: 12px;'>{summary}</p>"
        
        feed_html += f"<div style='font-size: 0.85rem; color: var(--text-primary); font-style: italic; background: var(--border-color); padding: 8px 12px; border-radius: 6px;'>Key Keywords: {keywords}</div>"
        feed_html += f"</div>"
        
    feed_html += "</div></div>"
    st.markdown(clean_html(feed_html), unsafe_allow_html=True)
