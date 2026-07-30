from datetime import datetime

import streamlit as st

from utils.auth import current_user


def render_topbar():
    user = current_user()
    name = user.get("full_name") or user.get("username") or "Analyst"
    today = datetime.now().strftime("%d %b %Y")
    st.markdown(
        f"""
        <div class="app-topbar">
            <div>
                <span class="topbar-kicker">CyberShield Forensics</span>
                <strong>Professional Investigation Workspace</strong>
            </div>
            <div class="topbar-meta">
                <span>{today}</span>
                <span>{name}</span>
                <span class="status-dot">Online</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(icon, title, subtitle, badge="Active Module"):
    st.markdown(
        f"""
        <div class="module-header">
            <div class="module-icon">{icon}</div>
            <div class="module-copy">
                <div class="module-badge">{badge}</div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
