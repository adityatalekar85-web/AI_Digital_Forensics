import os
import re
import tempfile


def send_email(username, country, prediction, confidence):
    sender = os.getenv("ALERT_EMAIL")
    password = os.getenv("ALERT_EMAIL_PASSWORD")
    recipient = os.getenv("ALERT_EMAIL_TO", sender or "")

    if not sender or not password or not recipient:
        return False, "Email alert is not configured."

    try:
        import yagmail

        yag = yagmail.SMTP(sender, password)
        subject = "CyberShield Forensics Alert"
        body = f"""
Threat Detected

Username: {username}
Country: {country}
Prediction: {prediction}
Confidence: {confidence}%
"""

        yag.send(to=recipient, subject=subject, contents=body)
        return True, "Threat alert email sent."
    except Exception as exc:
        return False, f"Email alert failed: {exc}"


def send_file_email(recipient, subject, body, filename, file_bytes, sender=None, password=None):
    sender = (sender or os.getenv("ALERT_EMAIL") or "").strip()
    password = (password or os.getenv("ALERT_EMAIL_PASSWORD") or "").strip()
    recipient = recipient.strip()

    if not recipient:
        return False, "Please enter recipient email."
    if "@" not in recipient or "." not in recipient.split("@")[-1]:
        return False, "Please enter a valid recipient email."
    if not sender or not password:
        return False, "Enter sender email and app password, or set ALERT_EMAIL and ALERT_EMAIL_PASSWORD."

    try:
        import yagmail

        safe_filename = re.sub(r"[^A-Za-z0-9_.-]", "_", filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{safe_filename}") as attachment:
            attachment.write(file_bytes)
            attachment_path = attachment.name

        yag = yagmail.SMTP(sender, password)
        yag.send(
            to=recipient,
            subject=subject,
            contents=body,
            attachments=attachment_path,
        )
        return True, f"File sent to {recipient}."
    except Exception as exc:
        return False, f"Email failed: {exc}"
    finally:
        try:
            if "attachment_path" in locals():
                os.remove(attachment_path)
        except OSError:
            pass


def get_email_configured():
    return bool(os.getenv("ALERT_EMAIL") and os.getenv("ALERT_EMAIL_PASSWORD"))
