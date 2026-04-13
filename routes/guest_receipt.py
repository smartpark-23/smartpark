from flask import Blueprint, send_file
from db import db
from bson.objectid import ObjectId
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from io import BytesIO

guest_receipt_bp = Blueprint("guest_receipt_bp", __name__)

guest_collection = db["guest_parking"]


@guest_receipt_bp.route("/download-receipt/<guest_id>")
def download_receipt(guest_id):

    guest = guest_collection.find_one({
        "_id": ObjectId(guest_id)
    })

    if not guest:
        return "Guest record not found"

    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)

    width, height = A4

    # =========================
    # HEADER BAR
    # =========================
    c.setFillColor(HexColor("#16a34a"))
    c.rect(0, height - 80, width, 80, fill=1)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(170, height - 50, "SMARTPARK RECEIPT")

    # =========================
    # INFO BOX
    # =========================
    c.setFillColor(HexColor("#f8fafc"))
    c.roundRect(60, height - 500, 480, 360, 12, fill=1)

    c.setStrokeColor(HexColor("#cbd5e1"))
    c.roundRect(60, height - 500, 480, 360, 12, fill=0)

    # Section Title
    c.setFillColor(HexColor("#2563eb"))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(80, height - 130, "Guest Booking Details")

    # Guest Details
    c.setFillColor(black)
    c.setFont("Helvetica", 12)

    y = height - 170
    gap = 35

    details = [
        f"Guest Name : {guest.get('guest_name', '')}",
        f"Mobile No  : {guest.get('mobile_number', '')}",
        f"Vehicle No : {guest.get('vehicle_no', '')}",
        f"Resident   : {guest.get('resident_name', '')}",
        f"Visit Date : {guest.get('visit_date', '')}",
        f"Slots      : {', '.join(guest.get('selected_slots', []))}",
        f"Status     : {guest.get('status', '')}",
        f"Resident Approval : {guest.get('resident_approval', '')}",
        f"Admin Approval    : {guest.get('admin_approval', '')}"
    ]

    for line in details:
        c.drawString(80, y, line)
        y -= gap

    # =========================
    # FOOTER
    # =========================
    c.setFillColor(HexColor("#16a34a"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(140, 80, "Thank you for visiting SMARTPARK 🚗")

    c.setFillColor(HexColor("#64748b"))
    c.setFont("Helvetica", 10)
    c.drawString(170, 60, "Please keep this receipt for exit verification")

    c.save()
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"SMARTPARK_Receipt_{guest_id}.pdf",
        mimetype="application/pdf"
    )