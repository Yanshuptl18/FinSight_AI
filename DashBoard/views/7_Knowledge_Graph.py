import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import os
from components.utils import load_css, render_page_header, THEMES
from components.charts import create_kpi_card

load_css()

render_page_header("AI Knowledge Graph Explorer", "Interactive entity network demonstrating relationships between Companies, Sectors, Topics, and Events.")

# --- Mock Data ---
# Expanded for a more realistic graph
all_nodes = [
    ("Apple", "Company", "#4da6ff"),
    ("Microsoft", "Company", "#4da6ff"),
    ("NVIDIA", "Company", "#4da6ff"),
    ("Tesla", "Company", "#4da6ff"),
    ("Google", "Company", "#4da6ff"),
    
    ("Technology", "Sector", "#00e676"),
    ("Automotive", "Sector", "#00e676"),
    
    ("AI Innovation", "Topic", "#ff9900"),
    ("Semiconductors", "Topic", "#ff9900"),
    ("EV Market", "Topic", "#ff9900"),
    
    ("Fed Meeting", "Event", "#ff4d4d"),
    ("Earnings Call", "Event", "#ff4d4d")
]

all_edges = [
    ("Apple", "Technology", "Sector"),
    ("Microsoft", "Technology", "Sector"),
    ("NVIDIA", "Technology", "Sector"),
    ("Tesla", "Automotive", "Sector"),
    ("Google", "Technology", "Sector"),
    
    ("Microsoft", "AI Innovation", "Mentions"),
    ("Google", "AI Innovation", "Mentions"),
    ("NVIDIA", "AI Innovation", "Drives"),
    ("NVIDIA", "Semiconductors", "Leader"),
    ("Apple", "Semiconductors", "Buyer"),
    
    ("Tesla", "EV Market", "Leader"),
    ("Apple", "EV Market", "Rumor"),
    
    ("Technology", "Fed Meeting", "Impacted By"),
    ("Automotive", "Fed Meeting", "Impacted By"),
    
    ("NVIDIA", "Earnings Call", "Scheduled"),
    ("Tesla", "Earnings Call", "Scheduled")
]

# --- KPI Section ---
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    create_kpi_card("Total Entities", str(len(all_nodes)), "+2 Today", "normal")
with kpi2:
    create_kpi_card("Relationships Extracted", str(len(all_edges)), "Real-time", "normal")
with kpi3:
    density = round(len(all_edges) / (len(all_nodes) * (len(all_nodes)-1)) * 100, 1)
    create_kpi_card("Network Density", f"{density}%", "High Connectivity", "normal")

st.divider()

# --- Graph Controls ---
col1, col2 = st.columns([1, 3.5])

with col1:
    with st.container(border=True):
        st.markdown("#### Graph Settings")
        
        entities = ["All"] + [n[0] for n in sorted(all_nodes, key=lambda x: x[0])]
        selected_node = st.selectbox("Focus Entity", entities)
        
        physics = st.toggle("Enable Physics", value=True)
        
        st.markdown("---")
        
        # Custom Info Card
        info_html = """
        <div class='kpi-card' style='padding: 16px; margin-bottom: 0;'>
            <div style='font-size: 0.95rem; color: var(--accent); font-weight: 700; margin-bottom: 8px;'>NLP Engine</div>
            <div style='font-size: 0.85rem; color: var(--text-primary); line-height: 1.5;'>
                The Knowledge Graph connects entities automatically extracted via the FinSight NLP Pipeline in real-time.
            </div>
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        with st.spinner("Generating Knowledge Graph..."):
            
            # Filter nodes and edges if a specific entity is selected
            display_nodes = set()
            display_edges = []
            
            if selected_node != "All":
                display_nodes.add(selected_node)
                for src, dst, title in all_edges:
                    if src == selected_node or dst == selected_node:
                        display_edges.append((src, dst, title))
                        display_nodes.add(src)
                        display_nodes.add(dst)
                
                # Filter full node list down to just the ones connected
                final_nodes = [n for n in all_nodes if n[0] in display_nodes]
            else:
                final_nodes = all_nodes
                display_edges = all_edges
                
            # Use theme-aware background and text colors
            _theme = THEMES.get(st.session_state.get('active_theme', 'Dark Cyan'), THEMES['Dark Cyan'])
            _bg = _theme['--bg-secondary']
            _font = _theme['--text-primary']
            net = Network(height="650px", width="100%", bgcolor=_bg, font_color=_font)
            
            if physics:
                net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=150)
            
            for n_id, n_group, n_color in final_nodes:
                net.add_node(n_id, label=n_id, title=n_group, color=n_color, size=25)
                
            for src, dst, title in display_edges:
                net.add_edge(src, dst, title=title, color=_theme['--border-color'])
                
            path = "html_files"
            if not os.path.exists(path):
                os.makedirs(path)
                
            net.save_graph(f"{path}/knowledge_graph.html")
            
            HtmlFile = open(f"{path}/knowledge_graph.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, height=670, scrolling=False)
