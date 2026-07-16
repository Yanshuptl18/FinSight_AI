import streamlit as st
from components.charts import render_plotly_chart
import pandas as pd
from components.utils import load_css, render_page_header
from components.charts import create_kpi_card, plot_bar_chart, plot_donut_chart
from data_loader.loader import load_timeline_data, load_event_influence

load_css()

render_page_header("Event Intelligence Explorer", "Deep dive into market events, severity, and resulting price signals.")

timeline_df = load_timeline_data()
influence_df = load_event_influence()

if timeline_df.empty or influence_df.empty:
    st.warning("No event intelligence data available.")
    st.stop()

# Prepare Data
latest_events = timeline_df.sort_values(by='published_date', ascending=False).head(200)

# Merge influence data onto timeline events
# This gives each event in the timeline its computed influence score and impact category
if 'final_event' in latest_events.columns and 'final_event' in influence_df.columns:
    latest_events = pd.merge(latest_events, influence_df[['final_event', 'influence_score', 'impact_category']], on='final_event', how='left')
else:
    latest_events['influence_score'] = 0.5
    latest_events['impact_category'] = 'Medium'

# Clean up any NaNs
latest_events['influence_score'] = latest_events['influence_score'].fillna(0.5)
latest_events['impact_category'] = latest_events['impact_category'].fillna('Medium')

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Event Filtering")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        impacts = ["All Levels"] + sorted([str(x) for x in influence_df['impact_category'].dropna().unique().tolist()])
        impact_filter = st.selectbox("Impact Category", impacts)
    with col_f2:
        sentiments = ["All"] + sorted(timeline_df['market_signal'].dropna().unique().tolist())
        sentiment_filter = st.selectbox("Market Signal", sentiments)

st.divider()

# --- KPI Section ---
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    high_impact_count = len(influence_df[influence_df['impact_category'] == 'High']) if 'impact_category' in influence_df.columns else 0
    create_kpi_card("High Impact Events", str(high_impact_count), "High Severity", "inverse")
with kpi2:
    if not influence_df.empty:
        top_event = influence_df.sort_values(by='influence_score', ascending=False).iloc[0]
        create_kpi_card("Highest Influence Event", str(top_event['final_event'])[:25] + "..." if len(str(top_event['final_event'])) > 25 else str(top_event['final_event']), f"{top_event['influence_score']:.2f} Score", "normal")
    else:
        create_kpi_card("Highest Influence Event", "N/A", "N/A", "normal")
with kpi3:
    avg_inf = influence_df['influence_score'].mean() if not influence_df.empty else 0
    create_kpi_card("Avg Influence Score", f"{avg_inf:.2f}", "Across all events", "normal")

st.divider()

# Apply Filters
filtered_events = latest_events.copy()

if impact_filter != "All Levels":
    filtered_events = filtered_events[filtered_events['impact_category'] == impact_filter]
    
if sentiment_filter != "All":
    filtered_events = filtered_events[filtered_events['market_signal'] == sentiment_filter]

col1, col2 = st.columns([2, 1.2])

with col1:
    with st.container(border=True):
        st.markdown("### Top Influential Events")
        top_events = influence_df.sort_values(by='influence_score', ascending=False).head(10)
        fig_bar = plot_bar_chart(top_events, 'final_event', 'influence_score', "Event Influence Score")
        render_plotly_chart(fig_bar, width='stretch')
        
    with st.container(border=True):
        st.markdown("### Signal Distribution")
        impact_counts = timeline_df['market_signal'].value_counts()
        if not impact_counts.empty:
            fig_donut = plot_donut_chart(impact_counts.index, impact_counts.values, "Market Signals")
            render_plotly_chart(fig_donut, width='stretch')
        else:
            st.info("No signal data.")

with col2:
    st.markdown("### Major Market Events")
    
    if filtered_events.empty:
        st.warning("No events match the selected filters.")
    else:
        feed_html = "<div style='padding: 10px; max-height: 800px; overflow-y: auto;'>"
        feed_html += "<div style='display: flex; flex-direction: column; gap: 12px;'>"
        
        for _, row in filtered_events.head(50).iterrows():
            inf_score = row.get('influence_score', 0.5)
            impact_cat = row.get('impact_category', 'Medium')
            sentiment = row.get('market_signal', 'Neutral')
            
            # Impact Colors
            if impact_cat == 'High':
                i_color, i_bg = "#ff4d4d", "rgba(255, 77, 77, 0.15)"
            elif impact_cat == 'Medium':
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
            feed_html += f"<div style='font-size: 1.1rem; font-weight: 700; color: var(--text-bright); margin-bottom: 4px;'>{row.get('final_event', 'Unknown Event')}</div>"
            feed_html += f"<div style='font-size: 0.9rem; color: var(--text-primary); font-weight: 500;'>Entity: <span style='color: var(--text-bright);'>{row.get('ticker', 'N/A')}</span></div>"
            feed_html += f"</div>"
            
            date_val = row.get('published_date', None)
            date_str = date_val.strftime('%Y-%m-%d') if pd.notna(date_val) else "N/A"
            feed_html += f"<div style='font-size: 0.85rem; color: var(--text-primary); font-family: monospace; font-weight: 600;'>{date_str}</div>"
            feed_html += f"</div>"
            
            feed_html += f"<div style='display: flex; align-items: center; flex-wrap: wrap; gap: 8px; font-size: 0.85rem;'>"
            feed_html += f"<span style='background: {i_bg}; color: {i_color}; padding: 4px 10px; border-radius: 20px; font-weight: 600; border: 1px solid {i_color};'>Impact: {impact_cat}</span>"
            feed_html += f"<span style='background: {s_bg}; color: {s_color}; padding: 4px 10px; border-radius: 20px; font-weight: 600; border: 1px solid {s_color};'>Signal: {sentiment}</span>"
            feed_html += f"</div></div>"
            
        feed_html += "</div></div>"
        st.markdown(feed_html, unsafe_allow_html=True)
