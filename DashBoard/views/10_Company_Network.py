import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import os
import pandas as pd
from components.utils import load_css, render_page_header, THEMES
from components.charts import create_kpi_card
from data_loader.loader import DATA_PATH

load_css()
render_page_header("Company Ecosystem Network", "Interactive visualization of supply chains, competitors, and strategic partnerships.")

# Load precomputed edges directly instead of computing on 7.3M rows
edge_file = os.path.join(DATA_PATH, "company_network_edges.parquet")
if os.path.exists(edge_file):
    edge_counts = pd.read_parquet(edge_file)
else:
    st.warning("Company network data is currently processing.")
    st.stop()

# Ensure we get a good mix of relations, not just the massive 'Co-mentioned'
specific = edge_counts[edge_counts['relation'] != 'Co-mentioned'].sort_values(by='weight', ascending=False).head(150)
coment = edge_counts[edge_counts['relation'] == 'Co-mentioned'].sort_values(by='weight', ascending=False).head(100)
edge_counts = pd.concat([specific, coment])

all_nodes_dict = {}
all_edges = []

for _, row in edge_counts.iterrows():
    ticker = row['ticker']
    entity = row['entity']
    relation = row['relation']
    weight = row['weight']
    
    if ticker == entity:
        continue # skip self loops
    
    if ticker not in all_nodes_dict:
        all_nodes_dict[ticker] = (ticker, "#4da6ff", 40, "Core Company")
    if entity not in all_nodes_dict:
        all_nodes_dict[entity] = (entity, "#00e676", 30, "Ecosystem Org")
        
    color = "#4da6ff"
    if relation == "Supplier / Hardware":
        color = "#ff9900"
    elif relation == "Competitor / Rival":
        color = "#ff5252"
    elif relation == "Partner":
        color = "#b388ff"
        
    all_edges.append((ticker, entity, f"{relation} ({weight} refs)", color, relation))

all_nodes = list(all_nodes_dict.values())

# --- KPI Container ---
kpi_container = st.container()

st.divider()

# --- Graph Controls ---
col1, col2 = st.columns([1, 3.5])

with col1:
    with st.container(border=True):
        st.markdown("#### Ecosystem Filters")
        
        entities_list = ["All"] + sorted(list(all_nodes_dict.keys()))
        selected_node = st.selectbox("Focus Company", entities_list)
        
        relation_types = ["All", "Supplier / Hardware", "Competitor / Rival", "Partner", "Co-mentioned"]
        selected_rel = st.selectbox("Relation Type", relation_types)
        
        physics = st.toggle("Enable Physics", value=True)
        
        st.markdown("---")
        
        info_html = """
        <div class='kpi-card' style='padding: 16px; margin-bottom: 0;'>
            <div style='font-size: 0.95rem; color: #ff5252; font-weight: 700; margin-bottom: 8px;'>Supply Chain NLP</div>
            <div style='font-size: 0.85rem; color: var(--text-primary); line-height: 1.5;'>
                Company links are dynamically identified through parsing 10-K filings, earnings calls, and news intelligence.
            </div>
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        with st.spinner("Generating Company Ecosystem..."):
            
            display_nodes = set()
            display_edges = []
            
            for src, dst, title, color, rel_type in all_edges:
                if selected_rel != "All" and selected_rel != rel_type:
                    continue
                    
                if selected_node == "All" or src == selected_node or dst == selected_node:
                    display_edges.append((src, dst, title, color, rel_type))
                    display_nodes.add(src)
                    display_nodes.add(dst)
            
            final_nodes = [n for n in all_nodes if n[0] in display_nodes]
            
            # --- Dynamic KPI Rendering ---
            with kpi_container:
                kpi1, kpi2, kpi3 = st.columns(3)
                with kpi1:
                    create_kpi_card("Entities Tracked", str(len(final_nodes)), "Global Coverage", "normal")
                with kpi2:
                    if display_edges:
                        from collections import Counter
                        all_connected = [src for src, dst, _, _, _ in display_edges] + [dst for src, dst, _, _, _ in display_edges]
                        top_node, node_count = Counter(all_connected).most_common(1)[0]
                        create_kpi_card("Most Connected Org", top_node, f"{node_count} Links", "normal")
                    else:
                        create_kpi_card("Most Connected Org", "N/A", "N/A", "normal")
                with kpi3:
                    if display_edges:
                        rel_counts = Counter([rel for _, _, _, _, rel in display_edges])
                        top_rel, rel_count = rel_counts.most_common(1)[0]
                        create_kpi_card("Dominant Relation", top_rel, f"{rel_count} Edges", "inverse")
                    else:
                        create_kpi_card("Dominant Relation", "N/A", "N/A", "inverse")
            
            if not final_nodes:
                st.warning("No connections match your current filter settings.")
            else:
                _theme = THEMES.get(st.session_state.get('active_theme', 'Dark Cyan'), THEMES['Dark Cyan'])
                net = Network(height="650px", width="100%", bgcolor=_theme['--bg-secondary'], font_color=_theme['--text-primary'])
                
                if physics:
                    net.barnes_hut(gravity=-6000, central_gravity=0.2, spring_length=200)
                
                for n_id, n_color, n_size, n_type in final_nodes:
                    net.add_node(n_id, label=str(n_id), title=n_type, color=n_color, size=n_size)
                    
                for src, dst, title, color, rel_type in display_edges:
                    if color.startswith("#"):
                        h = color.lstrip('#')
                        rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                        color = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.5)"
                    net.add_edge(src, dst, title=title, color=color)
                    
                path = "html_files"
                if not os.path.exists(path):
                    os.makedirs(path)
                    
                net.save_graph(f"{path}/company_network.html")
                
                with open(f"{path}/company_network.html", 'r', encoding='utf-8') as HtmlFile:
                    source_code = HtmlFile.read()
                    components.html(source_code, height=670, scrolling=False)
