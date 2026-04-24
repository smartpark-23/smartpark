from flask import Blueprint, render_template, request, session, redirect
from db import db

user_parking_bp = Blueprint("user_parking_bp", __name__)

slots_collection = db["parking_slots"]
vehicles_collection = db["vehicles"]
requests_collection = db["parking_requests"]


# =========================
# BOOK PARKING SLOT
# =========================
@user_parking_bp.route("/user/book_slot", methods=["GET", "POST"])
def book_slot():

    if "user_id" not in session:
        return redirect("/login")

    user_name = session["name"]

    if request.method == "POST":

        slot_number = request.form.get("slot_number")
        vehicle_number = request.form.get("vehicle_number")

        # 🔥 insert request (PENDING)
        requests_collection.insert_one({
            "resident_name": user_name,
            "vehicle_number": vehicle_number,
            "slot_number": slot_number,
            "status": "pending"
        })

        return redirect("/user/book_slot")

    # 🔥 ONLY AVAILABLE SLOTS
    slots = list(slots_collection.find({"status": "available"}))

    # 🔥 user vehicles
    vehicles = list(vehicles_collection.find({
        "resident_name": user_name
    }))

    return render_template(
        "user/book_slot.html",
        slots=slots,
        vehicles=vehicles
    )