from flask import Blueprint, render_template, request, session, redirect, flash
from db import db
user_booking_bp = Blueprint("user_booking_bp", __name__)

slots_collection = db["parking_slots"]
vehicles_collection = db["vehicles"]
requests_collection = db["parking_requests"]


@user_booking_bp.route("/user/book_slot", methods=["GET", "POST"])
def book_slot():

    if "user_id" not in session:
        return redirect("/login")

    user_name = session.get("name")

    # =========================
    # POST → SEND REQUEST
    # =========================
    if request.method == "POST":

        slot_number = request.form.get("slot_number")
        vehicle_number = request.form.get("vehicle_number")

        existing = requests_collection.find_one({
            "resident_name": user_name,
            "status": "pending"
        })

        if existing:
            flash("You already have a pending request!", "warning")
            return redirect("/user/book_slot")

        # slot → pending
        slots_collection.update_one(
            {"slot_number": slot_number},
            {"$set": {"status": "pending"}}
        )

        # request insert
        requests_collection.insert_one({
            "slot_number": slot_number,
            "resident_name": user_name,
            "vehicle_number": vehicle_number,
            "status": "pending"
        })

        flash("Request sent successfully!", "success")
        return redirect("/user/book_slot")

    # =========================
    # FILTER
    # =========================
    selected_type = request.args.get("type")

    query = {
        "status": "available",
        "tower": {"$in": ["A", "B"]}
    }

    if selected_type:
        query["slot_type"] = selected_type

    slots = list(slots_collection.find(query))

    # =========================
    # VEHICLE FILTER
    # =========================
    assigned_vehicles = slots_collection.distinct("vehicle_number", {
        "status": {"$in": ["occupied", "pending"]}
    })

    vehicles = list(vehicles_collection.find({
        "owner_name": user_name,
        "vehicle_number": {"$nin": assigned_vehicles}
    }))

    # =========================
    # USER REQUEST STATUS
    # =========================
    user_request = requests_collection.find_one(
        {"resident_name": user_name},
        sort=[("_id", -1)]
    )

    return render_template(
        "user/book_slot.html",
        slots=slots,
        vehicles=vehicles,
        selected_type=selected_type,
        user_request=user_request
    )