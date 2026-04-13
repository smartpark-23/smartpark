from flask import Blueprint, render_template, send_file
from db import db
import io

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

import matplotlib.pyplot as plt

admin_reports_bp = Blueprint("admin_reports_bp", __name__)

parking_collection = db["parking_slots"]
guest_collection = db["guest_parking"]


# =========================
# REPORT PAGE
# =========================
@admin_reports_bp.route("/admin/reports")
def reports():

    # 🔥 AUTO COUNTS
    total_slots = parking_collection.count_documents({})

    occupied_slots = parking_collection.count_documents({
        "status": {"$regex": "^occupied$", "$options": "i"}
    })

    available_slots = parking_collection.count_documents({
        "status": {"$in": ["available", "free", "Available"]}
    })

    pending_slots = parking_collection.count_documents({
        "status": {"$regex": "^pending$", "$options": "i"}
    })

    total_guests = guest_collection.count_documents({})

    approved_guests = guest_collection.count_documents({
        "status": "approved"
    })

    pending_guests = guest_collection.count_documents({
        "status": "pending"
    })

    denied_guests = guest_collection.count_documents({
        "status": {"$in": ["denied", "rejected"]}
    })

    # 🔥 PIE CHART AUTO DATA
    pie_labels = ["Occupied", "Available", "Pending"]
    pie_data = [
        occupied_slots,
        available_slots,
        pending_slots
    ]

    return render_template(
        "admin/parking_reports.html",
        total_slots=total_slots,
        occupied_slots=occupied_slots,
        available_slots=available_slots,
        pending_slots=pending_slots,
        total_guests=total_guests,
        approved_guests=approved_guests,
        pending_guests=pending_guests,
        denied_guests=denied_guests,
        pie_labels=pie_labels,
        pie_data=pie_data,
    )


# =========================
# PDF EXPORT
# =========================
@admin_reports_bp.route("/admin/reports/pdf")
def export_pdf():

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    content = []

    total_slots = parking_collection.count_documents({})

    occupied_slots = parking_collection.count_documents({
        "status": {"$regex": "^occupied$", "$options": "i"}
    })

    available_slots = parking_collection.count_documents({
        "status": {"$in": ["available", "free", "Available"]}
    })

    pending_slots = parking_collection.count_documents({
        "status": {"$regex": "^pending$", "$options": "i"}
    })

    total_guests = guest_collection.count_documents({})

    # 🔥 TITLE
    content.append(
        Paragraph("<b>SmartPark Parking Report</b>", styles["Title"])
    )
    content.append(Spacer(1, 20))

    # 🔥 TABLE DATA
    table_data = [
        ["Metric", "Value"],
        ["Total Slots", total_slots],
        ["Occupied Slots", occupied_slots],
        ["Available Slots", available_slots],
        ["Pending Slots", pending_slots],
        ["Guest Requests", total_guests]
    ]

    table = Table(table_data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke)
    ]))

    content.append(table)
    content.append(Spacer(1, 25))

    # 🔥 PIE CHART AUTO
    labels = ['Occupied', 'Available', 'Pending']
    sizes = [
        occupied_slots,
        available_slots,
        pending_slots
    ]

    plt.figure(figsize=(5, 5))
    plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%'
    )
    plt.title("Parking Status Overview")

    chart_buffer = io.BytesIO()
    plt.savefig(chart_buffer, format='png')
    plt.close()

    chart_buffer.seek(0)

    img = Image(chart_buffer, width=250, height=250)

    content.append(
        Paragraph("<b>Status Chart</b>", styles["Heading2"])
    )
    content.append(Spacer(1, 10))
    content.append(img)

    doc.build(content)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="SmartPark_Report.pdf",
        mimetype="application/pdf"
    )