import os

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.data_io import read_csv_safely
from utils.ui import render_page_header


require_login()


def get_secret(name):
    try:
        return st.secrets.get(name, os.getenv(name, ""))
    except Exception:
        return os.getenv(name, "")


render_page_header(
    "✧",
    "AI Cyber Security Assistant",
    "Ask cyber security questions, summarize uploaded logs, and generate analyst-ready guidance.",
    "Assistant",
)

api_key = get_secret("GEMINI_API_KEY")

if not api_key:
    st.info("Set GEMINI_API_KEY in environment variables or Streamlit secrets to enable the AI assistant.")
    st.stop()

try:
    import google.generativeai as genai
except ImportError:
    st.warning("google-generativeai is not installed in this environment.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

uploaded_file = st.file_uploader("Upload Security Log CSV", type=["csv"])
df = None

if uploaded_file is not None:
    try:
        df = read_csv_safely(uploaded_file)
        st.subheader("Dataset Preview")
        st.dataframe(df.head(20), use_container_width=True)
    except Exception as exc:
        st.error(f"Could not read CSV file: {exc}")
        st.stop()

default_question = st.query_params.get("assistant_question", "")
question = st.text_area("Ask a cyber security question", value=default_question)

if st.button("Ask AI"):
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    if df is not None:
        prompt = f"""
You are an expert cyber security analyst.

Dataset preview:
{df.head(20).to_string()}

User question:
{question}

Give a clear, practical cyber security analysis.
"""
    else:
        prompt = question

    try:
        with st.spinner("AI is thinking..."):
            response = model.generate_content(prompt)
        st.markdown(response.text)
    except Exception as exc:
        st.error(f"AI Error: {exc}")
