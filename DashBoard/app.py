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

# Define the navigation structure internally so Streamlit handles routing
# Using a flat list removes all plain text section headers, leaving ONLY the styled buttons
pages = [
    st.Page("views/0_Command_Center.py", title="Command Center", icon=":material/dashboard:"),
    st.Page("views/1_Executive_Dashboard.py", title="Executive Dashboard", icon=":material/insert_chart:"),
    st.Page("views/2_News_Explorer.py", title="News Explorer", icon=":material/article:"),
    st.Page("views/3_Company_Explorer.py", title="Company Explorer", icon=":material/domain:"),
    st.Page("views/4_Topic_Intelligence.py", title="Topic Intelligence", icon=":material/lightbulb:"),
    st.Page("views/5_Event_Intelligence.py", title="Event Intelligence", icon=":material/event:"),
    st.Page("views/6_Sector_Intelligence.py", title="Sector Intelligence", icon=":material/pie_chart:"),
    st.Page("views/7_Knowledge_Graph.py", title="Knowledge Graph", icon=":material/hub:"),
    st.Page("views/8_Event_Propagation.py", title="Event Propagation", icon=":material/share:"),
    st.Page("views/9_Sector_Network.py", title="Sector Network", icon=":material/lan:"),
    st.Page("views/10_Company_Network.py", title="Company Network", icon=":material/account_tree:"),
    st.Page("views/11_Timeline_Explorer.py", title="Timeline Explorer", icon=":material/timeline:"),
    st.Page("views/12_Semantic_Search.py", title="Semantic Search", icon=":material/manage_search:"),
    st.Page("views/13_Recommendation_Center.py", title="Recommendation Center", icon=":material/recommend:"),
    st.Page("views/15_Download_Center.py", title="Download Center", icon=":material/download:"),
    st.Page("views/16_Settings.py", title="Settings", icon=":material/settings:"),
    st.Page("views/17_About.py", title="About", icon=":material/info:"),
]

# Initialize the navigation
pg = st.navigation(pages)
# Run the selected page
pg.run()
