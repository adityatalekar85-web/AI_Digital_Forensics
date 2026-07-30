import streamlit as st

from utils.email_alert import get_email_configured, send_file_email


def render_email_sender(key_prefix, label, subject, body, filename, file_bytes):
    with st.expander(label):
        recipient = st.text_input("Recipient email", key=f"{key_prefix}_recipient")

        if get_email_configured():
            sender = None
            password = None
            st.caption("Using configured sender email.")
        else:
            st.caption("Enter Gmail/App SMTP credentials to send this file.")
            sender = st.text_input("Sender email", key=f"{key_prefix}_sender")
            password = st.text_input("Sender app password", type="password", key=f"{key_prefix}_password")

        if st.button("Send Email", key=f"{key_prefix}_send", use_container_width=True):
            sent, message = send_file_email(
                recipient=recipient,
                subject=subject,
                body=body,
                filename=filename,
                file_bytes=file_bytes,
                sender=sender,
                password=password,
            )
            if sent:
                st.success(message)
            else:
                st.error(message)
