import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import os
import pandas as pd
from collections import Counter
from components.utils import load_css, render_page_header, THEMES
from components.charts import create_kpi_card
from data_loader.loader import DATA_PATH, ensure_file

load_css()
render_page_header("Company Ecosystem Network", "Interactive visualization of supply chains, competitors, and strategic partnerships across all tracked corporate entities.")

# Load full precomputed network dataset
ensure_file("company_network_edges.parquet")
edge_file = os.path.join(DATA_PATH, "company_network_edges.parquet")
if os.path.exists(edge_file):
    full_edge_df = pd.read_parquet(edge_file)
else:
    st.warning("Company network data is currently processing.")
    st.stop()


# Compute Global Dataset Metrics across all 186k+ edges & 75k+ entities
global_all_nodes = set(full_edge_df['ticker']).union(set(full_edge_df['entity']))
total_global_entities = len(global_all_nodes)
all_connected_global = list(full_edge_df['ticker']) + list(full_edge_df['entity'])
top_global_org, node_link_count = Counter(all_connected_global).most_common(1)[0]
top_global_rel = full_edge_df['relation'].value_counts().index[0]
global_rel_count = full_edge_df['relation'].value_counts().iloc[0]

# --- Dynamic KPI Container ---
kpi_container = st.container()

st.divider()

# --- Graph Controls ---
col1, col2 = st.columns([1, 3.5])

with col1:
    with st.container(border=True):
        st.markdown("#### Ecosystem Filters")
        
        # Complete list of 75k+ entities available for search & focus
        entities_list = ["All"] + sorted(list(global_all_nodes))
        selected_node = st.selectbox("Focus Company / Entity", entities_list)
        
        relation_types = ["All", "Supplier / Hardware", "Competitor / Rival", "Partner", "Co-mentioned"]
        selected_rel = st.selectbox("Relation Type", relation_types)
        
        physics = st.toggle("Enable Physics Simulation", value=True)
        
        st.markdown("---")
        
        info_html = """
        <div class='kpi-card' style='padding: 16px; margin-bottom: 0;'>
            <div style='font-size: 0.95rem; color: #ff5252; font-weight: 700; margin-bottom: 8px;'>Supply Chain NLP</div>
            <div style='font-size: 0.85rem; color: var(--text-primary); line-height: 1.5;'>
                Company links are dynamically identified by parsing 10-K filings, earnings calls, and global news intelligence.
            </div>
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        with st.spinner("Generating Company Ecosystem Network..."):
            
            # Filter edges based on selection
            df_filtered = full_edge_df.copy()
            
            if selected_rel != "All":
                df_filtered = df_filtered[df_filtered['relation'] == selected_rel]
                
            if selected_node != "All":
                df_filtered = df_filtered[(df_filtered['ticker'] == selected_node) | (df_filtered['entity'] == selected_node)]
            else:
                # When "All" is selected, prioritize specific supply-chain / partnership relations & top weighted co-mentions
                specific = df_filtered[df_filtered['relation'] != 'Co-mentioned'].sort_values(by='weight', ascending=False).head(200)
                coment = df_filtered[df_filtered['relation'] == 'Co-mentioned'].sort_values(by='weight', ascending=False).head(150)
                df_filtered = pd.concat([specific, coment]).drop_duplicates()
                
            # Build node dictionary and edge list for rendering
            nodes_dict = {}
            display_edges = []
            
            for _, row in df_filtered.iterrows():
                ticker = str(row['ticker'])
                entity = str(row['entity'])
                relation = str(row['relation'])
                weight = int(row['weight'])
                
                if ticker == entity:
                    continue
                    
                if ticker not in nodes_dict:
                    nodes_dict[ticker] = (ticker, "#4da6ff", 40, "Core Company")
                if entity not in nodes_dict:
                    nodes_dict[entity] = (entity, "#00e676", 30, "Ecosystem Entity")
                    
                color = "#4da6ff"
                if relation == "Supplier / Hardware":
                    color = "#ff9900"
                elif relation == "Competitor / Rival":
                    color = "#ff5252"
                elif relation == "Partner":
                    color = "#b388ff"
                    
                display_edges.append((ticker, entity, f"{relation} ({weight} refs)", color, relation))
                
            final_nodes = list(nodes_dict.values())
            
            # --- Dynamic KPI Rendering ---
            with kpi_container:
                k1, k2, k3 = st.columns(3)
                
                with k1:
                    if selected_node == "All" and selected_rel == "All":
                        create_kpi_card("Entities Tracked", f"{total_global_entities:,}", "Global Coverage", "normal")
                    else:
                        create_kpi_card("Entities Tracked", f"{len(final_nodes):,}", "Filtered Coverage", "normal")
                        
                with k2:
                    if selected_node == "All" and selected_rel == "All":
                        create_kpi_card("Most Connected Org", str(top_global_org), f"{node_link_count:,} Links", "normal")
                    elif display_edges:
                        all_conn = [src for src, dst, _, _, _ in display_edges] + [dst for src, dst, _, _, _ in display_edges]
                        top_node, n_count = Counter(all_conn).most_common(1)[0]
                        create_kpi_card("Most Connected Org", str(top_node), f"{n_count:,} Links", "normal")
                    else:
                        create_kpi_card("Most Connected Org", "N/A", "0 Links", "normal")
                        
                with k3:
                    if selected_node == "All" and selected_rel == "All":
                        create_kpi_card("Dominant Relation", str(top_global_rel), f"{global_rel_count:,} Edges", "inverse")
                    elif display_edges:
                        rel_counts = Counter([rel for _, _, _, _, rel in display_edges])
                        top_r, r_count = rel_counts.most_common(1)[0]
                        create_kpi_card("Dominant Relation", str(top_r), f"{r_count:,} Edges", "inverse")
                    else:
                        create_kpi_card("Dominant Relation", "N/A", "0 Edges", "inverse")

            if not final_nodes:
                st.warning("No connections match your current filter settings.")
            else:
                _theme = THEMES.get(st.session_state.get('active_theme', 'Dark Cyan'), THEMES['Dark Cyan'])
                net = Network(height="650px", width="100%", bgcolor=_theme['--bg-secondary'], font_color=_theme['--text-primary'])
                
                if physics:
                    net.barnes_hut(gravity=-6000, central_gravity=0.2, spring_length=200)
                
                added_nodes = set()
                for n_id, n_color, n_size, n_type in final_nodes:
                    net.add_node(n_id, label=str(n_id), title=f"{n_type}: {n_id}", color=n_color, size=n_size)
                    added_nodes.add(n_id)
                    
                for src, dst, title, color, rel_type in display_edges:
                    if src not in added_nodes:
                        net.add_node(src, label=str(src), title=str(src), color="#4da6ff", size=30)
                        added_nodes.add(src)
                    if dst not in added_nodes:
                        net.add_node(dst, label=str(dst), title=str(dst), color="#00e676", size=30)
                        added_nodes.add(dst)

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
                    import warnings
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        components.html(source_code, height=670, scrolling=False)
