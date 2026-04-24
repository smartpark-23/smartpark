from flask import Blueprint, render_template, request, session, redirect
from db import db

user_parking_bp = Blueprint("user_parking_bp", __name__)

slots_collection = db["parking_slots"]
vehicles_collection = db["vehicles"]
requests_collection = db["parking_requests"]


@user_parking_bp.route("/user/book_slot", methods=["GET", "POST"])
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

        # 🔥 duplicate request avoid
        existing = requests_collection.find_one({
            "resident_name": user_name,
            "status": "pending"
        })

        if existing:
            return redirect("/user/book_slot")

        # 🔥 slot ne pending karo
        slots_collection.update_one(
            {"slot_number": slot_number},
            {"$set": {"status": "pending"}}
        )

        # 🔥 request insert
        requests_collection.insert_one({
            "slot_number": slot_number,
            "tower": "",
            "resident_name": user_name,
            "user_id": session["user_id"],
            "vehicle_number": vehicle_number,
            "vehicle_type": "",
            "status": "pending",
            "request_type": "resident"
        })

        return redirect("/user/book_slot")

    # =========================
    # ONLY AVAILABLE SLOTS
    # =========================
    slots = list(slots_collection.find({"status": "available"}))

    # 🔥 CORRECT MATCH (IMPORTANT)
    vehicles = list(vehicles_collection.find({
        "owner_name": user_name
    }))

    return render_template(
        "user/book_slot.html",
        slots=slots,
        vehicles=vehicles
    )