# config.py - Centralized configuration for the dashboard
import os

# Page Configuration
PAGE_TITLE = "FinSight AI Platform"
PAGE_ICON = "Chart"
LAYOUT = "wide"

# Theme Colors
THEME_COLOR = "#0052cc"
BACKGROUND_COLOR = "#0e1117"
TEXT_COLOR = "#ffffff"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")
MODEL_PATH = os.path.join(BASE_DIR, "models")
REPORT_PATH = os.path.join(BASE_DIR, "reports")
EXPORT_PATH = "exports/generated_reports"

# Cache Settings
CACHE_TTL = 3600

# Graph Constants
GRAPH_NODE_COLOR = "#1f77b4"
GRAPH_EDGE_COLOR = "#7f7f7f"

# Hugging Face Repository Configuration (No hardcoded tokens)
HF_REPO_ID = os.getenv("HF_REPO_ID", "Yanshuptl18/finsight-ai-data")

def get_hf_token():
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "HF_TOKEN" in st.secrets:
            token = st.secrets["HF_TOKEN"]
            if token and str(token).strip():
                return str(token).strip()
    except Exception:
        pass
    token = os.getenv("HF_TOKEN")
    if token and str(token).strip():
        return str(token).strip()
    return None

HF_TOKEN = get_hf_token()
