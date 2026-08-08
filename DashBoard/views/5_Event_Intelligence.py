import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from components.charts import render_plotly_chart, create_kpi_card
from components.utils import load_css, render_page_header, clean_html
from data_loader.loader import (
    load_event_influence,
    load_event_statistics,
    load_event_heatmap,
    load_event_propagation_paths,
    load_timeline_data,
    get_dataset_row_count
)

load_css()

render_page_header(
    "Event Intelligence Explorer",
    "Deep dive into 30 core market event types, 812 propagation pathways, sentiment signals, network centrality, and temporal co-occurrence heatmaps."
)

master_event_df = load_event_influence()
stat_df = load_event_statistics()
heatmap_df = load_event_heatmap()
paths_df = load_event_propagation_paths()
timeline_df = load_timeline_data()

if master_event_df.empty:
    st.warning("Event intelligence data is currently loading or unavailable.")
    st.stop()

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Multi-Dimensional Event Filtering")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ev_list = ["All Events"] + sorted([str(x) for x in master_event_df['final_event'].dropna().unique()])
        selected_event = st.selectbox("Focus Event", ev_list)
        
    with col2:
        impacts = ["All Levels"]
        if 'impact_category' in master_event_df.columns:
            impacts += sorted([str(x) for x in master_event_df['impact_category'].dropna().unique()])
        selected_impact = st.selectbox("Impact Category", impacts)
        
    with col3:
        signals = ["All"]
        if 'market_signal' in timeline_df.columns:
            signals += sorted([str(x) for x in timeline_df['market_signal'].dropna().unique()])
        selected_signal = st.selectbox("Market Signal", signals)

# Apply filters
filtered_events = master_event_df.copy()
if selected_event != "All Events":
    filtered_events = filtered_events[filtered_events['final_event'] == selected_event]
if selected_impact != "All Levels" and 'impact_category' in filtered_events.columns:
    filtered_events = filtered_events[filtered_events['impact_category'] == selected_impact]

st.divider()

# --- Top Key Performance Indicators ---
k1, k2, k3, k4 = st.columns(4)
total_event_items = get_dataset_row_count("financial_intelligence_dataset.parquet") or 3215296
total_pathways = len(paths_df) if not paths_df.empty else 812

with k1:
    create_kpi_card("Event Categories", "30 Core Events", "Categorized Signals", "normal")

with k2:
    create_kpi_card("Event Corpus", f"{total_event_items:,}", "Full News Records", "normal")

with k3:
    if not filtered_events.empty and 'influence_score' in filtered_events.columns:
        top_inf = filtered_events.loc[filtered_events['influence_score'].idxmax()]
        create_kpi_card("Highest Influence", str(top_inf.get('final_event', 'Event')), f"Score: {top_inf.get('influence_score', 0):.1f}", "normal")
    else:
        create_kpi_card("Highest Influence", "N/A", "Score: 0", "normal")

with k4:
    if not filtered_events.empty and 'propagation_risk' in filtered_events.columns:
        top_risk = filtered_events.loc[filtered_events['propagation_risk'].idxmax()]
        create_kpi_card("Propagation Risk", str(top_risk.get('final_event', 'Event')), f"Risk: {top_risk.get('propagation_risk', 0):.1f}", "inverse")
    else:
        create_kpi_card("Propagation Risk", "N/A", "Risk: 0", "inverse")

st.divider()

# --- Multi-Tab Analytics ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Event Sentiment & Signal Distribution",
    "Temporal Co-occurrence Heatmap",
    "Network Centrality & Graph Importance",
    "Propagation Pathways & Risk"
])

with tab1:
    if not filtered_events.empty and 'bullish' in filtered_events.columns:
        melt_df = filtered_events.melt(
            id_vars=['final_event'],
            value_vars=['bullish', 'bearish', 'neutral'],
            var_name='Sentiment',
            value_name='Count'
        )
        melt_df['Sentiment'] = melt_df['Sentiment'].str.capitalize()
        
        fig_sent = px.bar(
            melt_df,
            x='final_event',
            y='Count',
            color='Sentiment',
            title="Event Sentiment Breakdown (Bullish / Bearish / Neutral)",
            color_discrete_map={'Bullish': '#00e676', 'Bearish': '#ff5252', 'Neutral': '#475569'}
        )
        fig_sent.update_layout(
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=80, l=50, r=20),
            xaxis=dict(showgrid=False, title="Market Event", tickangle=-45),
            yaxis=dict(gridcolor='var(--border-color)', title="Article Volume")
        )
        render_plotly_chart(fig_sent, width='stretch')
    else:
        st.info("Event sentiment metrics unavailable.")

with tab2:
    if not heatmap_df.empty:
        fig_hm = px.imshow(
            heatmap_df.T,
            labels=dict(x="Timeline Month", y="Event Category", color="Co-occurrences"),
            title="Temporal Co-occurrence Heatmap Matrix (136 Months)",
            color_continuous_scale="Viridis"
        )
        fig_hm.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=50, l=120, r=20)
        )
        render_plotly_chart(fig_hm, width='stretch')
    else:
        st.info("Event timeline heatmap matrix unavailable.")

with tab3:
    if not filtered_events.empty and 'graph_importance' in filtered_events.columns:
        fig_cent = px.bar(
            filtered_events.sort_values(by='graph_importance', ascending=False),
            x='final_event',
            y='graph_importance',
            color='influence_score',
            title="Event Network Centrality & Graph Importance Ranking"
        )
        fig_cent.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=80, l=50, r=20),
            xaxis=dict(showgrid=False, title="Market Event", tickangle=-45),
            yaxis=dict(gridcolor='var(--border-color)', title="Graph Importance Score")
        )
        render_plotly_chart(fig_cent, width='stretch')
    else:
        st.info("Graph centrality metrics unavailable.")

with tab4:
    st.markdown("### Directional Event Propagation Pathways (812 Routes)")
    if not paths_df.empty:
        path_search = st.text_input("Search Propagation Path (Source / Target)", placeholder="e.g. Analyst Rating, Dividend, Earnings")
        
        pv = paths_df.copy()
        if path_search:
            pv = pv[
                pv['source_event'].str.contains(path_search, case=False, na=False) |
                pv['target_event'].str.contains(path_search, case=False, na=False) |
                pv['path'].str.contains(path_search, case=False, na=False)
            ]
            
        st.dataframe(
            pv[['source_event', 'target_event', 'path_length', 'path']].head(100),
            column_config={
                "source_event": "Originating Event",
                "target_event": "Impacted Event",
                "path_length": "Path Hops",
                "path": "Propagation Trajectory"
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Propagation path dataset unavailable.")

st.divider()

# --- AI Event Knowledge Cards ---
st.markdown("### AI Event Knowledge Base Cards")

if filtered_events.empty:
    st.warning("No events match the selected filters.")
else:
    feed_html = "<div style='padding: 10px; max-height: 800px; overflow-y: auto;'>"
    feed_html += "<div style='display: flex; flex-direction: column; gap: 16px;'>"
    
    for _, row in filtered_events.iterrows():
        ev_name = str(row.get('final_event', 'Event'))
        total_n = row.get('total_news', 0)
        impact = str(row.get('impact_category', 'Medium'))
        inf_score = row.get('influence_score', 50.0)
        peak_y = row.get('peak_year', 'N/A')
        peak_v = row.get('peak_news', 0)
        summary = str(row.get('summary', f"AI impact analysis for {ev_name}."))

        if impact in ["Very High", "High"]:
            color, bg = "var(--color-bear)", "var(--bg-bear)"
            badge = f"Impact: {impact}"
        else:
            color, bg = "var(--color-bull)", "var(--bg-bull)"
            badge = f"Impact: {impact}"

        feed_html += f"<div class='headline-card' style='border-left: 5px solid {color}; padding: 20px;'>"
        feed_html += f"<div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;'>"
        feed_html += f"<div>"
        feed_html += f"<div style='font-size: 1.25rem; font-weight: 700; color: var(--text-bright); margin-bottom: 4px;'>{ev_name}</div>"
        feed_html += f"<div style='font-size: 0.9rem; color: var(--text-primary);'>Total Coverage: <strong style='color: var(--accent);'>{total_n:,} Articles</strong> | Peak Year: <strong style='color: var(--text-bright);'>{peak_y} ({peak_v:,} items)</strong></div>"
        feed_html += f"</div>"
        feed_html += f"<span style='background: {bg}; color: {color}; padding: 6px 14px; border-radius: 20px; font-weight: 700; border: 1px solid {color};'>{badge}</span>"
        feed_html += f"</div>"
        
        feed_html += f"<p style='color: var(--text-primary); font-size: 0.92rem; line-height: 1.5; margin-bottom: 12px;'>{summary}</p>"
        
        # Bullish / Bearish / Neutral Pills
        bull = int(row.get('bullish', 0))
        bear = int(row.get('bearish', 0))
        neu = int(row.get('neutral', 0))
        
        feed_html += f"<div style='display: flex; gap: 12px; font-size: 0.82rem; margin-top: 8px;'>"
        feed_html += f"<span style='color: #00e676; background: rgba(0,230,118,0.1); padding: 4px 10px; border-radius: 12px;'>Bullish: {bull:,}</span>"
        feed_html += f"<span style='color: #ff5252; background: rgba(255,82,82,0.1); padding: 4px 10px; border-radius: 12px;'>Bearish: {bear:,}</span>"
        feed_html += f"<span style='color: #c9d1d9; background: rgba(255,255,255,0.08); padding: 4px 10px; border-radius: 12px;'>Neutral: {neu:,}</span>"
        feed_html += f"</div></div>"
        
    feed_html += "</div></div>"
    st.markdown(clean_html(feed_html), unsafe_allow_html=True)
