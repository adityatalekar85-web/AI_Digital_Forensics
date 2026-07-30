from datetime import datetime

import joblib
import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.database import save_prediction
from utils.email_alert import send_email
from utils.email_delivery import render_email_sender
from utils.pdf_report import create_pdf
from utils.ui import render_page_header


require_login()


@st.cache_resource
def load_artifacts():
    model = joblib.load("models/cyber_model.pkl")
    encoders = joblib.load("models/encoders.pkl")
    return model, encoders


def safe_encode(encoders, column, value):
    encoder = encoders[column]
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    return 0


render_page_header(
    "◆",
    "ML Threat Detection",
    "Classify login events with the trained cyber threat model and generate investigation reports.",
    "Prediction",
)

try:
    model, encoders = load_artifacts()
except Exception as exc:
    st.error(f"Could not load ML model files: {exc}")
    st.stop()

with st.form("prediction_form"):
    st.subheader("Security Log Details")

    c1, c2 = st.columns(2)
    with c1:
        username = st.text_input("Username", "admin")
        ip = st.text_input("IP Address", "192.168.1.10")
        country = st.selectbox("Country", encoders["Country"].classes_)
        login = st.selectbox("Login Status", encoders["Login_Status"].classes_)
        failed_attempts = st.slider("Failed Attempts", 0, 10, 0)

    with c2:
        device = st.selectbox("Device", encoders["Device"].classes_)
        os_name = st.selectbox("Operating System", encoders["OS"].classes_)
        browser = st.selectbox("Browser", encoders["Browser"].classes_)
        attack = st.selectbox("Attack Type", encoders["Attack_Type"].classes_)
        risk_score = st.slider("Risk Score", 0, 100, 50)

    submitted = st.form_submit_button("Predict Threat")

if not submitted:
    st.stop()

now = datetime.now()
input_data = pd.DataFrame(
    [
        {
            "Username": safe_encode(encoders, "Username", username),
            "IP_Address": safe_encode(encoders, "IP_Address", ip),
            "Country": safe_encode(encoders, "Country", country),
            "Login_Status": safe_encode(encoders, "Login_Status", login),
            "Failed_Attempts": failed_attempts,
            "Device": safe_encode(encoders, "Device", device),
            "OS": safe_encode(encoders, "OS", os_name),
            "Browser": safe_encode(encoders, "Browser", browser),
            "Risk_Score": risk_score,
            "Attack_Type": safe_encode(encoders, "Attack_Type", attack),
            "Year": now.year,
            "Month": now.month,
            "Day": now.day,
            "Hour": now.hour,
        }
    ]
)

try:
    prediction = int(model.predict(input_data)[0])
    probability = model.predict_proba(input_data)
    confidence = round(float(max(probability[0])) * 100, 2)
except Exception as exc:
    st.error(f"Prediction Error: {exc}")
    st.stop()

prediction_text = "Threat" if prediction == 1 else "Safe"

result_col, confidence_col = st.columns(2)
if prediction_text == "Threat":
    result_col.error("THREAT DETECTED")
else:
    result_col.success("SAFE LOGIN")

confidence_col.metric("Prediction Confidence", f"{confidence}%")

if prediction_text == "Threat":
    sent, message = send_email(username, country, prediction_text, confidence)
    if sent:
        st.success(message)
    else:
        st.info(message)

save_prediction(username, ip, country, login, prediction_text, confidence)
create_pdf(username, ip, country, login, prediction_text, confidence)

with open("Investigation_Report.pdf", "rb") as file:
    pdf_bytes = file.read()

download_col, email_col = st.columns(2)
with download_col:
    st.download_button(
        "Download Investigation Report",
        pdf_bytes,
        file_name="Investigation_Report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

with email_col:
    render_email_sender(
        "prediction_pdf",
        "Send PDF Report to Email",
        "CyberShield Investigation PDF Report",
        "Attached is your CyberShield Forensics investigation PDF report.",
        "Investigation_Report.pdf",
        pdf_bytes,
    )

st.success("Prediction saved successfully")
