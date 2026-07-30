import base64
import mimetypes
from pathlib import Path

import streamlit as st

from utils.ai_popup import render_ai_popup
from utils.auth import init_auth_state, logout_button
from utils.ui import render_topbar


st.set_page_config(
    page_title="CyberShield Forensics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def css_asset_url(asset_name):
    asset_path = Path("assets") / asset_name
    if not asset_path.exists():
        return asset_name

    mime_type = mimetypes.guess_type(asset_path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(asset_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def load_css():
    with open("assets/style.css", encoding="utf-8") as css_file:
        css = css_file.read()

    replacements = {
        'url("login-cybershield.png")': f'url("{css_asset_url("login-cybershield.png")}")',
        'url("luxury-cyber-hero.svg")': f'url("{css_asset_url("luxury-cyber-hero.svg")}")',
        'url("cyber-hero.svg")': f'url("{css_asset_url("cyber-hero.svg")}")',
    }
    for original, replacement in replacements.items():
        css = css.replace(original, replacement)

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


PAGES = {
    "▦ Dashboard": "pages/dashboard.py",
    "⇧ Upload Logs": "pages/upload.py",
    "✦ Data Cleaning": "pages/cleaning.py",
    "◌ Data Visualization": "pages/visualization.py",
    "◇ ML Threat Detection": "pages/ml_prediction.py",
    "▣ ML Performance": "pages/model_performance.py",
    "◎ VirusTotal": "pages/virustotal.py",
    "◷ Prediction History": "pages/history.py",
    "✧ AI Assistant": "pages/ai_assistant.py",
    "▤ Reports": "pages/reports.py",
}

PAGE_ALIASES = {
    "Dashboard": "▦ Dashboard",
    "Upload Logs": "⇧ Upload Logs",
    "Data Cleaning": "✦ Data Cleaning",
    "Data Visualization": "◌ Data Visualization",
    "ML Threat Detection": "◇ ML Threat Detection",
    "ML Performance": "▣ ML Performance",
    "VirusTotal": "◎ VirusTotal",
    "Prediction History": "◷ Prediction History",
    "AI Assistant": "✧ AI Assistant",
    "Reports": "▤ Reports",
}


load_css()
init_auth_state()

if not st.session_state["logged_in"]:
    exec(open("pages/login.py", encoding="utf-8").read())
    st.stop()

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="sidebar-logo">CS</div>
        <div>
            <div class="sidebar-title">CyberShield</div>
            <div class="sidebar-subtitle">Professional SOC Console</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

logout_button()
st.sidebar.markdown("---")

requested_page = st.query_params.get("page", "Dashboard")
requested_page = PAGE_ALIASES.get(requested_page, requested_page)
page_names = list(PAGES.keys())
default_index = page_names.index(requested_page) if requested_page in PAGES else 0
selected_page = st.sidebar.radio("Select Module", page_names, index=default_index)

st.sidebar.markdown("---")
st.sidebar.caption("Investigation, analytics, prediction, and reporting workspace.")

render_topbar()
exec(open(PAGES[selected_page], encoding="utf-8").read())
render_ai_popup()
