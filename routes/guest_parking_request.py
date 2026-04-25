from flask import Blueprint, render_template, request, redirect, url_for
from db import db

guest_request_bp = Blueprint("guest_request_bp", __name__)

guest_collection = db["guest_parking"]
parking_collection = db["parking_slots"]


# =========================
# GUEST PARKING FORM
# =========================
@guest_request_bp.route("/guest-parking", methods=["GET", "POST"])
def guest_parking_form():

    # ✅ FIX: Proper query for available guest slots
    free_slots = list(parking_collection.find({
        "status": {"$in": ["free", "available", "Available"]},
        "$or": [
            {"slot_type": {"$regex": "guest", "$options": "i"}},
            {"tower": {"$regex": "guest", "$options": "i"}}
        ]
    }))

    print("FREE SLOTS:", free_slots)  # 🔥 DEBUG (check terminal)

    if request.method == "POST":

        guest_name = request.form.get("guest_name")
        mobile_number = request.form.get("mobile_number")
        vehicle_number = request.form.get("vehicle_number")
        resident_name = request.form.get("resident_name")
        visit_date = request.form.get("visit_date")

        selected_slots = request.form.getlist("selected_slots")

        # ❌ if no slot selected
        if len(selected_slots) == 0:
            return render_template(
                "guest_parking_form.html",
                free_slots=free_slots,
                error="⚠️ Please select at least one slot"
            )

        guest_data = {
            "guest_name": guest_name,
            "mobile_number": mobile_number,
            "vehicle_no": vehicle_number,
            "resident_name": resident_name.strip(),
            "visit_date": visit_date,
            "selected_slots": selected_slots,
            "slots_required": len(selected_slots),

            # approval system
            "status": "pending",
            "resident_approval": "pending",
            "request_sent_by": "guest"
        }

        # ✅ Insert booking
        guest_collection.insert_one(guest_data)

        # ✅ OPTIONAL: mark slots as temporary booked
        parking_collection.update_many(
            {"slot_number": {"$in": selected_slots}},
            {"$set": {"status": "pending"}}
        )

        return redirect(url_for("guest_request_bp.track_request"))

    return render_template(
        "guest_parking_form.html",
        free_slots=free_slots
    )


# =========================
# TRACK REQUEST
# =========================
@guest_request_bp.route("/guest-access", methods=["GET", "POST"])
def track_request():

    error = None

    if request.method == "POST":

        mobile_number = request.form.get("mobile_number")
        vehicle_no = request.form.get("vehicle_no")

        guest = guest_collection.find_one({
            "mobile_number": mobile_number,
            "vehicle_no": vehicle_no
        })

        if guest:
            return redirect(f"/guest-dashboard/{str(guest['_id'])}")
        else:
            error = "❌ Invalid Mobile Number or Vehicle Number"

    return render_template(
        "guest_access.html",
        error=error
    )