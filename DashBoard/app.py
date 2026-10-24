import streamlit as st
from components.utils import load_css
from config import PAGE_TITLE, PAGE_ICON, LAYOUT

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

load_css()

# Render logo at top of sidebar
st.sidebar.markdown(
    """
    <div class="sidebar-logo-container" id="finsight-sidebar-logo">
        <div class="rhombus-badge">
            <div class="monogram-text">
                <span class="f-letter">F</span><span class="s-letter">S</span>
            </div>
        </div>
        <div class="logo-title">
            <span class="title-top">FINSIGHT</span>
            <span class="title-bottom">INTELLIGENCE</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# Define the navigation structure internally with robust path resolution
import os
BASE_VIEWS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "views")

def view_path(filename):
    return os.path.join(BASE_VIEWS_DIR, filename)

pages = [
    st.Page(view_path("0_Command_Center.py"), title="Command Center", icon=":material/dashboard:"),
    st.Page(view_path("1_Executive_Dashboard.py"), title="Executive Dashboard", icon=":material/insert_chart:"),
    st.Page(view_path("2_News_Explorer.py"), title="News Explorer", icon=":material/article:"),
    st.Page(view_path("3_Company_Explorer.py"), title="Company Explorer", icon=":material/domain:"),
    st.Page(view_path("4_Topic_Intelligence.py"), title="Topic Intelligence", icon=":material/lightbulb:"),
    st.Page(view_path("5_Event_Intelligence.py"), title="Event Intelligence", icon=":material/event:"),
    st.Page(view_path("6_Sector_Intelligence.py"), title="Sector Intelligence", icon=":material/pie_chart:"),
    st.Page(view_path("7_Knowledge_Graph.py"), title="Entity Network", icon=":material/hub:"),
    st.Page(view_path("8_Event_Propagation.py"), title="Event Propagation", icon=":material/share:"),
    st.Page(view_path("9_Sector_Network.py"), title="Sector Network", icon=":material/lan:"),
    st.Page(view_path("10_Company_Network.py"), title="Company Network", icon=":material/account_tree:"),
    st.Page(view_path("11_Timeline_Explorer.py"), title="Timeline Explorer", icon=":material/timeline:"),
    st.Page(view_path("12_Semantic_Search.py"), title="Intelligence Search", icon=":material/manage_search:"),
    st.Page(view_path("13_Recommendation_Center.py"), title="Market Signals", icon=":material/recommend:"),

    st.Page(view_path("15_Download_Center.py"), title="Download Center", icon=":material/download:"),
    st.Page(view_path("16_Settings.py"), title="Settings", icon=":material/settings:"),
    st.Page(view_path("17_About.py"), title="About", icon=":material/info:"),
]

# Initialize the navigation
pg = st.navigation(pages, expanded=True)
# Run the selected page
pg.run()
