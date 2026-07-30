import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.data_io import read_csv_safely
from utils.ui import render_page_header


require_login()


render_page_header(
    "⇧",
    "Dataset Upload",
    "Import CSV evidence and inspect schema, missing values, and field types before analysis.",
    "Evidence Intake",
)

uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file is None:
    st.info("Upload any CSV dataset to continue.")
    st.stop()

try:
    df = read_csv_safely(uploaded_file)
except Exception as exc:
    st.error(f"Error reading file: {exc}")
    st.stop()

st.success("Dataset uploaded successfully")

c1, c2, c3 = st.columns(3)
c1.metric("Rows", df.shape[0])
c2.metric("Columns", df.shape[1])
c3.metric("Missing Values", int(df.isnull().sum().sum()))

st.markdown("---")
st.subheader("Dataset Preview")
st.dataframe(df.head(20), use_container_width=True)

st.markdown("---")
st.subheader("Column Names")
st.write(df.columns.tolist())

st.markdown("---")
st.subheader("Data Types")
st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={"index": "Column", 0: "Data Type"}))

st.markdown("---")
st.subheader("Missing Values")
missing = pd.DataFrame({"Column": df.columns, "Missing Values": df.isnull().sum().values})
st.dataframe(missing, use_container_width=True)
