import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import os
import pandas as pd
from components.utils import load_css, render_page_header, THEMES
from components.charts import create_kpi_card
from data_loader.loader import load_news_data

load_css()
render_page_header("Sector Correlation Network", "Interactive visualization of inter-sector dependencies based on real-time news volume correlation.")

news_df = load_news_data()

if news_df.empty or 'Sector' not in news_df.columns:
    st.warning("No sector data available.")
    st.stop()

# Compute Daily Volume per Sector
pivot = pd.pivot_table(news_df, index=news_df['Date'].dt.date, columns='Sector', aggfunc='size', fill_value=0)

# Compute Correlation Matrix
corr_matrix = pivot.corr()

all_sectors = []
sector_colors = ['#4da6ff', '#ff9900', '#00e676', '#b388ff', '#ff5252', '#ff7043', '#9e9e9e', '#00e5ff']
sectors_list = list(corr_matrix.columns)

for i, sector in enumerate(sectors_list):
    color = sector_colors[i % len(sector_colors)]
    # Node size based on total news volume
    vol = pivot[sector].sum()
    size = max(20, min(60, vol / 10))
    all_sectors.append((sector, color, size))

all_edges = []
for i in range(len(sectors_list)):
    for j in range(i + 1, len(sectors_list)):
        src = sectors_list[i]
        dst = sectors_list[j]
        corr = corr_matrix.iloc[i, j]
        if pd.notna(corr) and corr > 0: # Only positive correlations
            weight = int(corr * 100)
            all_edges.append((src, dst, "Correlated Activity", weight))

# --- KPI Container ---
kpi_container = st.container()

st.divider()

# --- Graph Controls ---
col1, col2 = st.columns([1, 3.5])

with col1:
    with st.container(border=True):
        st.markdown("#### Network Settings")
        
        entities = ["All"] + sorted([s[0] for s in all_sectors])
        selected_sector = st.selectbox("Focus Sector", entities)
        
        min_correlation = st.slider("Min Correlation Threshold", min_value=0, max_value=100, value=20, step=5)
        physics = st.toggle("Enable Physics", value=True)
        
        st.markdown("---")
        
        # Custom Info Card
        info_html = """
        <div class='kpi-card' style='padding: 16px; margin-bottom: 0;'>
            <div style='font-size: 0.95rem; color: #ff9900; font-weight: 700; margin-bottom: 8px;'>Dependency Engine</div>
            <div style='font-size: 0.85rem; color: var(--text-primary); line-height: 1.5;'>
                Linkages are calculated by measuring the Pearson correlation coefficient of daily news volume between sectors.
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
            
            # --- Dynamic KPI Rendering ---
            with kpi_container:
                kpi1, kpi2, kpi3 = st.columns(3)
                with kpi1:
                    create_kpi_card("Total Sectors", str(len(final_nodes)), "Global Markets", "normal")
                with kpi2:
                    if display_edges:
                        top_edge = max(display_edges, key=lambda x: x[3])
                        create_kpi_card("Strongest Link", f"{top_edge[0]} ↔ {top_edge[1]}", f"{top_edge[3]}% Correlation", "inverse")
                    else:
                        create_kpi_card("Strongest Link", "N/A", "N/A", "normal")
                with kpi3:
                    if display_edges:
                        avg_corr = sum([e[3] for e in display_edges]) / max(1, len(display_edges))
                        create_kpi_card("Avg Correlation", f"{avg_corr:.1f}%", "Market Dependency", "normal")
                    else:
                        create_kpi_card("Avg Correlation", "N/A", "Market Dependency", "normal")
                        
            
            # If everything was filtered out
            if not final_nodes:
                st.warning("No connections match your current filter settings.")
            else:
                _theme = THEMES.get(st.session_state.get('active_theme', 'Dark Cyan'), THEMES['Dark Cyan'])
                _bg = _theme['--bg-secondary']
                _font = _theme['--text-primary']
                net = Network(height="650px", width="100%", bgcolor=_bg, font_color=_font)
                
                if physics:
                    net.barnes_hut(gravity=-5000, central_gravity=0.15, spring_length=200)
                
                for s_id, s_color, s_size in final_nodes:
                    net.add_node(s_id, label=s_id, title=s_id, color=s_color, size=s_size)
                    
                for src, dst, title, weight in display_edges:
                    thickness = max(1, (weight - 20) / 10)
                    net.add_edge(src, dst, title=f"{title}<br>Correlation: {weight}%", value=thickness, color=_theme['--border-color'])
                    
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
