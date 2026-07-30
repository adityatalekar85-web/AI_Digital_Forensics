import hashlib

import pandas as pd
import streamlit as st
from pandas.api.types import is_numeric_dtype

from utils.auth import require_login
from utils.email_delivery import render_email_sender
from utils.data_io import read_csv_safely
from utils.ui import render_page_header


require_login()


render_page_header(
    "✦",
    "Data Cleaning",
    "Prepare evidence-grade datasets by removing duplicates, repairing missing values, and exporting clean files.",
    "Preparation",
)

uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV dataset to start cleaning.")
    st.stop()

try:
    file_bytes = uploaded_file.getvalue()
    original_df = read_csv_safely(file_bytes)
except Exception as exc:
    st.error(f"Could not read CSV file: {exc}")
    st.stop()

file_hash = hashlib.sha256(file_bytes).hexdigest()[:12]
state_key = f"clean_df_{uploaded_file.name}_{file_hash}"
if state_key not in st.session_state:
    st.session_state[state_key] = original_df.copy()

df = st.session_state[state_key]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", df.shape[0])
c2.metric("Columns", df.shape[1])
c3.metric("Missing Values", int(df.isnull().sum().sum()))
c4.metric("Duplicate Rows", int(df.duplicated().sum()))

st.subheader("Current Dataset")
st.dataframe(df.head(20), use_container_width=True)

st.markdown("---")
st.subheader("Cleaning Actions")

a1, a2, a3 = st.columns(3)

if a1.button("Remove Duplicate Rows"):
    before = len(df)
    st.session_state[state_key] = df.drop_duplicates().reset_index(drop=True)
    removed = before - len(st.session_state[state_key])
    st.success(f"Removed {removed} duplicate rows.")
    st.rerun()

if a2.button("Fill Missing Values"):
    cleaned = df.copy()
    for col in cleaned.columns:
        if is_numeric_dtype(cleaned[col]):
            fill_value = cleaned[col].median()
            if pd.isna(fill_value):
                fill_value = 0
            cleaned[col] = cleaned[col].fillna(fill_value)
        else:
            mode_values = cleaned[col].dropna().mode()
            fill_value = mode_values.iloc[0] if not mode_values.empty else "Unknown"
            cleaned[col] = cleaned[col].fillna(fill_value)
    st.session_state[state_key] = cleaned
    st.success("Missing values filled successfully.")
    st.rerun()

if a3.button("Reset Dataset"):
    st.session_state[state_key] = original_df.copy()
    st.success("Dataset reset.")
    st.rerun()

st.markdown("---")
st.subheader("Missing Values")
missing = pd.DataFrame({"Column": df.columns, "Missing Values": df.isnull().sum().values})
st.dataframe(missing, use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8")
download_col, email_col = st.columns(2)
with download_col:
    st.download_button(
        "Download Clean Dataset",
        csv,
        file_name="clean_dataset.csv",
        mime="text/csv",
        use_container_width=True,
    )

with email_col:
    render_email_sender(
        "clean_dataset",
        "Send Clean Dataset to Email",
        "CyberShield Clean Dataset",
        "Attached is your cleaned dataset exported from CyberShield Forensics.",
        "clean_dataset.csv",
        csv,
    )
