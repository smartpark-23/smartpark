from flask import Blueprint, render_template
from db import db

guest_parking_bp = Blueprint("guest_parking_bp", __name__)

parking_collection = db["parking_slots"]


@guest_parking_bp.route("/")
def guest_homepage():

    free_slots = list(
        parking_collection.find({"status": "available"})
    )

    free_count = len(free_slots)

    return render_template(
        "guest_homepage.html",
        free_count=free_count
    )
    # =========================
# SLOTS PAGE
# =========================
@guest_parking_bp.route("/slots")
def slots_page():

    all_slots = list(parking_collection.find())

    return render_template(
        "slots_page.html",
        all_slots=all_slots
    )