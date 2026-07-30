from xml.sax.saxutils import escape

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


styles = getSampleStyleSheet()


def safe_text(value):
    return escape(str(value))


def create_pdf(username, ip, country, login, prediction, confidence, output_path="Investigation_Report.pdf"):
    pdf = SimpleDocTemplate(output_path)
    story = [
        Paragraph("<b>CyberShield Forensics Report</b>", styles["Title"]),
        Spacer(1, 12),
    ]

    rows = [
        ("Username", username),
        ("IP Address", ip),
        ("Country", country),
        ("Login Status", login),
        ("Prediction", prediction),
        ("Confidence", f"{confidence}%"),
    ]

    for label, value in rows:
        story.append(Paragraph(f"<b>{safe_text(label)}:</b> {safe_text(value)}", styles["Normal"]))
        story.append(Spacer(1, 6))

    pdf.build(story)
