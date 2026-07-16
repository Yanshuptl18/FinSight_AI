import streamlit as st
from components.charts import render_plotly_chart
import pandas as pd
import plotly.graph_objects as go
import random
from components.utils import load_css, render_page_header, THEMES
from components.charts import create_kpi_card
from data_loader.loader import load_event_influence, load_event_propagation_paths, load_propagation_risk

load_css()

render_page_header("Event Propagation Explorer", "Visualize how specific events cascade across sectors, industries, and companies based on AI-generated causal chains.")

influence_df = load_event_influence()
paths_df = load_event_propagation_paths()
risk_df = load_propagation_risk()

if influence_df.empty or paths_df.empty:
    st.warning("Event data is currently loading or unavailable. Please check data sources.")
    st.stop()

# --- Filters Section ---
with st.container(border=True):
    st.markdown("#### Event Selection")
    
    # Sort events by influence score to show the most impactful ones first
    if 'influence_score' in influence_df.columns:
        influence_df = influence_df.sort_values(by='influence_score', ascending=False)
        
    events_list = influence_df['final_event'].dropna().unique().tolist()
    if not events_list:
        events_list = ["No Events Found"]
        
    selected_event = st.selectbox("Select Event Origin to trace its propagation path:", events_list)

st.divider()

# Get metrics for the selected event
event_metrics = influence_df[influence_df['final_event'] == selected_event]
if not event_metrics.empty:
    event_metrics = event_metrics.iloc[0]
else:
    event_metrics = pd.Series({'total_news': 0, 'companies': 0, 'impact_category': 'Unknown', 'influence_score': 0})

event_risk = risk_df[risk_df['final_event'] == selected_event]
if not event_risk.empty:
    prop_risk = int(event_risk.iloc[0].get('propagation_risk', 0))
else:
    prop_risk = 0

# --- KPI Section ---
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    create_kpi_card("Impacted Companies", f"{int(event_metrics.get('companies', 0)):,}", "Directly Exposed", "normal")
with kpi2:
    create_kpi_card("Influence Score", f"{event_metrics.get('influence_score', 0):.1f}/100", f"Category: {event_metrics.get('impact_category', 'Unknown')}", "inverse")
with kpi3:
    create_kpi_card("Propagation Risk", f"{prop_risk}%", "Contagion Probability", "normal")

st.divider()

# --- Propagation Chart ---
with st.container(border=True):
    st.markdown(f"### Propagation Ripple Effect: {selected_event}")
    
    # Filter paths originating from the selected event
    event_paths = paths_df[paths_df['source_event'] == selected_event]
    
    if event_paths.empty:
        st.info("No propagation paths discovered for this event.")
    else:
        # Build the graph (nodes and edges)
        nodes = []
        edges = {} # (source, target): weight
        
        for _, row in event_paths.iterrows():
            path_str = row['path']
            if pd.isna(path_str):
                continue
            
            # Paths look like: "Analyst Rating --> Layoffs --> Bankruptcy"
            steps = [s.strip() for s in str(path_str).split("-->")]
            
            for i in range(len(steps) - 1):
                src = steps[i]
                tgt = steps[i+1]
                
                if src not in nodes:
                    nodes.append(src)
                if tgt not in nodes:
                    nodes.append(tgt)
                    
                edge = (src, tgt)
                edges[edge] = edges.get(edge, 0) + 1
        
        # Build Sankey data format
        source_indices = []
        target_indices = []
        values = []
        
        for (src, tgt), weight in edges.items():
            source_indices.append(nodes.index(src))
            target_indices.append(nodes.index(tgt))
            # Amplify weight for visual clarity
            values.append(weight * 10)
            
        # Node Colors
        node_colors = []
        for node in nodes:
            if node == selected_event:
                node_colors.append("#ff5252") # Origin (Red)
            else:
                # Alternate colors for downstream nodes
                node_colors.append(random.choice(["#4da6ff", "#00e676", "#ff9900", "#b388ff"]))

        # Get current theme for dynamic chart colors
        _active_theme = THEMES.get(st.session_state.get('active_theme', 'Dark Cyan'), THEMES['Dark Cyan'])
        _is_light = st.session_state.get('active_theme', 'Dark Cyan') in ('Light Blue', 'Cool Gray')
        _link_color = "rgba(17, 45, 78, 0.25)" if _is_light else "rgba(255, 255, 255, 0.15)"
        
        # Render Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node = dict(
              pad = 20,
              thickness = 25,
              line = dict(color = _active_theme['--bg-primary'], width = 1.5),
              label = nodes,
              color = node_colors
            ),
            link = dict(
              source = source_indices,
              target = target_indices,
              value = values,
              color = _link_color
            )
        )])
        
        fig.update_layout(
            font_size=12,
            font_color=_active_theme['--text-primary'],
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=30, b=60, l=50, r=20),
            height=550
        )
        render_plotly_chart(fig, width='stretch')

