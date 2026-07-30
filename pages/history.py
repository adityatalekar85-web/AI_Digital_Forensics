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
    "◷",
    "Prediction History",
    "Search, filter, export, and email saved ML prediction records from prior investigations.",
    "Case Timeline",
)

conn = sqlite3.connect(DB_PATH)
ensure_predictions_table(conn)
df = pd.read_sql_query("SELECT * FROM predictions ORDER BY id DESC", conn)
conn.close()

if df.empty:
    st.info("No predictions saved yet.")
    st.stop()

st.subheader("Search and Filters")
search = st.text_input("Search Username")

if search:
    df = df[df["username"].str.contains(search, case=False, na=False)]

col1, col2 = st.columns(2)
prediction_filter = col1.selectbox("Prediction", ["All", "Safe", "Threat"])
country_values = sorted(df["country"].dropna().unique().tolist())
country_filter = col2.selectbox("Country", ["All"] + country_values)

if prediction_filter != "All":
    df = df[df["prediction"] == prediction_filter]

if country_filter != "All":
    df = df[df["country"] == country_filter]

c1, c2, c3 = st.columns(3)
c1.metric("Total Predictions", len(df))
c2.metric("Safe", int((df["prediction"] == "Safe").sum()))
c3.metric("Threat", int((df["prediction"] == "Threat").sum()))

st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8")
download_col, email_col = st.columns(2)
with download_col:
    st.download_button(
        "Download CSV",
        csv,
        file_name="prediction_history.csv",
        mime="text/csv",
        use_container_width=True,
    )

with email_col:
    render_email_sender(
        "history_csv",
        "Send History CSV to Email",
        "CyberShield Prediction History",
        "Attached is your CyberShield Forensics prediction history export.",
        "prediction_history.csv",
        csv,
    )
