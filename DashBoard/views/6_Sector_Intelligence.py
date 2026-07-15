import streamlit as st
from components.charts import render_plotly_chart
import plotly.express as px
from data_loader.loader import load_mock_sector_data
from components.charts import plot_bar_chart, create_kpi_card

from components.utils import load_css, render_page_header
load_css()

render_page_header("Sector Intelligence Explorer", "Analyze sector performance, risk, and growth trends based on NLP aggregations.")

sector_df = load_mock_sector_data()

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Sector Filtering")
    recommendations = ["All"] + list(sector_df['Recommendation'].unique())
    rec_filter = st.selectbox("Filter by Recommendation", recommendations)

# Apply Filter
if rec_filter != "All":
    filtered_df = sector_df[sector_df['Recommendation'] == rec_filter]
else:
    filtered_df = sector_df

st.divider()

# --- Top Metrics ---
col1, col2, col3 = st.columns(3)
top_sector = sector_df.loc[sector_df['Growth Score'].idxmax()]
highest_risk = sector_df.loc[sector_df['Risk Score'].idxmax()]
most_active = sector_df.loc[sector_df['News Volume'].idxmax()]

with col1:
    create_kpi_card("Fastest Growing", top_sector['Sector'], f"Score: {top_sector['Growth Score']}", "normal")
with col2:
    create_kpi_card("Highest Risk", highest_risk['Sector'], f"Risk: {highest_risk['Risk Score']}", "inverse")
with col3:
    create_kpi_card("Most Active", most_active['Sector'], f"{most_active['News Volume']} articles", "normal")

st.divider()

# --- Sector Analysis Charts ---
col_chart1, col_chart2 = st.columns([1.5, 1])

with col_chart1:
    with st.container(border=True):
        st.markdown("### Risk vs Growth Matrix")
        fig_scatter = px.scatter(
            filtered_df, 
            x='Risk Score', 
            y='Growth Score', 
            size='News Volume', 
            color='Recommendation',
            hover_name='Sector',
            title="Sector Positioning"
        )
        fig_scatter.update_traces(
            marker=dict(line=dict(width=2, color='var(--bg-primary)')),
            selector=dict(mode='markers')
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=60, l=50, r=20)
        )
        render_plotly_chart(fig_scatter, width='stretch')

with col_chart2:
    with st.container(border=True):
        st.markdown("### News Volume by Sector")
        fig_bar = plot_bar_chart(filtered_df, 'Sector', 'News Volume', "Sector Media Coverage", color='Recommendation')
        render_plotly_chart(fig_bar, width='stretch')

st.divider()

# --- Data Table Feed ---
st.markdown("### Sector Intelligence Data")

if filtered_df.empty:
    st.warning("No sectors match the selected filter.")
else:
    feed_html = "<div style=\'padding: 10px; max-height: 700px; overflow-y: auto;\'>"
    feed_html += "<div style='display: flex; flex-direction: column; gap: 12px;'>"
    
    for _, row in filtered_df.iterrows():
        rec = row['Recommendation']
        
        # Color coding based on recommendation
        if rec == 'Strong Buy':
            color, bg = "var(--color-bull)", "var(--bg-bull)"
        elif rec == 'Buy':
            color, bg = "#69f0ae", "rgba(105, 240, 174, 0.15)"
        elif rec == 'Watch':
            color, bg = "#ffa726", "rgba(255, 167, 38, 0.15)"
        elif rec == 'Avoid':
            color, bg = "#ff5252", "rgba(255, 82, 82, 0.15)"
        else:
            color, bg = "#4da6ff", "rgba(77, 166, 255, 0.15)"
            
        feed_html += f"<div class='headline-card' style='border-left: 4px solid {color}; padding: 16px;'>"
        feed_html += f"<div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;'>"
        feed_html += f"<div>"
        feed_html += f"<div style='font-size: 1.15rem; font-weight: 700; color: var(--text-bright); margin-bottom: 4px;'>{row['Sector']}</div>"
        feed_html += f"<div style='font-size: 0.9rem; color: var(--text-primary); font-weight: 500;'>News Volume: <span style='color: var(--text-bright);'>{row['News Volume']}</span></div>"
        feed_html += f"</div>"
        feed_html += f"<span style='background: {bg}; color: {color}; padding: 6px 14px; border-radius: 20px; font-weight: 700; border: 1px solid {color};'>Recommendation: {rec}</span>"
        feed_html += f"</div>"
        
        feed_html += f"<div style='display: flex; align-items: center; gap: 16px; font-size: 0.9rem;'>"
        feed_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 12px; border-radius: 6px; font-weight: 500; border: 1px solid var(--border-color);'>Growth Score: <span style='color:#00e676;'>{row['Growth Score']}</span>/100</span>"
        feed_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 12px; border-radius: 6px; font-weight: 500; border: 1px solid var(--border-color);'>Risk Score: <span style='color:#ff5252;'>{row['Risk Score']}</span>/100</span>"
        feed_html += f"</div></div>"
        
    feed_html += "</div></div>"
    st.markdown(feed_html, unsafe_allow_html=True)
