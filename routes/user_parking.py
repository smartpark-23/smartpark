from flask import Blueprint, render_template, session, redirect
from db import db

user_parking_bp = Blueprint("user_parking_bp", __name__)

parking_collection = db["parking_slots"]


# =========================
# PARKING STATUS
# =========================
@user_parking_bp.route("/user/parking_status")
def parking_status():

    if "user_id" not in session:
        return redirect("/login")

    user_name = session["name"]

    slot = parking_collection.find_one({
        "resident_name": user_name,
        "status": "occupied"
    })

    return render_template(
        "user/parking_status.html",
        slot=slot
    )