import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from components.utils import THEMES

def get_theme_colors():
    active = st.session_state.get("active_theme", "Dark Cyan")
    return THEMES.get(active, THEMES["Dark Cyan"])

def create_kpi_card(title, value, delta=None, delta_color="normal"):
    # Using CSS variables for inline HTML styles so they adapt instantly
    if delta:
        if delta_color == "normal":
            if str(delta).startswith("-"):
                delta_html = f'<span style="background: rgba(255,68,68,0.15); color: #ff6b6b; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; white-space: nowrap; border: 1px solid rgba(255,68,68,0.3); display: inline-block;">↓ {delta}</span>'
            else:
                delta_html = f'<span style="background: rgba(0,200,81,0.15); color: #00e676; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; white-space: nowrap; border: 1px solid rgba(0,200,81,0.3); display: inline-block;">↑ {delta}</span>'
        else:
            delta_html = f'<span style="background: var(--border-color); color: var(--text-primary); padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; white-space: nowrap; border: 1px solid var(--border-color); display: inline-block;">{delta}</span>'
    else:
        delta_html = ""

    delta_container = f'<div style="align-self: flex-start; margin-top: 4px;">{delta_html}</div>' if delta_html else ''
    html = f'<div class="kpi-card"><div style="font-size: 0.8rem; color: var(--text-primary); font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{title}</div><div style="display: flex; flex-direction: column; justify-content: space-between; flex-grow: 1; gap: 6px;"><div style="font-size: 1.35rem; font-weight: 800; color: var(--text-bright); line-height: 1.25; word-wrap: break-word; overflow-wrap: break-word;">{value}</div>{delta_container}</div></div>'
    st.markdown(html, unsafe_allow_html=True)

def plot_donut_chart(labels, values, title, colors=None):
    theme = get_theme_colors()
    if colors is None:
        colors = ['#00e676', '#ff6b6b', theme['--accent'], '#ffbb33']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.55, 
        marker=dict(colors=colors, line=dict(color=theme['--bg-primary'], width=3)),
        hoverinfo="label+percent+value",
        textinfo="percent",
        textfont=dict(color='#ffffff', size=12)
    )])
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=theme['--text-bright'])),
        font=dict(color=theme['--text-primary']),
        legend=dict(font=dict(color=theme['--text-primary'])),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=20, l=20, r=20),
        hoverlabel=dict(bgcolor=theme['--bg-secondary'], font_size=14, bordercolor=theme['--border-color']),
        clickmode='event+select'
    )
    return fig

def plot_time_series(df, x_col, y_col, title, enable_rangeslider=True):
    theme = get_theme_colors()
    fig = px.line(df, x=x_col, y=y_col, title=title)
    fig.update_traces(
        line=dict(width=3, color=theme['--accent'], shape='linear'),
        fill='tozeroy',
        fillcolor=theme['--border-color'],
        mode='lines+markers',
        marker=dict(size=5, color=theme['--accent'], line=dict(width=1.5, color=theme['--bg-primary'])),
        selected=dict(marker=dict(opacity=1)),
        unselected=dict(marker=dict(opacity=0.2, color=theme['--text-primary']))
    )
    fig.update_layout(
        title=dict(font=dict(size=16, color=theme['--text-bright'])),
        font=dict(color=theme['--text-primary']),
        legend=dict(font=dict(color=theme['--text-primary'])),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=60, l=60, r=30),
        xaxis=dict(
            showgrid=False, 
            title="", 
            tickfont=dict(color=theme['--text-primary']),
            rangeslider=dict(visible=enable_rangeslider),
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(step="all", label="All")
                ]),
                bgcolor=theme['--bg-secondary'],
                activecolor=theme['--accent'],
                font=dict(color=theme['--text-bright'], size=11)
            ) if enable_rangeslider else None
        ),
        yaxis=dict(automargin=True, showgrid=True, gridcolor=theme['--border-color'], title="", tickfont=dict(color=theme['--text-primary'])),
        hovermode="x unified",
        hoverlabel=dict(bgcolor=theme['--bg-secondary'], bordercolor=theme['--accent'], font=dict(color=theme['--text-bright'])),
        clickmode='event+select'
    )
    return fig

def plot_bar_chart(df, x_col, y_col, title, color=None):
    theme = get_theme_colors()
    fig = px.bar(df, x=x_col, y=y_col, title=title, color=color)
    fig.update_traces(
        marker_color=theme['--accent'] if not color else None,
        marker_line_color=theme['--bg-primary'],
        marker_line_width=1.5,
        opacity=0.9,
        selected=dict(marker=dict(opacity=1)),
        unselected=dict(marker=dict(opacity=0.2, color=theme['--text-primary']))
    )
    fig.update_layout(
        title=dict(font=dict(size=16, color=theme['--text-bright'])),
        font=dict(color=theme['--text-primary']),
        legend=dict(font=dict(color=theme['--text-primary'])),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=60, l=140, r=30),
        xaxis=dict(showgrid=False, title="", tickfont=dict(color=theme['--text-primary'])),
        yaxis=dict(automargin=True, showgrid=True, gridcolor=theme['--border-color'], title="", tickfont=dict(color=theme['--text-primary'])),
        hovermode="x",
        hoverlabel=dict(bgcolor=theme['--bg-secondary'], bordercolor=theme['--border-color'], font=dict(color=theme['--text-bright'])),
        clickmode='event+select'
    )
    return fig

def apply_custom_theme(fig):
    """Applies the current dynamic theme colors to ANY Plotly figure."""
    theme = get_theme_colors()
    title_text = None
    if fig.layout.title and getattr(fig.layout.title, 'text', None):
        title_text = fig.layout.title.text

    fig.update_layout(
        font=dict(color=theme['--text-primary'], family='Inter, sans-serif'),
        legend=dict(font=dict(color=theme['--text-primary'])),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, title_font=dict(color=theme['--text-primary']), tickfont=dict(color=theme['--text-primary'])),
        yaxis=dict(automargin=True, showgrid=True, gridcolor=theme['--border-color'], title_font=dict(color=theme['--text-primary']), tickfont=dict(color=theme['--text-primary'])),
        hoverlabel=dict(bgcolor=theme['--bg-secondary'], font_size=13, bordercolor=theme['--border-color'], font=dict(color=theme['--text-bright'])),
    )
    
    if title_text:
        fig.update_layout(title=dict(text=title_text, font=dict(size=16, color=theme['--text-bright'])))

    return fig

def render_plotly_chart(fig, **kwargs):
    """Renders a Plotly chart in Streamlit, applying the dynamic custom theme and disabling Streamlit's default theme override."""
    fig = apply_custom_theme(fig)
    st.plotly_chart(fig, theme=None, **kwargs)
