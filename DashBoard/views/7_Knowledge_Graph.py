import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import os
import pandas as pd
from components.utils import load_css, render_page_header, THEMES
from components.charts import create_kpi_card
from data_loader.loader import load_kg_nodes, load_kg_edges, load_kg_metrics

load_css()
render_page_header("AI Knowledge Graph Explorer", "Interactive entity network demonstrating relationships between Companies, Publishers, Topics, and Events.")

# Load Real KG Data
nodes_df = load_kg_nodes()
edges_df = load_kg_edges()
metrics_df = load_kg_metrics()

if nodes_df.empty or edges_df.empty:
    st.warning("Knowledge Graph data is loading or unavailable. Please wait.")
    st.stop()

# --- KPI Section ---
metrics_dict = dict(zip(metrics_df['Metric'], metrics_df['Value'])) if not metrics_df.empty else {}
total_nodes = metrics_dict.get('Total Nodes', len(nodes_df))
total_edges = metrics_dict.get('Total Edges', len(edges_df))
density = metrics_dict.get('Network Density', round(len(edges_df) / (max(1, len(nodes_df) * (len(nodes_df)-1))) * 100, 4))

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    create_kpi_card("Total Nodes", f"{int(total_nodes):,}", "Discovered Entities", "normal")
with kpi2:
    create_kpi_card("Relationships Extracted", f"{int(total_edges):,}", "Strong Links", "normal")
with kpi3:
    create_kpi_card("Network Density", f"{density}%", "Connectivity", "normal")

st.divider()

# --- Graph Controls ---
col1, col2 = st.columns([1, 3.5])

with col1:
    with st.container(border=True):
        st.markdown("#### Graph Settings")
        
        cluster_mapping = {
            "CLUSTER_0": "Technology & Software",
            "CLUSTER_1": "Healthcare & Biotech",
            "CLUSTER_2": "Financial Services",
            "CLUSTER_3": "Consumer Goods",
            "CLUSTER_4": "Energy & Utilities",
            "CLUSTER_5": "Industrial & Manufacturing",
            "CLUSTER_6": "Real Estate",
            "CLUSTER_7": "Telecommunications",
            "CLUSTER_8": "Basic Materials",
            "CLUSTER_9": "Consumer Services",
            "CLUSTER_10": "Transportation",
            "CLUSTER_11": "Miscellaneous / Other"
        }
        
        def format_label(row):
            nid = str(row['node_id'])
            dl = str(row['display_label']) if pd.notna(row['display_label']) else nid
            
            if nid.startswith('CLUSTER_'):
                return cluster_mapping.get(nid, f"{dl}")
            return dl

        nodes_df['dropdown_label'] = nodes_df.apply(format_label, axis=1)
        
        # Categorize nodes
        sectors = nodes_df[nodes_df['node_id'].str.startswith('CLUSTER_')]
        companies = nodes_df[nodes_df['node_id'].str.startswith('COMP_')]
        publishers = nodes_df[nodes_df['node_id'].str.startswith('PUB_')]
        events = nodes_df[nodes_df['node_id'].str.startswith('EVENT_')]
        
        def get_options_map(df):
            return {row['dropdown_label']: row['node_id'] for _, row in df.iterrows()}
            
        sector_opts = get_options_map(sectors)
        company_opts = get_options_map(companies)
        pub_opts = get_options_map(publishers)
        event_opts = get_options_map(events)
        
        selected_nodes = []
        
        st.caption("Leave filters blank to show ALL nodes.")
        
        sel_sectors = st.multiselect("Filter Sectors", sorted(sector_opts.keys()))
        selected_nodes.extend([sector_opts[k] for k in sel_sectors])
        
        sel_companies = st.multiselect("Filter Companies", sorted(company_opts.keys()))
        selected_nodes.extend([company_opts[k] for k in sel_companies])
        
        sel_pubs = st.multiselect("Filter Publishers", sorted(pub_opts.keys()))
        selected_nodes.extend([pub_opts[k] for k in sel_pubs])
        
        sel_events = st.multiselect("Filter Events", sorted(event_opts.keys()))
        selected_nodes.extend([event_opts[k] for k in sel_events])
        
        active_filters = sum(1 for f in [sel_sectors, sel_companies, sel_pubs, sel_events] if len(f) > 0)
        
        st.markdown("---")
        physics = st.toggle("Enable Physics", value=True)
        
        st.markdown("---")
        
        # Custom Info Card
        info_html = """
        <div class='kpi-card' style='padding: 16px; margin-bottom: 0;'>
            <div style='font-size: 0.95rem; color: var(--accent); font-weight: 700; margin-bottom: 8px;'>AI Connectivity Engine</div>
            <div style='font-size: 0.85rem; color: var(--text-primary); line-height: 1.5;'>
                The Knowledge Graph maps actual relationships extracted natively via the FinSight LLM Pipeline. Edges signify real co-occurrences.
            </div>
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        # Top-right style legend
        legend_html = """
        <div style="display: flex; justify-content: flex-end; gap: 15px; margin-bottom: 10px; font-size: 0.85rem; font-weight: 600;">
            <span style="color: #4da6ff;">● Company</span>
            <span style="color: #ff9900;">● Publisher</span>
            <span style="color: #ff5252;">● Event</span>
            <span style="color: #b388ff;">● Sector (Cluster)</span>
        </div>
        """
        st.markdown(legend_html, unsafe_allow_html=True)
        
        with st.spinner("Generating Knowledge Graph..."):
            
            # Filter edges based on selection to avoid massive overload
            display_edges = edges_df.copy()
            if selected_nodes:
                if active_filters > 1:
                    display_edges = display_edges[
                        (display_edges['source'].isin(selected_nodes)) & 
                        (display_edges['target'].isin(selected_nodes))
                    ]
                else:
                    display_edges = display_edges[
                        (display_edges['source'].isin(selected_nodes)) | 
                        (display_edges['target'].isin(selected_nodes))
                    ]
            else:
                # If 'All', limit to the top 200 edges by weight to keep rendering fast
                if 'weight' in display_edges.columns:
                    display_edges = display_edges.sort_values(by='weight', ascending=False).head(200)
                else:
                    display_edges = display_edges.head(200)
                    
            # Get valid nodes present in the filtered edges
            valid_node_ids = set(display_edges['source'].unique()).union(set(display_edges['target'].unique()))
            
            if selected_nodes:
                valid_node_ids.update(selected_nodes)
                
            display_nodes = nodes_df[nodes_df['node_id'].isin(valid_node_ids)]
                
            # Use theme-aware background and text colors
            _theme = THEMES.get(st.session_state.get('active_theme', 'Dark Cyan'), THEMES['Dark Cyan'])
            _bg = _theme['--bg-secondary']
            _font = _theme['--text-primary']
            net = Network(height="650px", width="100%", bgcolor=_bg, font_color=_font)
            
            if physics:
                net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=150)
            
# Color mapping for entity types
            label_colors = {
                'Company': '#4da6ff',
                'Publisher': '#ff9900',
                'Event': '#ff5252',
                'Topic': '#00e676',
                'Cluster': '#b388ff',
                'ENTITY_PERSON': '#b388ff',
                'ENTITY_GPE': '#00e5ff',
                'ENTITY_ORG': '#ff4d4d'
            }
            
            # Map node attributes
            # PyVis nodes
            for _, row in display_nodes.iterrows():
                n_id = row['node_id']
                n_type = row.get('node_type', 'Unknown')
                n_label = str(row.get('dropdown_label', row.get('display_label', n_id)))
                n_color = label_colors.get(n_type, '#9e9e9e')
                n_size = 40 if n_type == 'Company' else 25
                
                # Make the selected focus node larger
                if n_id in selected_nodes:
                    n_size = 60
                    
                n_title = f"{n_label} ({n_type})"
                net.add_node(n_id, label=n_label, title=n_title, color=n_color, size=n_size)
                
            for _, row in display_edges.iterrows():
                src = row['source']
                dst = row['target']
                title = row.get('relation', '')
                weight = row.get('weight', 1.0)
                
                # PyVis needs nodes to exist before adding edges
                if src in valid_node_ids and dst in valid_node_ids:
                    net.add_edge(src, dst, title=title, value=weight, color=_theme['--border-color'])
                
            path = "html_files"
            if not os.path.exists(path):
                os.makedirs(path)
                
            net.save_graph(f"{path}/knowledge_graph.html")
            
            with open(f"{path}/knowledge_graph.html", 'r', encoding='utf-8') as HtmlFile:
                source_code = HtmlFile.read()
                # Use components.html, warnings are fine unless we can disable them
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    components.html(source_code, height=670, scrolling=False)
