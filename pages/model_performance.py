import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from utils.auth import require_login
from utils.ui import render_page_header


require_login()


@st.cache_data
def load_dataset():
    df = pd.read_csv("datasets/sample_logs.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Year"] = df["Timestamp"].dt.year
    df["Month"] = df["Timestamp"].dt.month
    df["Day"] = df["Timestamp"].dt.day
    df["Hour"] = df["Timestamp"].dt.hour
    return df.drop(columns=["Timestamp"])


@st.cache_resource
def load_artifacts():
    return joblib.load("models/cyber_model.pkl"), joblib.load("models/encoders.pkl")


render_page_header(
    "◉",
    "ML Model Performance",
    "Review model accuracy, confusion matrix, and classification metrics for the saved detector.",
    "Model Audit",
)

try:
    df = load_dataset()
    model, encoders = load_artifacts()
except Exception as exc:
    st.error(f"Could not load model performance assets: {exc}")
    st.stop()

encoded_df = df.copy()
for column, encoder in encoders.items():
    if column in encoded_df.columns:
        encoded_df[column] = encoder.transform(encoded_df[column].astype(str))

X = encoded_df.drop(columns=["Threat_Label", "Log_ID"])
y = encoded_df["Threat_Label"]

try:
    predictions = model.predict(X)
except Exception as exc:
    st.error(f"Could not run model evaluation: {exc}")
    st.stop()

accuracy = accuracy_score(y, predictions)

c1, c2, c3 = st.columns(3)
c1.metric("Dataset Rows", len(df))
c2.metric("Features", X.shape[1])
c3.metric("Accuracy", f"{accuracy * 100:.2f}%")

labels = encoders["Threat_Label"].classes_.tolist()
matrix = confusion_matrix(y, predictions)
matrix_df = pd.DataFrame(matrix, index=labels, columns=labels)

st.subheader("Confusion Matrix")
fig = px.imshow(matrix_df, text_auto=True, aspect="auto", labels=dict(x="Predicted", y="Actual"))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Classification Report")
report = classification_report(y, predictions, target_names=labels, output_dict=True)
st.dataframe(pd.DataFrame(report).transpose(), use_container_width=True)

st.subheader("Sample Data")
st.dataframe(df.head(20), use_container_width=True)
