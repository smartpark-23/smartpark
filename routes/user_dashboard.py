from flask import Blueprint, render_template, session
from db import db

user_dashboard_bp = Blueprint("user_dashboard_bp", __name__)

vehicles_collection = db["vehicles"]
parking_collection = db["parking_slots"]
guest_collection = db["guest_parking"]


@user_dashboard_bp.route("/user/home")
def user_home():

    # 🔐 Session check
    if "user_id" not in session:
        return "Unauthorized Access"

    user_name = session["name"]

    # Total vehicles
    total_vehicles = vehicles_collection.count_documents({
        "owner_name": user_name
    })

    # My parking slot
    slot_data = parking_collection.find_one({
        "resident_name": user_name,
        "status": "occupied"
    })

    my_slot = slot_data["slot_number"] if slot_data else "Not Allocated"

    # Guest requests
    guest_requests = guest_collection.count_documents({
        "resident_name": user_name
    })

    # Activity
    activity = []
    data = parking_collection.find({
        "resident_name": user_name
    }).limit(5)

    for d in data:
      activity.append({
        "vehicle": d.get("vehicle_number", "-"),
        "slot": d.get("slot_number", "-"),
        "status": d.get("status", "-")
    })
    return render_template(
        "user/user_home.html",
        name=user_name,
        total_vehicles=total_vehicles,
        my_slot=my_slot,
        guest_requests=guest_requests,
        activity=activity
    )