import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import os
import pandas as pd
import numpy as np
from components.utils import load_css, render_page_header, THEMES
from components.charts import create_kpi_card
from data_loader.loader import load_news_data, load_sector_relationships, load_sector_data

load_css()
render_page_header("Sector Correlation & Relationship Network", "Interactive visualization of inter-sector dependencies across all 28 market sectors based on NLP embeddings, risk similarity, and news correlation.")

sec_df = load_sector_data()
rel_df = load_sector_relationships()
news_df = load_news_data()

if sec_df.empty:
    st.warning("No sector network data available.")
    st.stop()

# Color palette for 28 sectors
palette = [
    '#4da6ff', '#ff9900', '#00e676', '#b388ff', '#ff5252', '#ff7043', '#00e5ff', '#9e9e9e',
    '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#03a9f4', '#00bcd4', '#009688',
    '#4caf50', '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107', '#ff9800', '#ff5722', '#795548'
]

all_sectors = []
sector_node_map = {}

# Build node tuples for ALL 28 sectors
for i, row in sec_df.iterrows():
    sec_name = str(row['Sector'])
    vol = row.get('News Volume', 1000)
    growth = row.get('Growth Score', 50)
    color = palette[i % len(palette)]
    # Node size scaled dynamically by volume/growth
    size = max(22, min(65, int(20 + np.sqrt(vol) / 40)))
    node_tuple = (sec_name, color, size)
    all_sectors.append(node_tuple)
    sector_node_map[sec_name] = row

# Build Edge Relationships across all 28 sectors
all_edges = []
edge_set = set()

# 1. Primary Edges from sector_relationships.parquet
if not rel_df.empty:
    for _, row in rel_df.iterrows():
        s1 = str(row['sector_1'])
        s2 = str(row['sector_2'])
        sim = float(row.get('similarity', 0.5))
        shared = int(row.get('shared_companies', 0))
        weight = int(sim * 100)
        title = f"Similarity: {sim:.4f} | Shared Companies: {shared:,}"
        all_edges.append((s1, s2, title, weight))
        edge_set.add((min(s1, s2), max(s1, s2)))

# 2. Daily News Correlation Edges
if not news_df.empty and 'Sector' in news_df.columns:
    try:
        pivot = pd.pivot_table(news_df, index=news_df['Date'].dt.date, columns='Sector', aggfunc='size', fill_value=0)
        corr_matrix = pivot.corr()
        sectors_list = list(corr_matrix.columns)
        for i in range(len(sectors_list)):
            for j in range(i + 1, len(sectors_list)):
                src = sectors_list[i]
                dst = sectors_list[j]
                pair_key = (min(src, dst), max(src, dst))
                if pair_key not in edge_set:
                    corr = corr_matrix.iloc[i, j]
                    if pd.notna(corr) and corr > 0.15:
                        weight = int(corr * 100)
                        all_edges.append((src, dst, f"News Correlation: {weight}%", weight))
                        edge_set.add(pair_key)
    except Exception as e:
        print(f"Correlation calculation error: {e}")

# 3. Cross-Sector Risk & Growth Similarity Edges for all 28 sectors
sec_names = list(sector_node_map.keys())
for i in range(len(sec_names)):
    for j in range(i + 1, len(sec_names)):
        s1 = sec_names[i]
        s2 = sec_names[j]
        pair_key = (min(s1, s2), max(s1, s2))
        if pair_key not in edge_set:
            r1 = sector_node_map[s1]
            r2 = sector_node_map[s2]
            g_diff = abs(r1.get('Growth Score', 50) - r2.get('Growth Score', 50))
            rk_diff = abs(r1.get('Risk Score', 50) - r2.get('Risk Score', 50))
            sim_score = max(0, 100 - (g_diff * 1.5 + rk_diff * 1.5))
            if sim_score >= 40:
                all_edges.append((s1, s2, f"Profile Similarity: {sim_score:.0f}%", int(sim_score)))
                edge_set.add(pair_key)

# --- Dynamic KPI Container ---
kpi_container = st.container()

st.divider()

# --- Graph Controls ---
col1, col2 = st.columns([1, 3.5])

with col1:
    with st.container(border=True):
        st.markdown("#### Network Settings")
        
        entities = ["All"] + sorted([s[0] for s in all_sectors])
        selected_sector = st.selectbox("Focus Sector", entities)
        
        min_correlation = st.slider("Min Connection Threshold (%)", min_value=0, max_value=100, value=25, step=5)
        physics = st.toggle("Enable Physics Simulation", value=True)
        
        st.markdown("---")
        
        info_html = """
        <div class='kpi-card' style='padding: 16px; margin-bottom: 0;'>
            <div style='font-size: 0.95rem; color: #ff9900; font-weight: 700; margin-bottom: 8px;'>Sector Linkage Engine</div>
            <div style='font-size: 0.85rem; color: var(--text-primary); line-height: 1.5;'>
                Network spans all 28 market sectors derived from shared corporate overlaps, NLP embedding similarity, and temporal activity correlations.
            </div>
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        with st.spinner("Generating Sector Network for All 28 Sectors..."):
            display_nodes = set()
            display_edges = []
            
            for src, dst, title, weight in all_edges:
                if weight >= min_correlation:
                    if selected_sector == "All" or src == selected_sector or dst == selected_sector:
                        display_edges.append((src, dst, title, weight))
                        display_nodes.add(src)
                        display_nodes.add(dst)
            
            # If no edge filter matches, still keep all nodes available
            if selected_sector == "All" and min_correlation <= 40:
                final_nodes = all_sectors
            else:
                final_nodes = [s for s in all_sectors if s[0] in display_nodes or s[0] == selected_sector]
            
            # Dynamic KPIs
            with kpi_container:
                kpi1, kpi2, kpi3 = st.columns(3)
                with kpi1:
                    create_kpi_card("Total Sectors", str(len(all_sectors)), "Global Markets (28 Sectors)", "normal")
                with kpi2:
                    if display_edges:
                        top_edge = max(display_edges, key=lambda x: x[3])
                        create_kpi_card("Strongest Link", f"{top_edge[0]} ↔ {top_edge[1]}", f"Strength: {top_edge[3]}%", "inverse")
                    else:
                        create_kpi_card("Strongest Link", "N/A", "N/A", "normal")
                with kpi3:
                    if display_edges:
                        avg_corr = sum([e[3] for e in display_edges]) / max(1, len(display_edges))
                        create_kpi_card("Avg Link Strength", f"{avg_corr:.1f}%", "Inter-Sector Coupling", "normal")
                    else:
                        create_kpi_card("Avg Link Strength", "N/A", "Inter-Sector Coupling", "normal")

            if not final_nodes:
                st.warning("No connections match your current filter settings.")
            else:
                _theme = THEMES.get(st.session_state.get('active_theme', 'Dark Cyan'), THEMES['Dark Cyan'])
                _bg = _theme['--bg-secondary']
                _font = _theme['--text-primary']
                net = Network(height="650px", width="100%", bgcolor=_bg, font_color=_font)
                
                if physics:
                    net.barnes_hut(gravity=-6000, central_gravity=0.15, spring_length=200)
                
                added_nodes = set()
                for s_id, s_color, s_size in final_nodes:
                    net.add_node(s_id, label=str(s_id), title=str(s_id), color=s_color, size=s_size)
                    added_nodes.add(s_id)
                    
                for src, dst, title, weight in display_edges:
                    if src not in added_nodes:
                        net.add_node(src, label=str(src), title=str(src), color="#9e9e9e", size=25)
                        added_nodes.add(src)
                    if dst not in added_nodes:
                        net.add_node(dst, label=str(dst), title=str(dst), color="#9e9e9e", size=25)
                        added_nodes.add(dst)
                        
                    thickness = max(1, (weight - 10) / 15)
                    net.add_edge(src, dst, title=title, value=thickness, color=_theme['--border-color'])
                    
                path = "html_files"
                if not os.path.exists(path):
                    os.makedirs(path)
                    
                net.save_graph(f"{path}/sector_network.html")
                
                with open(f"{path}/sector_network.html", 'r', encoding='utf-8') as HtmlFile:
                    source_code = HtmlFile.read()
                    import warnings
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        components.html(source_code, height=670, scrolling=False)
