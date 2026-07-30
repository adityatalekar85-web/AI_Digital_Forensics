import plotly.express as px
import streamlit as st

from utils.auth import require_login
from utils.data_io import read_csv_safely
from utils.ui import render_page_header


require_login()


render_page_header(
    "▥",
    "Data Visualization",
    "Explore distributions, correlations, categories, and cyber-specific investigation patterns.",
    "Analytics",
)

uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV dataset to view charts.")
    st.stop()

try:
    df = read_csv_safely(uploaded_file)
except Exception as exc:
    st.error(f"Could not read CSV file: {exc}")
    st.stop()

st.success("Dataset loaded successfully")
st.dataframe(df.head(20), use_container_width=True)

numeric_cols = df.select_dtypes(include="number").columns.tolist()
category_cols = df.select_dtypes(include="object").columns.tolist()

if not numeric_cols and not category_cols:
    st.warning("No supported columns found for visualization.")
    st.stop()

if numeric_cols:
    st.markdown("---")
    st.subheader("Histogram")
    col = st.selectbox("Select Numeric Column", numeric_cols, key="hist")
    st.plotly_chart(px.histogram(df, x=col), use_container_width=True)

if category_cols:
    st.markdown("---")
    st.subheader("Category Bar Chart")
    col = st.selectbox("Select Category Column", category_cols, key="bar")
    chart = df[col].astype(str).value_counts().reset_index()
    chart.columns = [col, "Count"]
    st.plotly_chart(px.bar(chart.head(25), x=col, y="Count", color="Count"), use_container_width=True)

if category_cols:
    st.markdown("---")
    st.subheader("Pie Chart")
    col = st.selectbox("Pie Category", category_cols, key="pie")
    st.plotly_chart(px.pie(df, names=col), use_container_width=True)

if len(numeric_cols) >= 2:
    st.markdown("---")
    st.subheader("Scatter Plot")
    x_col = st.selectbox("X Axis", numeric_cols, key="scatter_x")
    y_col = st.selectbox("Y Axis", numeric_cols, index=1, key="scatter_y")
    color_col = st.selectbox("Color", ["None"] + category_cols, key="scatter_color")
    color = None if color_col == "None" else color_col
    st.plotly_chart(px.scatter(df, x=x_col, y=y_col, color=color), use_container_width=True)

if len(numeric_cols) >= 2:
    st.markdown("---")
    st.subheader("Line Chart")
    x_col = st.selectbox("Line X Axis", df.columns.tolist(), key="line_x")
    y_col = st.selectbox("Line Y Axis", numeric_cols, key="line_y")
    st.plotly_chart(px.line(df, x=x_col, y=y_col), use_container_width=True)

if numeric_cols:
    st.markdown("---")
    st.subheader("Box Plot")
    col = st.selectbox("Box Plot Column", numeric_cols, key="box")
    st.plotly_chart(px.box(df, y=col), use_container_width=True)

if len(numeric_cols) >= 2:
    st.markdown("---")
    st.subheader("Correlation Heatmap")
    corr = df[numeric_cols].corr()
    st.plotly_chart(px.imshow(corr, text_auto=True, aspect="auto"), use_container_width=True)

if {"Threat_Label", "Country", "Login_Status", "OS", "Browser"}.issubset(df.columns):
    st.markdown("---")
    st.subheader("Cyber Security Insights")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.pie(df, names="Threat_Label", title="Threat vs Safe Logs"), use_container_width=True)
    with c2:
        st.plotly_chart(px.bar(df, x="Login_Status", color="Login_Status", title="Login Status"), use_container_width=True)

    st.plotly_chart(
        px.histogram(df, x="Country", color="Threat_Label", title="Threats by Country"),
        use_container_width=True,
    )
    st.plotly_chart(px.bar(df, x="OS", color="Threat_Label", title="Operating System Analysis"), use_container_width=True)
    st.plotly_chart(px.bar(df, x="Browser", color="Threat_Label", title="Browser Analysis"), use_container_width=True)
