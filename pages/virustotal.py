import os

import requests
import streamlit as st

from utils.auth import require_login
from utils.ui import render_page_header


require_login()


def get_secret(name):
    try:
        return st.secrets.get(name, os.getenv(name, ""))
    except Exception:
        return os.getenv(name, "")


render_page_header(
    "◎",
    "VirusTotal Reputation Checker",
    "Check IP addresses and URLs against external reputation intelligence.",
    "Reputation",
)

api_key = get_secret("VIRUSTOTAL_API_KEY")

if not api_key:
    st.info("Set VIRUSTOTAL_API_KEY in environment variables or Streamlit secrets to enable this page.")
    st.stop()

option = st.selectbox("Select Scan Type", ["IP Address", "URL"])
headers = {"x-apikey": api_key}

if option == "IP Address":
    ip = st.text_input("Enter IP Address")

    if st.button("Check IP"):
        if not ip.strip():
            st.warning("Please enter an IP address.")
            st.stop()

        try:
            response = requests.get(
                f"https://www.virustotal.com/api/v3/ip_addresses/{ip.strip()}",
                headers=headers,
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
            stats = data["data"]["attributes"]["last_analysis_stats"]
            st.success("Analysis completed")
            st.json(stats)
        except Exception as exc:
            st.error(f"VirusTotal error: {exc}")

if option == "URL":
    url_input = st.text_input("Enter URL")

    if st.button("Check URL"):
        if not url_input.strip():
            st.warning("Please enter a URL.")
            st.stop()

        try:
            response = requests.post(
                "https://www.virustotal.com/api/v3/urls",
                headers=headers,
                data={"url": url_input.strip()},
                timeout=20,
            )
            response.raise_for_status()
            st.success("URL submitted successfully")
            st.json(response.json())
        except Exception as exc:
            st.error(f"VirusTotal error: {exc}")
