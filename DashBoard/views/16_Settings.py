import streamlit as st
import time
from components.utils import load_css, render_page_header

load_css()

render_page_header("System Configuration", "Manage platform preferences.")

# Initialize session state for settings if they don't exist
if 'settings_saved' not in st.session_state:
    st.session_state.settings_saved = False
if 'show_hints' not in st.session_state:
    st.session_state.show_hints = True

with st.container(border=True):
    st.markdown("<h4 style='color: var(--accent); margin-bottom: 15px;'>User Experience</h4>", unsafe_allow_html=True)
    
    # Theme Selector
    if 'active_theme' not in st.session_state:
        st.session_state.active_theme = "Light Blue"
        
    selected_theme = st.selectbox(
        "Global Dashboard Theme", 
        ["Light Blue", "Cool Gray", "Dark Cyan", "Dark Hacker"], 
        index=["Light Blue", "Cool Gray", "Dark Cyan", "Dark Hacker"].index(st.session_state.active_theme),
        help="Select a color palette to instantly theme the entire dashboard."
    )
    
    # If theme changes, update session state and rerun immediately to apply new CSS
    if selected_theme != st.session_state.active_theme:
        st.session_state.active_theme = selected_theme
        st.rerun()
        
    st.divider()
    # A setting we can actually track in session state
    show_hints = st.toggle("Show Tooltips & Onboarding Hints", value=st.session_state.show_hints)

st.markdown("<br>", unsafe_allow_html=True)

# Action button area
_, _, c3 = st.columns([2, 2, 1])
with c3:
    if st.button("Save System Configuration", type="primary", use_container_width=True):
        # Save to session state so they actually persist
        st.session_state.show_hints = show_hints
        
        with st.spinner("Saving configuration..."):
            time.sleep(0.5)
        st.toast("Settings saved successfully!", icon="✅")
        time.sleep(0.5)
        st.success("Configuration updated and saved to active session.")
