from flask import Blueprint, render_template, session, redirect
from db import db

admin_dashboard_bp = Blueprint("admin_dashboard_bp", __name__)

users_collection = db["users"]
vehicles_collection = db["vehicles"]
parking_collection = db["parking_slots"]
guest_collection = db["guest_parking"]


@admin_dashboard_bp.route("/admin/dashboard")
def admin_dashboard():

    # 🔐 Session check
    if "role" not in session or session["role"] != "admin":
        return redirect("/login")

    # 📊 Stats
    total_residents = users_collection.count_documents({"role": "resident"})
    total_vehicles = vehicles_collection.count_documents({})
    available_slots = parking_collection.count_documents({"status": "available"})
    guest_requests = guest_collection.count_documents({})

    # 🚗 Recent Parking Activity
    activities = []

    data = parking_collection.find({"status": "occupied"}).limit(5)

    for d in data:
        activities.append({
            "vehicle": d.get("vehicle_number", "N/A"),
            "resident": d.get("resident_name", "N/A"),
            "slot": d.get("slot_number", "N/A"),
            "status": "Parked"
        })

    return render_template(
        "admin/admin_dashboard.html",
        admin_name=session.get("name"),
        total_residents=total_residents,
        total_vehicles=total_vehicles,
        available_slots=available_slots,
        guest_requests=guest_requests,
        activities=activities
    )