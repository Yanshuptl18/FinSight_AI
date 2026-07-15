import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import os
from components.utils import load_css, render_page_header, THEMES
from components.charts import create_kpi_card

load_css()

render_page_header("Sector Correlation Network", "Interactive visualization of inter-sector dependencies, correlations, and supply-chain linkages.")

# --- Mock Data ---
all_sectors = [
    ("Technology", "#4da6ff", 45),
    ("Financials", "#ff9900", 40),
    ("Healthcare", "#00e676", 38),
    ("Consumer Discretionary", "#b388ff", 35),
    ("Energy", "#ff5252", 35),
    ("Materials", "#ff7043", 30),
    ("Industrials", "#9e9e9e", 35),
    ("Real Estate", "#00e5ff", 30),
    ("Utilities", "#ffee58", 25)
]

# Source, Target, Title, Correlation Weight (0-100)
all_edges = [
    ("Technology", "Financials", "FinTech Integration", 85),
    ("Technology", "Consumer Discretionary", "E-commerce Tech", 90),
    ("Healthcare", "Technology", "BioTech / HealthTech", 75),
    ("Energy", "Industrials", "Power & Fuel Supply", 88),
    ("Materials", "Industrials", "Raw Materials", 92),
    ("Financials", "Real Estate", "Mortgage & Lending", 86),
    ("Utilities", "Energy", "Power Grid Operations", 80),
    ("Utilities", "Real Estate", "Infrastructure", 65),
    ("Consumer Discretionary", "Industrials", "Manufacturing", 70),
    ("Healthcare", "Consumer Discretionary", "Consumer Health", 55),
    ("Financials", "Industrials", "CapEx Financing", 60)
]

# --- KPI Section ---
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    create_kpi_card("Total Sectors", str(len(all_sectors)), "Global Markets", "normal")
with kpi2:
    create_kpi_card("Strongest Link", "Materials ↔ Industrials", "92% Correlation", "inverse")
with kpi3:
    avg_corr = sum([e[3] for e in all_edges]) / len(all_edges)
    create_kpi_card("Avg Correlation", f"{avg_corr:.1f}%", "High Dependency", "normal")

st.divider()

# --- Graph Controls ---
col1, col2 = st.columns([1, 3.5])

with col1:
    with st.container(border=True):
        st.markdown("#### Network Settings")
        
        entities = ["All"] + [s[0] for s in sorted(all_sectors, key=lambda x: x[0])]
        selected_sector = st.selectbox("Focus Sector", entities)
        
        min_correlation = st.slider("Min Correlation Threshold", min_value=0, max_value=100, value=50, step=5)
        physics = st.toggle("Enable Physics", value=True)
        
        st.markdown("---")
        
        # Custom Info Card
        info_html = """
        <div class='kpi-card' style='padding: 16px; margin-bottom: 0;'>
            <div style='font-size: 0.95rem; color: #ff9900; font-weight: 700; margin-bottom: 8px;'>Dependency Engine</div>
            <div style='font-size: 0.85rem; color: var(--text-primary); line-height: 1.5;'>
                Linkages are calculated by combining historical price correlations with real-time NLP supply-chain mentions.
            </div>
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        with st.spinner("Generating Sector Network..."):
            
            # Apply Filters
            display_nodes = set()
            display_edges = []
            
            for src, dst, title, weight in all_edges:
                if weight >= min_correlation:
                    if selected_sector == "All" or src == selected_sector or dst == selected_sector:
                        display_edges.append((src, dst, title, weight))
                        display_nodes.add(src)
                        display_nodes.add(dst)
            
            final_nodes = [s for s in all_sectors if s[0] in display_nodes]
            
            # If everything was filtered out
            if not final_nodes:
                st.warning("No connections match your current filter settings.")
            else:
                # Use theme-aware background and text colors
                _theme = THEMES.get(st.session_state.get('active_theme', 'Dark Cyan'), THEMES['Dark Cyan'])
                _bg = _theme['--bg-secondary']
                _font = _theme['--text-primary']
                net = Network(height="650px", width="100%", bgcolor=_bg, font_color=_font)
                
                if physics:
                    net.barnes_hut(gravity=-5000, central_gravity=0.15, spring_length=200)
                
                for s_id, s_color, s_size in final_nodes:
                    net.add_node(s_id, label=s_id, title=s_id, color=s_color, size=s_size)
                    
                for src, dst, title, weight in display_edges:
                    # Map weight to line thickness (1 to 5)
                    thickness = max(1, (weight - 40) / 10)
                    net.add_edge(src, dst, title=f"{title}<br>Correlation: {weight}%", value=thickness, color=_theme['--border-color'])
                    
                path = "html_files"
                if not os.path.exists(path):
                    os.makedirs(path)
                    
                net.save_graph(f"{path}/sector_network.html")
                
                HtmlFile = open(f"{path}/sector_network.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read()
                components.html(source_code, height=670, scrolling=False)
