"""
pdf_generator.py - Example PDF reporting using ReportLab
"""

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def generate_pdf_report(results, output_file="ssh_audit_report.pdf"):
    c = canvas.Canvas(output_file, pagesize=LETTER)
    c.setFont("Helvetica", 12)

    c.drawString(30, 750, "SSH Configuration Audit Report")
    y_position = 700
    for key, value in results.items():
        c.drawString(30, y_position, f"{key}: {value}")
        y_position -= 20

    c.save()
    return output_file

