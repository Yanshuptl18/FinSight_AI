import streamlit as st
import os

THEMES = {
    "Light Blue": {
        "--bg-primary": "#F9F7F7",
        "--bg-secondary": "#DBE2EF",
        "--accent": "#3F72AF",
        "--text-primary": "#112D4E",
        "--text-bright": "#0a1a2e",
        "--btn-text": "#FFFFFF",
        "--card-bg": "rgba(219, 226, 239, 0.6)",
        "--border-color": "rgba(17, 45, 78, 0.15)",
        "--sidebar-active-bg": "#F9F7F7",
        "--color-bull": "#008542",
        "--bg-bull": "rgba(0, 133, 66, 0.15)",
        "--color-bear": "#d32f2f",
        "--bg-bear": "rgba(211, 47, 47, 0.15)",
        "--color-neutral": "#475569",
        "--bg-neutral": "rgba(71, 85, 105, 0.15)",
        "--sidebar-link-bg": "var(--accent)",
        "--sidebar-link-text": "var(--btn-text)",
        "--sidebar-link-hover-bg": "var(--accent)",
        "--sidebar-link-hover-text": "var(--btn-text)",
        "--sidebar-link-active-bg": "var(--accent)",
        "--sidebar-link-active-text": "var(--btn-text)",
        "--sidebar-link-border": "transparent"
    },
    "Cool Gray": {
        "--bg-primary": "#F8FAFC",
        "--bg-secondary": "#D9EAFD",
        "--accent": "#BCCCDC",
        "--text-primary": "#475569", 
        "--text-bright": "#1e293b",
        "--btn-text": "#1e293b",
        "--card-bg": "rgba(217, 234, 253, 0.6)",
        "--border-color": "rgba(188, 204, 220, 0.5)",
        "--sidebar-active-bg": "#F8FAFC",
        "--color-bull": "#059669",
        "--bg-bull": "rgba(5, 150, 105, 0.15)",
        "--color-bear": "#dc2626",
        "--bg-bear": "rgba(220, 38, 38, 0.15)",
        "--color-neutral": "#475569",
        "--bg-neutral": "rgba(71, 85, 105, 0.15)",
        "--sidebar-link-bg": "var(--accent)",
        "--sidebar-link-text": "var(--btn-text)",
        "--sidebar-link-hover-bg": "var(--accent)",
        "--sidebar-link-hover-text": "var(--btn-text)",
        "--sidebar-link-active-bg": "var(--accent)",
        "--sidebar-link-active-text": "var(--btn-text)",
        "--sidebar-link-border": "transparent"
    },
    "Dark Cyan": {
        "--bg-primary": "#222831",
        "--bg-secondary": "#393E46",
        "--accent": "#00ADB5",
        "--text-primary": "#EEEEEE",
        "--text-bright": "#FFFFFF",
        "--btn-text": "#FFFFFF",
        "--card-bg": "rgba(57, 62, 70, 0.6)",
        "--border-color": "rgba(238, 238, 238, 0.1)",
        "--sidebar-active-bg": "#222831",
        "--color-bull": "#00e676",
        "--bg-bull": "rgba(0, 230, 118, 0.15)",
        "--color-bear": "#ff6b6b",
        "--bg-bear": "rgba(255, 107, 107, 0.15)",
        "--color-neutral": "#c9d1d9",
        "--bg-neutral": "rgba(255, 255, 255, 0.1)",
        "--sidebar-link-bg": "var(--accent)",
        "--sidebar-link-text": "var(--btn-text)",
        "--sidebar-link-hover-bg": "var(--accent)",
        "--sidebar-link-hover-text": "var(--btn-text)",
        "--sidebar-link-active-bg": "var(--accent)",
        "--sidebar-link-active-text": "var(--btn-text)",
        "--sidebar-link-border": "transparent"
    },
    "Dark Hacker": {
        "--bg-primary": "#000000",
        "--bg-secondary": "#3D0000",
        "--accent": "#FF0000",
        "--text-primary": "#CCCCCC",
        "--text-bright": "#FF0000",
        "--btn-text": "#FFFFFF",
        "--card-bg": "rgba(61, 0, 0, 0.6)",
        "--border-color": "rgba(149, 1, 1, 0.5)",
        "--sidebar-active-bg": "#000000",
        "--color-bull": "#00ff00",
        "--bg-bull": "rgba(0, 255, 0, 0.15)",
        "--color-bear": "#ff0000",
        "--bg-bear": "rgba(255, 0, 0, 0.15)",
        "--color-neutral": "#cccccc",
        "--bg-neutral": "rgba(255, 255, 255, 0.1)",
        "--sidebar-link-bg": "#0A0A0A",
        "--sidebar-link-text": "#FFFFFF",
        "--sidebar-link-hover-bg": "#000000",
        "--sidebar-link-hover-text": "#FFFFFF",
        "--sidebar-link-active-bg": "#0A0A0A",
        "--sidebar-link-active-text": "#FFFFFF",
        "--sidebar-link-border": "rgba(255, 255, 255, 0.1)"
    }
}

def load_css():
    """Injects custom CSS from assets/css/style.css into the Streamlit app.
    Also injects dynamic CSS variables based on the active theme.
    """
    if 'active_theme' not in st.session_state:
        st.session_state.active_theme = "Light Blue" # Default to Light Blue theme
        
    theme = THEMES.get(st.session_state.active_theme, THEMES["Dark Cyan"])
    
    # Generate the CSS variable root block
    css_vars = ":root {\n"
    for key, value in theme.items():
        css_vars += f"    {key}: {value};\n"
    css_vars += "}\n"
    
    # Inject variables
    st.markdown(f"<style>{css_vars}</style>", unsafe_allow_html=True)

    # Inject static CSS file
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "css", "style.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found.")

def render_template(template_name: str, **kwargs) -> str:
    """Reads an HTML template from assets/templates and formats it with kwargs."""
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "templates", f"{template_name}.html")
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
            html_str = template.format(**kwargs)
            # CRITICAL: Strip leading whitespace from all lines so Streamlit's 
            # Markdown parser doesn't accidentally treat indented HTML as a code block!
            return "\n".join(line.lstrip() for line in html_str.split("\n"))
    except FileNotFoundError:
        st.error(f"Template not found: {template_name}.html")
        return ""
    except KeyError as e:
        st.error(f"Missing template variable {e} for {template_name}.html")
        return ""

def render_page_header(title: str, subtitle: str = ""):
    """Renders a beautiful, theme-aware page header."""
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"<p style='color: var(--btn-text); font-size: 1.15rem; margin-bottom: 0; font-weight: 500; opacity: 0.95; max-width: 800px;'>{subtitle}</p>"
        
    html_content = render_template("page_header", title=title, subtitle_html=subtitle_html)
    if html_content:
        st.markdown(html_content, unsafe_allow_html=True)
