import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from components.charts import render_plotly_chart, create_kpi_card, plot_time_series, plot_bar_chart
from components.utils import load_css, render_page_header, clean_html
from data_loader.loader import load_timeline_data

load_css()

render_page_header("Timeline Intelligence Explorer", "Chronological analysis and event intensity mapping across the complete 3,215,296 market news timeline.")

@st.cache_data(ttl=3600, show_spinner="Loading 3.2M Event Timeline...")
def get_timeline_data():
    timeline_df = load_timeline_data()
    if timeline_df.empty:
        return pd.DataFrame(columns=['Date', 'Event Intensity', 'Category', 'Entity', 'Headline', 'Signal'])
        
    rename_map = {
        'published_date': 'Date',
        'final_event': 'Category',
        'ticker': 'Entity',
        'headline': 'Headline',
        'market_signal': 'Signal'
    }
    
    timeline_df = timeline_df.rename(columns=lambda x: rename_map.get(x, x))
    
    if 'Date' in timeline_df.columns:
        timeline_df['Date'] = pd.to_datetime(timeline_df['Date'])
        if hasattr(timeline_df['Date'].dt, 'tz') and timeline_df['Date'].dt.tz is not None:
            timeline_df['Date'] = timeline_df['Date'].dt.tz_localize(None)
        
    if 'event_importance' in timeline_df.columns:
        timeline_df['Event Intensity'] = (timeline_df['event_importance'] * 10).clip(0, 100)
    else:
        timeline_df['Event Intensity'] = 50.0
        
    if 'Category' not in timeline_df.columns:
        timeline_df['Category'] = "General"
    if 'Entity' not in timeline_df.columns:
        timeline_df['Entity'] = "Market"
    if 'Headline' not in timeline_df.columns:
        timeline_df['Headline'] = "Market Event"
    if 'Signal' not in timeline_df.columns:
        timeline_df['Signal'] = "Neutral"
        
    return timeline_df

df = get_timeline_data()

if df.empty:
    st.warning("Timeline data is currently loading or unavailable.")
    st.stop()

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Time Window & Event Selection")
    
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    # Date Slider across full corpus
    selected_dates = st.slider(
        "Select Time Horizon Window:", 
        min_value=min_date, 
        max_value=max_date, 
        value=(pd.to_datetime('2015-01-01').date(), max_date)
    )
    
    c1, c2, c3 = st.columns(3)
    with c1:
        cat_list = ["All Categories"] + sorted(list(df['Category'].dropna().unique()))
        selected_category = st.selectbox("Event Category", cat_list)
    with c2:
        sig_list = ["All Signals"] + sorted(list(df['Signal'].dropna().unique()))
        selected_signal = st.selectbox("Market Signal", sig_list)
    with c3:
        min_intensity = st.slider("Min Event Intensity", 0, 100, 20, 5)

# --- Filter Data Across 3.2M Corpus ---
start_dt = pd.to_datetime(selected_dates[0])
if hasattr(start_dt, 'tz') and start_dt.tz is not None:
    start_dt = start_dt.tz_localize(None)

end_dt = pd.to_datetime(selected_dates[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
if hasattr(end_dt, 'tz') and end_dt.tz is not None:
    end_dt = end_dt.tz_localize(None)

mask = (df['Date'] >= start_dt) & (df['Date'] <= end_dt)
if selected_category != "All Categories":
    mask &= (df['Category'] == selected_category)
if selected_signal != "All Signals":
    mask &= (df['Signal'] == selected_signal)
mask &= (df['Event Intensity'] >= min_intensity)

filtered_df = df.loc[mask]
total_events = len(filtered_df)

st.divider()

# --- 4 Dynamic KPIs ---
k1, k2, k3, k4 = st.columns(4)

with k1:
    create_kpi_card("Events in Window", f"{total_events:,}", "Full Dataset Match", "normal")

with k2:
    if total_events > 0:
        most_active = str(filtered_df['Category'].mode()[0])
        create_kpi_card("Dominant Category", most_active, "Highest Volume", "normal")
    else:
        create_kpi_card("Dominant Category", "N/A", "0 Events", "normal")

with k3:
    avg_int = int(filtered_df['Event Intensity'].mean()) if total_events > 0 else 0
    create_kpi_card("Average Intensity", f"{avg_int}/100", "Market Impact Score", "normal")

with k4:
    unique_entities = filtered_df['Entity'].nunique() if total_events > 0 else 0
    create_kpi_card("Impacted Entities", f"{unique_entities:,}", "Active Tickers", "normal")

st.divider()

# --- Multi-Tab Analytics ---
tab1, tab2, tab3 = st.tabs([
    "Timeline Volume & Intensity Density",
    "Category Distribution Breakdown",
    "High-Impact Dynamic Event Feed"
])

with tab1:
    if total_events > 0:
        st.markdown("### Chronological News Activity & Intensity Trajectory")
        
        # 1. Timeline Volume Trend
        timeline_agg = filtered_df.groupby(filtered_df['Date'].dt.date).size().reset_index(name='News Volume')
        fig_timeline = plot_time_series(timeline_agg, 'Date', 'News Volume', "Full Timeline News Volume Trajectory", enable_rangeslider=True)
        render_plotly_chart(fig_timeline, width='stretch')
        
        st.divider()
        
        # 2. Event Intensity Distribution Map (Sample representative events across time for smooth browser rendering & true 0-100 spread)
        st.markdown("### Event Intensity Distribution Map")
        if len(filtered_df) > 2500:
            scatter_df = filtered_df.sample(n=2500, random_state=42).sort_values(by='Date')
        else:
            scatter_df = filtered_df.sort_values(by='Date')
        
        fig_scatter = px.scatter(
            scatter_df,
            x='Date',
            y='Event Intensity',
            size='Event Intensity',
            color='Category',
            hover_name='Headline',
            title="Event Intensity Distribution (Real Historical Data)",
            height=480
        )
        fig_scatter.update_traces(
            marker=dict(line=dict(width=1, color='rgba(255,255,255,0.2)')),
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=50, l=50, r=20),
            xaxis=dict(showgrid=False, title="Date"),
            yaxis=dict(gridcolor='var(--border-color)', range=[0, 105], title="Event Intensity Score (0-100)")
        )
        render_plotly_chart(fig_scatter, width='stretch')
    else:
        st.info("No events match the selected timeline filters.")

with tab2:
    if total_events > 0:
        st.markdown("### Category Event Volume in Window")
        cat_counts = filtered_df['Category'].value_counts().head(15).reset_index()
        cat_counts.columns = ['Category', 'Volume']
        
        fig_cat = plot_bar_chart(cat_counts, 'Volume', 'Category', "Top Event Categories by Volume")
        fig_cat.update_layout(yaxis=dict(autorange="reversed"))
        render_plotly_chart(fig_cat, width='stretch')
    else:
        st.info("No category data available.")

with tab3:
    st.markdown("### High-Impact Event Feed")
    if total_events == 0:
        st.info("No events available in current window.")
    else:
        top_events = filtered_df.sort_values(by='Event Intensity', ascending=False).head(50)
        
        cards_html = ""
        feed_html = "<div style='padding: 10px; max-height: 750px; overflow-y: auto;'>"
        feed_html += "<div style='display: flex; flex-direction: column; gap: 14px;'>"
        
        for _, row in top_events.iterrows():
            cat = str(row['Category'])
            intensity = int(row['Event Intensity'])
            headline = str(row['Headline'])
            entity = str(row['Entity'])
            date_str = str(row['Date'])[:10]
            signal = str(row.get('Signal', 'Neutral'))
            
            if signal == 'Bullish':
                color, bg = "var(--color-bull)", "var(--bg-bull)"
            elif signal == 'Bearish':
                color, bg = "var(--color-bear)", "var(--bg-bear)"
            else:
                color, bg = "var(--color-neutral)", "var(--bg-neutral)"
                
            feed_html += f"<div class='headline-card' style='border-left: 4px solid {color}; padding: 16px;'>"
            feed_html += f"<div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;'>"
            feed_html += f"<div>"
            feed_html += f"<div style='font-size: 1.05rem; font-weight: 700; color: var(--text-bright); margin-bottom: 4px;'>{headline}</div>"
            feed_html += f"<div style='font-size: 0.85rem; color: var(--text-primary); font-weight: 500;'>Impacted Entity: <strong style='color: var(--accent);'>{entity}</strong></div>"
            feed_html += f"</div>"
            feed_html += f"<div style='font-size: 0.8rem; color: var(--text-primary); font-family: monospace; font-weight: 600; white-space: nowrap; margin-left: 10px;'>{date_str}</div>"
            feed_html += f"</div>"
            
            feed_html += f"<div style='display: flex; align-items: center; gap: 12px; font-size: 0.85rem; margin-top: 8px;'>"
            feed_html += f"<span style='background: {bg}; color: {color}; padding: 4px 12px; border-radius: 20px; font-weight: 600; border: 1px solid {color};'>{cat}</span>"
            feed_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 12px; border-radius: 20px; font-weight: 500; border: 1px solid var(--border-color);'>Intensity: <strong style='color: #ff9900;'>{intensity}</strong>/100</span>"
            feed_html += f"<span style='background: var(--bg-secondary); color: var(--text-primary); padding: 4px 12px; border-radius: 20px; font-weight: 500; margin-left: auto;'>Signal: {signal}</span>"
            feed_html += f"</div></div>"
            
        feed_html += "</div></div>"
        st.markdown(clean_html(feed_html), unsafe_allow_html=True)
