import os

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.auth import require_login
from utils.data_io import read_csv_safely


require_login()


def get_secret(name):
    try:
        return st.secrets.get(name, os.getenv(name, ""))
    except Exception:
        return os.getenv(name, "")


def detect_dataset_type(df):
    columns = set(df.columns)
    if {"Threat_Label", "Country", "Attack_Type", "Risk_Score"}.issubset(columns):
        return "Cyber Security"
    if {"Room_Type", "Payment_Status", "Total_Bill"}.issubset(columns):
        return "Hotel"
    if {"Sales", "Profit"}.issubset(columns):
        return "Sales"
    return "Generic"


def render_ai_tools(df):
    api_key = get_secret("GEMINI_API_KEY")

    st.markdown("---")
    st.subheader("AI Dataset Analysis")

    if not api_key:
        st.info("Set GEMINI_API_KEY in environment variables or Streamlit secrets to enable AI analysis.")
        return

    try:
        import google.generativeai as genai
    except ImportError:
        st.warning("google-generativeai is not installed in this environment.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    if st.button("Analyze Dataset with AI"):
        with st.spinner("Analyzing dataset..."):
            prompt = f"""
You are an expert data analyst. Analyze this dataset.

Columns:
{df.columns.tolist()}

Sample:
{df.head(20).to_string()}

Include dataset type, data quality, key trends, risks, and recommendations.
"""
            try:
                response = model.generate_content(prompt)
                st.success("Analysis completed")
                st.markdown(response.text)
            except Exception as exc:
                st.error(f"AI Error: {exc}")

    st.subheader("Executive AI Report")
    if st.button("Generate Executive Report"):
        with st.spinner("Generating report..."):
            prompt = f"""
Create a professional executive report from this dataset.

Columns:
{df.columns.tolist()}

Sample:
{df.head(30).to_string()}

Include executive summary, findings, risks, opportunities, recommendations, and conclusion.
"""
            try:
                response = model.generate_content(prompt)
                st.success("Executive report generated")
                st.markdown(response.text)
            except Exception as exc:
                st.error(f"AI Error: {exc}")

    st.subheader("Chat With Dataset")
    question = st.text_input("Ask anything about your uploaded dataset")

    if st.button("Ask AI"):
        if not question.strip():
            st.warning("Please enter a question.")
            return

        with st.spinner("AI is thinking..."):
            prompt = f"""
Answer only from this dataset. If the answer cannot be determined, say so clearly.

Columns:
{df.columns.tolist()}

Sample:
{df.head(50).to_string()}

Question:
{question}
"""
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as exc:
                st.error(f"AI Error: {exc}")


st.markdown(
    """
    <div class="page-hero">
        <div>
            <div class="eyebrow">CyberShield Forensics</div>
            <h1>Investigation Command Center</h1>
            <p>Command-grade threat analytics with live log inspection, attack-pattern visualization, ML risk scoring, and evidence-ready reporting.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV dataset to start live investigation. No default dataset is loaded.")
    st.markdown(
        """
        <div class="mission-grid">
            <div class="mission-card">
                <span>01</span>
                <strong>Upload Evidence</strong>
                <p>Start with a CSV log file from authentication, firewall, endpoint, or case exports.</p>
            </div>
            <div class="mission-card">
                <span>02</span>
                <strong>Analyze Risk</strong>
                <p>Inspect missing values, suspicious patterns, attack types, and high-risk records.</p>
            </div>
            <div class="mission-card">
                <span>03</span>
                <strong>Share Results</strong>
                <p>Download reports or send them directly to an investigator's email.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

try:
    df = read_csv_safely(uploaded_file)
except Exception as exc:
    st.error(f"Could not read CSV file: {exc}")
    st.stop()

dataset_type = detect_dataset_type(df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", df.shape[0])
c2.metric("Columns", df.shape[1])
c3.metric("Missing Values", int(df.isnull().sum().sum()))
c4.metric("Dataset Type", dataset_type)

st.markdown(
    """
    <div class="mission-grid">
        <div class="mission-card">
            <span>01</span>
            <strong>Ingest</strong>
            <p>Upload logs and verify schema quality before investigation.</p>
        </div>
        <div class="mission-card">
            <span>02</span>
            <strong>Detect</strong>
            <p>Use ML prediction and risk signals to classify suspicious events.</p>
        </div>
        <div class="mission-card">
            <span>03</span>
            <strong>Report</strong>
            <p>Export history, reports, and PDF evidence for case review.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if "Threat_Label" in df.columns:
    threat_count = int((df["Threat_Label"].astype(str) == "Threat").sum())
    safe_count = int((df["Threat_Label"].astype(str) == "Safe").sum())
    high_risk_count = int((df.get("Risk_Score", pd.Series(dtype=int)) >= 70).sum()) if "Risk_Score" in df.columns else 0

    t1, t2, t3 = st.columns(3)
    t1.metric("Threat Events", threat_count)
    t2.metric("Safe Events", safe_count)
    t3.metric("High Risk Logs", high_risk_count)

st.subheader("Dataset Preview")
st.dataframe(df.head(20), use_container_width=True)

filtered_df = df.copy()
object_cols = filtered_df.select_dtypes(include="object").columns.tolist()

if object_cols:
    st.markdown(
        """
        <div class="filter-panel">
            <h3>Dataset Filters</h3>
            <p>Select values below to narrow the investigation view.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    filter_columns = st.columns(min(3, len(object_cols)))
    for index, col in enumerate(object_cols):
        values = sorted(filtered_df[col].dropna().astype(str).unique().tolist())
        if not values:
            continue

        with filter_columns[index % len(filter_columns)]:
            selected = st.multiselect(
                col,
                values,
                default=values,
                key=f"dashboard_filter_{col}",
            )
        filtered_df = filtered_df[filtered_df[col].astype(str).isin(selected)]
else:
    st.info("No categorical columns available for filtering.")

st.markdown("---")
st.subheader("Visual Analysis")

numeric_cols = filtered_df.select_dtypes(include="number").columns.tolist()
category_cols = filtered_df.select_dtypes(include="object").columns.tolist()

if filtered_df.empty:
    st.warning("No rows match the selected filters.")
elif numeric_cols:
    selected_num = st.selectbox("Numeric Column", numeric_cols)
    fig = px.histogram(filtered_df, x=selected_num, title=f"Distribution of {selected_num}")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No numeric columns found for histogram analysis.")

if not filtered_df.empty and category_cols:
    selected_cat = st.selectbox("Category Column", category_cols)
    chart = filtered_df[selected_cat].astype(str).value_counts().reset_index()
    chart.columns = [selected_cat, "Count"]
    fig = px.bar(chart.head(20), x=selected_cat, y="Count", color="Count", title=f"Top {selected_cat} Values")
    st.plotly_chart(fig, use_container_width=True)

if not filtered_df.empty and len(numeric_cols) >= 2:
    st.subheader("Correlation Heatmap")
    corr = filtered_df[numeric_cols].corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Statistical Summary")
st.dataframe(filtered_df.describe(include="all"), use_container_width=True)

missing = filtered_df.isnull().sum().reset_index()
missing.columns = ["Column", "Missing"]
fig = px.bar(missing, x="Column", y="Missing", color="Missing", title="Missing Values by Column")
st.plotly_chart(fig, use_container_width=True)

render_ai_tools(filtered_df)
