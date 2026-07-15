import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import os
from components.utils import load_css, render_page_header, THEMES
from components.charts import create_kpi_card

load_css()

render_page_header("Company Ecosystem Network", "Interactive visualization of supply chains, competitors, and strategic partnerships.")

# --- Mock Data ---
# Node ID, Color, Size, Type
all_nodes = [
    ("Apple", "#4da6ff", 40, "Tech Giant"),
    ("Microsoft", "#4da6ff", 40, "Tech Giant"),
    ("Google", "#4da6ff", 35, "Tech Giant"),
    ("NVIDIA", "#00e676", 35, "Semiconductor"),
    ("TSMC", "#00e676", 30, "Foundry"),
    ("ASML", "#00e676", 25, "Equipment"),
    ("Qualcomm", "#00e676", 25, "Chip Design"),
    ("Foxconn", "#ff9900", 25, "Manufacturer"),
    ("OpenAI", "#b388ff", 30, "AI Lab"),
    ("Tesla", "#ff5252", 35, "Automaker"),
    ("BYD", "#ff5252", 30, "Automaker"),
    ("Ford", "#ff5252", 25, "Automaker")
]

# Source, Target, Relation, Color
all_edges = [
    ("TSMC", "Apple", "Sole Supplier (3nm)", "#00e676"),
    ("Foxconn", "Apple", "Primary Assembler", "#ff9900"),
    ("Qualcomm", "Apple", "Modem Supplier", "#00e676"),
    
    ("TSMC", "NVIDIA", "Primary Foundry", "#00e676"),
    ("ASML", "TSMC", "Lithography Eqpt.", "#00e676"),
    
    ("NVIDIA", "Microsoft", "AI Hardware", "#00e676"),
    ("OpenAI", "Microsoft", "Strategic Partner", "#b388ff"),
    
    ("NVIDIA", "Tesla", "FSD Hardware", "#00e676"),
    
    ("Apple", "Microsoft", "Fierce Competitor", "#ff5252"),
    ("Google", "Microsoft", "Cloud & AI Rival", "#ff5252"),
    ("Apple", "Google", "Mobile OS Rival", "#ff5252"),
    
    ("Tesla", "BYD", "EV Competitor", "#ff5252"),
    ("Ford", "Tesla", "EV Competitor", "#ff5252"),
    
    ("Google", "OpenAI", "AI Race", "#ff5252")
]

# --- KPI Section ---
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    create_kpi_card("Entities Tracked", str(len(all_nodes)), "Global Coverage", "normal")
with kpi2:
    create_kpi_card("Critical Supplier", "TSMC", "3 Major Clients", "normal")
with kpi3:
    competitions = sum(1 for e in all_edges if "Competitor" in e[2] or "Rival" in e[2] or "Race" in e[2])
    create_kpi_card("Active Rivalries", str(competitions), "High Competition", "inverse")

st.divider()

# --- Graph Controls ---
col1, col2 = st.columns([1, 3.5])

with col1:
    with st.container(border=True):
        st.markdown("#### Ecosystem Filters")
        
        entities = ["All"] + [n[0] for n in sorted(all_nodes, key=lambda x: x[0])]
        selected_node = st.selectbox("Focus Company", entities)
        
        relation_types = ["All", "Supplier / Hardware", "Competitor / Rival", "Partner"]
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
            
            # Apply Filters
            display_nodes = set()
            display_edges = []
            
            for src, dst, title, color in all_edges:
                
                # Filter by relation type
                if selected_rel != "All":
                    is_comp = "Competitor" in title or "Rival" in title or "Race" in title
                    is_supp = "Supplier" in title or "Foundry" in title or "Eqpt." in title or "Hardware" in title or "Assembler" in title
                    is_part = "Partner" in title
                    
                    if selected_rel == "Supplier / Hardware" and not is_supp:
                        continue
                    if selected_rel == "Competitor / Rival" and not is_comp:
                        continue
                    if selected_rel == "Partner" and not is_part:
                        continue
                        
                # Filter by Focus Company
                if selected_node == "All" or src == selected_node or dst == selected_node:
                    display_edges.append((src, dst, title, color))
                    display_nodes.add(src)
                    display_nodes.add(dst)
            
            final_nodes = [n for n in all_nodes if n[0] in display_nodes]
            
            if not final_nodes:
                st.warning("No connections match your current filter settings.")
            else:
                _theme = THEMES.get(st.session_state.get('active_theme', 'Dark Cyan'), THEMES['Dark Cyan'])
                net = Network(height="650px", width="100%", bgcolor=_theme['--bg-secondary'], font_color=_theme['--text-primary'])
                
                if physics:
                    net.barnes_hut(gravity=-6000, central_gravity=0.2, spring_length=200)
                
                for n_id, n_color, n_size, n_type in final_nodes:
                    net.add_node(n_id, label=n_id, title=n_type, color=n_color, size=n_size)
                    
                for src, dst, title, color in display_edges:
                    # Make lines slightly transparent for a sleek look
                    if color.startswith("#"):
                        # Convert hex to rgba string
                        h = color.lstrip('#')
                        rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                        color = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.5)"
                    net.add_edge(src, dst, title=title, color=color)
                    
                path = "html_files"
                if not os.path.exists(path):
                    os.makedirs(path)
                    
                net.save_graph(f"{path}/company_network.html")
                
                HtmlFile = open(f"{path}/company_network.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read()
                components.html(source_code, height=670, scrolling=False)
