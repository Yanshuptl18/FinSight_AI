import streamlit as st
import plotly.express as px
import pandas as pd
from components.charts import render_plotly_chart, create_kpi_card
from data_loader.loader import (
    load_sector_data,
    load_sector_relationships,
    load_sector_temporal,
    load_sector_clusters,
    load_investment_themes
)
from components.utils import load_css, render_page_header, clean_html, THEMES

load_css()

render_page_header(
    "Sector Intelligence Explorer",
    "Comprehensive sector analysis incorporating network centrality, temporal momentum, macro investment themes, and AI knowledge bases."
)

sector_df = load_sector_data()
temporal_df = load_sector_temporal()
cluster_df = load_sector_clusters()
themes_df = load_investment_themes()
rel_df = load_sector_relationships()

if sector_df.empty:
    st.warning("Sector intelligence data is loading or unavailable.")
    st.stop()

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Multi-Dimensional Sector Filtering")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        recs = ["All"] + sorted([str(r) for r in sector_df['Recommendation'].unique() if pd.notna(r)])
        rec_filter = st.selectbox("Filter by Recommendation", recs)
        
    with f_col2:
        themes = ["All"]
        if 'investment_theme' in sector_df.columns:
            themes += sorted([str(t) for t in sector_df['investment_theme'].unique() if pd.notna(t)])
        theme_filter = st.selectbox("Filter by Investment Theme", themes)
        
    with f_col3:
        stabilities = ["All"]
        if 'market_stability_category' in sector_df.columns:
            stabilities += sorted([str(s) for s in sector_df['market_stability_category'].unique() if pd.notna(s)])
        stability_filter = st.selectbox("Filter by Market Stability", stabilities)

# Apply Filters
filtered_df = sector_df.copy()
if rec_filter != "All":
    filtered_df = filtered_df[filtered_df['Recommendation'] == rec_filter]
if theme_filter != "All" and 'investment_theme' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['investment_theme'] == theme_filter]
if stability_filter != "All" and 'market_stability_category' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['market_stability_category'] == stability_filter]

st.divider()

# --- Top Key Performance Indicators ---
col1, col2, col3, col4 = st.columns(4)
if not filtered_df.empty:
    top_growth = filtered_df.loc[filtered_df['Growth Score'].idxmax()] if 'Growth Score' in filtered_df.columns else filtered_df.iloc[0]
    top_risk = filtered_df.loc[filtered_df['Risk Score'].idxmax()] if 'Risk Score' in filtered_df.columns else filtered_df.iloc[0]
    most_active = filtered_df.loc[filtered_df['News Volume'].idxmax()] if 'News Volume' in filtered_df.columns else filtered_df.iloc[0]
    most_influential = filtered_df.sort_values(by='network_influence', ascending=False).iloc[0] if 'network_influence' in filtered_df.columns and not filtered_df['network_influence'].dropna().empty else top_growth

    with col1:
        create_kpi_card("Fastest Growing", str(top_growth['Sector']), f"Score: {top_growth['Growth Score']}", "normal")
    with col2:
        create_kpi_card("Highest Risk", str(top_risk['Sector']), f"Risk Score: {top_risk['Risk Score']}", "inverse")
    with col3:
        create_kpi_card("Most Active", str(most_active['Sector']), f"{most_active['News Volume']:,} articles", "normal")
    with col4:
        influence_val = f"Influence: {most_influential.get('network_influence', 0):.3f}" if 'network_influence' in most_influential else "Top Ranked"
        create_kpi_card("Network Leader", str(most_influential['Sector']), influence_val, "normal")
else:
    with col1: create_kpi_card("Fastest Growing", "N/A", "Score: 0", "normal")
    with col2: create_kpi_card("Highest Risk", "N/A", "Risk: 0", "inverse")
    with col3: create_kpi_card("Most Active", "N/A", "0 articles", "normal")
    with col4: create_kpi_card("Network Leader", "N/A", "Rank: N/A", "normal")

st.divider()

# Color Map
rec_colors = {
    'Strong Buy': '#00e676',
    'Buy': '#69f0ae',
    'Watch': '#ffa726',
    'Avoid': '#ff5252',
    'Neutral': '#4da6ff'
}

# --- Main Analytics Dashboard ---
tab1, tab2, tab3 = st.tabs(["Positioning & Network Centrality", "Temporal Growth & Momentum", "Macro Themes & Knowledge Base"])

with tab1:
    c_left, c_right = st.columns([1.5, 1])
    
    with c_left:
        with st.container(border=True):
            st.markdown("### Risk vs Growth Matrix")
            if not filtered_df.empty:
                fig_scatter = px.scatter(
                    filtered_df,
                    x='Risk Score',
                    y='Growth Score',
                    size='News Volume',
                    color='Recommendation',
                    color_discrete_map=rec_colors,
                    hover_name='Sector',
                    title="Sector Strategic Positioning Matrix"
                )
                fig_scatter.update_traces(
                    marker=dict(line=dict(width=2, color='var(--bg-primary)')),
                    selector=dict(mode='markers')
                )
                fig_scatter.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=50, b=60, l=50, r=20),
                    xaxis=dict(gridcolor='var(--border-color)'),
                    yaxis=dict(gridcolor='var(--border-color)')
                )
                render_plotly_chart(fig_scatter, width='stretch')
            else:
                st.info("No sectors match current filters.")
                
    with c_right:
        with st.container(border=True):
            st.markdown("### Network Centrality & Influence")
            if not filtered_df.empty and 'network_influence' in filtered_df.columns:
                net_sorted = filtered_df.dropna(subset=['network_influence']).sort_values(by='network_influence', ascending=True)
                fig_net = px.bar(
                    net_sorted,
                    y='Sector',
                    x='network_influence',
                    color='Recommendation',
                    color_discrete_map=rec_colors,
                    orientation='h',
                    title="Inter-Sector Centrality Index"
                )
                fig_net.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=50, b=60, l=80, r=20),
                    xaxis=dict(gridcolor='var(--border-color)'),
                    yaxis=dict(showgrid=False)
                )
                render_plotly_chart(fig_net, width='stretch')
            else:
                st.info("Network metrics processing or unavailable.")

with tab2:
    if not temporal_df.empty:
        t_left, t_right = st.columns([1, 1])
        with t_left:
            with st.container(border=True):
                st.markdown("### Average Monthly Growth Rate")
                fig_growth = px.bar(
                    temporal_df.sort_values(by='average_growth', ascending=False),
                    x='sector',
                    y='average_growth',
                    color='average_growth',
                    color_continuous_scale='Viridis',
                    title="Sector Growth Velocity"
                )
                fig_growth.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=50, b=60, l=50, r=20),
                    xaxis=dict(showgrid=False, title="Sector"),
                    yaxis=dict(gridcolor='var(--border-color)', title="Growth Rate")
                )
                render_plotly_chart(fig_growth, width='stretch')
                
        with t_right:
            with st.container(border=True):
                st.markdown("### Peak News Volume per Sector")
                fig_peak = px.bar(
                    temporal_df.sort_values(by='peak_news', ascending=False),
                    x='sector',
                    y='peak_news',
                    color='peak_news',
                    color_continuous_scale='Magma',
                    title="Historical Peak News Volume"
                )
                fig_peak.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=50, b=60, l=50, r=20),
                    xaxis=dict(showgrid=False, title="Sector"),
                    yaxis=dict(gridcolor='var(--border-color)', title="Peak Volume")
                )
                render_plotly_chart(fig_peak, width='stretch')
    else:
        st.info("Temporal trend data unavailable.")

with tab3:
    m1, m2 = st.columns([1, 1])
    
    with m1:
        with st.container(border=True):
            st.markdown("### Macro Investment Themes")
            if not themes_df.empty:
                # 1. Plotly Theme Strength Chart
                fig_themes = px.bar(
                    themes_df,
                    x='average_strength',
                    y='investment_theme',
                    orientation='h',
                    color='average_strength',
                    color_continuous_scale='Tealgrn',
                    title="Theme Strength Score"
                )
                fig_themes.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=40, b=40, l=120, r=20),
                    xaxis=dict(gridcolor='var(--border-color)', title="Strength Score"),
                    yaxis=dict(showgrid=False, title="")
                )
                render_plotly_chart(fig_themes, width='stretch')
                
                # 2. Glassmorphic Theme Cards
                t_html = "<div style='display: flex; flex-direction: column; gap: 12px; margin-top: 15px;'>"
                for _, row in themes_df.iterrows():
                    th_name = str(row['investment_theme'])
                    sec_cnt = int(row['sectors'])
                    str_score = float(row['average_strength'])
                    
                    t_html += f"""
                    <div style='background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 14px; display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <div style='font-size: 1.05rem; font-weight: 700; color: var(--text-bright);'>{th_name}</div>
                            <div style='font-size: 0.85rem; color: var(--text-primary); margin-top: 4px;'>Affected Sectors: <strong style='color: var(--accent);'>{sec_cnt} Sectors</strong></div>
                        </div>
                        <span style='background: var(--bg-bull); color: var(--color-bull); border: 1px solid var(--color-bull); padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.9rem;'>
                            Strength: {str_score:.1f}
                        </span>
                    </div>
                    """
                t_html += "</div>"
                st.markdown(clean_html(t_html), unsafe_allow_html=True)
            else:
                st.info("No macro themes data available.")
                
    with m2:
        with st.container(border=True):
            st.markdown("### Sector Cluster Communities")
            if not cluster_df.empty:
                # 1. Plotly Cluster Intelligence & Risk Comparison Chart
                comm_melt = cluster_df.melt(
                    id_vars=['community', 'strongest_sector'],
                    value_vars=['avg_intelligence', 'avg_risk'],
                    var_name='Metric',
                    value_name='Score'
                )
                comm_melt['Metric'] = comm_melt['Metric'].map({'avg_intelligence': 'Avg Intelligence', 'avg_risk': 'Avg Risk'})
                comm_melt['Cluster'] = comm_melt['community'].astype(int).map(lambda x: f"Cluster {x}")
                
                fig_comm = px.bar(
                    comm_melt,
                    x='Cluster',
                    y='Score',
                    color='Metric',
                    barmode='group',
                    title="Cluster Intelligence vs Risk Profile",
                    color_discrete_map={'Avg Intelligence': 'var(--accent)', 'Avg Risk': '#ff5252'}
                )
                fig_comm.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=40, b=40, l=50, r=20),
                    xaxis=dict(showgrid=False, title="Community Cluster"),
                    yaxis=dict(gridcolor='var(--border-color)', title="Score")
                )
                render_plotly_chart(fig_comm, width='stretch')
                
                # 2. Glassmorphic Cluster Cards
                c_html = "<div style='display: flex; flex-direction: column; gap: 12px; margin-top: 15px;'>"
                for _, row in cluster_df.iterrows():
                    comm_id = int(row['community']) if pd.notna(row['community']) else 0
                    lead_sec = str(row['strongest_sector'])
                    avg_intel = float(row['avg_intelligence'])
                    avg_rk = float(row['avg_risk'])
                    
                    c_html += f"""
                    <div style='background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 14px;'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                            <div style='font-size: 1.05rem; font-weight: 700; color: var(--text-bright);'>Community Cluster {comm_id}</div>
                            <span style='background: var(--bg-secondary); color: var(--text-primary); border: 1px solid var(--border-color); padding: 4px 12px; border-radius: 15px; font-size: 0.8rem; font-weight: 600;'>
                                Lead: {lead_sec}
                            </span>
                        </div>
                        <div style='display: flex; gap: 12px; font-size: 0.85rem;'>
                            <span style='color: var(--color-bull); background: var(--bg-bull); padding: 4px 10px; border-radius: 12px; border: 1px solid var(--color-bull);'>Intelligence: {avg_intel:.1f}</span>
                            <span style='color: #ff5252; background: rgba(255,82,82,0.1); padding: 4px 10px; border-radius: 12px; border: 1px solid rgba(255,82,82,0.3);'>Risk: {avg_rk:.1f}</span>
                        </div>
                    </div>
                    """
                c_html += "</div>"
                st.markdown(clean_html(c_html), unsafe_allow_html=True)
            else:
                st.info("No cluster data available.")

st.divider()

# --- Detailed Sector Intelligence Knowledge Base ---
st.markdown("### AI Sector Knowledge Base & Detailed Profiles")

if filtered_df.empty:
    st.warning("No sectors match the selected filters.")
else:
    feed_html = "<div style='padding: 10px; max-height: 800px; overflow-y: auto;'>"
    feed_html += "<div style='display: flex; flex-direction: column; gap: 16px;'>"
    
    for _, row in filtered_df.iterrows():
        rec = str(row['Recommendation'])
        sec_name = str(row['Sector'])
        vol = row.get('News Volume', 0)
        growth = row.get('Growth Score', 50)
        risk = row.get('Risk Score', 50)
        theme = row.get('investment_theme', 'General')
        lifecycle = row.get('lifecycle', 'Active')
        stability = row.get('market_stability_category', 'Standard')
        desc = row.get('complete_description', f"Sector analytics profile for {sec_name}.")

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
            
        feed_html += f"<div class='headline-card' style='border-left: 5px solid {color}; padding: 20px;'>"
        feed_html += f"<div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;'>"
        feed_html += f"<div>"
        feed_html += f"<div style='font-size: 1.25rem; font-weight: 700; color: var(--text-bright); margin-bottom: 4px;'>{sec_name}</div>"
        feed_html += f"<div style='font-size: 0.9rem; color: var(--text-primary);'>News Volume: <strong style='color: var(--text-bright);'>{vol:,}</strong> | Investment Theme: <strong style='color: var(--accent);'>{theme}</strong></div>"
        feed_html += f"</div>"
        feed_html += f"<span style='background: {bg}; color: {color}; padding: 6px 14px; border-radius: 20px; font-weight: 700; border: 1px solid {color};'>Recommendation: {rec}</span>"
        feed_html += f"</div>"
        
        feed_html += f"<p style='color: var(--text-primary); font-size: 0.92rem; line-height: 1.5; margin-bottom: 14px;'>{desc}</p>"
        
        feed_html += f"<div style='display: flex; flex-wrap: wrap; gap: 12px; font-size: 0.85rem;'>"
        feed_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 6px; font-weight: 600;'>Growth Score: <span style='color:#00e676;'>{growth}</span>/100</span>"
        feed_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 6px; font-weight: 600;'>Risk Score: <span style='color:#ff5252;'>{risk}</span>/100</span>"
        feed_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 6px; font-weight: 600;'>Lifecycle: <span style='color:var(--accent);'>{lifecycle}</span></span>"
        feed_html += f"<span style='background: var(--border-color); color: var(--text-bright); padding: 4px 10px; border-radius: 6px; font-weight: 600;'>Stability: {stability}</span>"
        feed_html += f"</div></div>"
        
    feed_html += "</div></div>"
    st.markdown(clean_html(feed_html), unsafe_allow_html=True)
