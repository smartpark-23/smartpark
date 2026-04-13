from flask import Blueprint, render_template, request, redirect, session
from db import db

user_guest_bp = Blueprint("user_guest_bp", __name__)

guest_collection = db["guest_parking"]
parking_collection = db["parking_slots"]


# =========================
# GUEST REQUEST BY RESIDENT
# =========================
@user_guest_bp.route("/user/guest_request", methods=["GET", "POST"])
def guest_request():

    # Login check
    if "user_id" not in session:
        return redirect("/login")

    # =========================
    # POST → DIRECT APPROVED
    # =========================
    if request.method == "POST":

        guest_name = request.form.get("guest_name")
        mobile_number = request.form.get("mobile_number")
        vehicle_number = request.form.get("vehicle_number")
        visit_date = request.form.get("visit_date")

        selected_slots = request.form.getlist("selected_slots")

        # 🔥 Resident request = direct approved
        guest_collection.insert_one({
            "guest_name": guest_name,
            "mobile_number": mobile_number,
            "vehicle_no": vehicle_number,
            "resident_name": session["name"],
            "visit_date": visit_date,
            "selected_slots": selected_slots,
            "slots_required": len(selected_slots),

            "status": "approved",
            "resident_approval": "approved",
            "request_sent_by": "user"
        })

        # 🔥 selected slots occupied
        if selected_slots:
            parking_collection.update_many(
                {"slot_number": {"$in": selected_slots}},
                {"$set": {"status": "occupied"}}
            )

        return redirect("/user/home")

    # =========================
    # GET → SHOW FREE GUEST SLOTS
    # =========================
    free_slots = list(parking_collection.find({
        "status": {"$in": ["available", "free"]},
        "tower": {"$regex": "^guest$", "$options": "i"}
    }))

    return render_template(
        "user/guest_request.html",
        free_slots=free_slots
    )