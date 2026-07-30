import sqlite3

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.email_delivery import render_email_sender
from utils.ui import render_page_header


require_login()


DB_PATH = "cyber.db"


def ensure_predictions_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            ip TEXT,
            country TEXT,
            login_status TEXT,
            prediction TEXT,
            confidence REAL,
            date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


render_page_header(
    "▤",
    "Investigation Reports",
    "Review saved threat decisions and export CSV reports for case documentation.",
    "Reporting",
)

conn = sqlite3.connect(DB_PATH)
ensure_predictions_table(conn)

df = pd.read_sql_query("SELECT * FROM predictions ORDER BY id DESC", conn)
conn.close()

if df.empty:
    st.warning("No reports available yet. Run a prediction first.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Total Reports", len(df))
c2.metric("Threats", int((df["prediction"] == "Threat").sum()))
c3.metric("Safe", int((df["prediction"] == "Safe").sum()))

st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8")
download_col, email_col = st.columns(2)
with download_col:
    st.download_button(
        "Download CSV Report",
        csv,
        file_name="Cyber_Report.csv",
        mime="text/csv",
        use_container_width=True,
    )

with email_col:
    render_email_sender(
        "reports_csv",
        "Send CSV Report to Email",
        "CyberShield Investigation CSV Report",
        "Attached is your CyberShield Forensics investigation report.",
        "Cyber_Report.csv",
        csv,
    )
