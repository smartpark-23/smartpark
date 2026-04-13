from flask import Blueprint, render_template, session, redirect, request
from db import db

user_booking_bp = Blueprint("user_booking_bp", __name__)

parking_collection = db["parking_slots"]
vehicles_collection = db["vehicles"]


# =========================
# BOOK SLOT
# =========================
@user_booking_bp.route("/user/book_slot", methods=["GET", "POST"])
def book_slot():

    if "user_id" not in session:
        return redirect("/login")

    user_name = session["name"]

    # =========================
    # POST → BOOK SLOT
    # =========================
    if request.method == "POST":

        slot_number = request.form.get("slot_number")
        vehicle_number = request.form.get("vehicle_number")

        parking_collection.update_one(
            {"slot_number": slot_number},
            {
                "$set": {
                    "status": "occupied",
                    "resident_name": user_name,
                    "vehicle_number": vehicle_number
                }
            }
        )

        return redirect("/user/home")


    # =========================
    # GET → SHOW DATA
    # =========================

    # Already allocated vehicles
    allocated_vehicles = parking_collection.distinct(
        "vehicle_number",
        {"status": "occupied"}
    )

    # Show only user's unallocated vehicles
    vehicles = list(vehicles_collection.find({
        "owner_name": user_name,
        "vehicle_number": {"$nin": allocated_vehicles}
    }))

    # Slot type filter
    selected_type = request.args.get("type")

    # 🔥 IMPORTANT CONDITION ADDED
    # only available slots and tower should not be guest
    slot_filter = {
        "status": "available",
        "tower": {"$ne": "GUEST"}
    }

    if selected_type:
        slot_filter["slot_type"] = selected_type

    slots = list(parking_collection.find(slot_filter))

    return render_template(
        "user/book_slot.html",
        slots=slots,
        vehicles=vehicles,
        selected_type=selected_type
    )