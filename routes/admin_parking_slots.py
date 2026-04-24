from flask import Blueprint, render_template, redirect
from db import db
from bson.objectid import ObjectId

admin_parking_slot_bp = Blueprint("admin_parking_slot_bp", __name__)

slots_collection = db["parking_slots"]
requests_collection = db["parking_requests"]
users_collection = db["users"]


# =========================
# VIEW SLOTS + REQUESTS
# =========================
@admin_parking_slot_bp.route("/admin/parking_slots")
def manage_slots():

    # 🔥 all slots
    slots = list(slots_collection.find())

    # 🔥 pending requests
    pending_requests = list(
        requests_collection.find({"status": "pending"})
    )

    # 🔥 pending slot numbers
    pending_slot_numbers = [
        r.get("slot_number") for r in pending_requests
    ]

    # 🔥 mark pending status in slots
    for slot in slots:
        slot["status"] = slot.get("status", "available")

        if slot["slot_number"] in pending_slot_numbers:
            slot["status"] = "pending"

    # 🔥 split slots
    normal_slots = [
        s for s in slots if s["status"] != "pending"
    ]

    return render_template(
        "admin/admin_parking_slots.html",
        normal_slots=normal_slots,
        requests=pending_requests
    )


# =========================
# APPROVE REQUEST
# =========================
@admin_parking_slot_bp.route("/admin/approve/<id>")
def approve_request(id):

    req = requests_collection.find_one({"_id": ObjectId(id)})

    if req:
        slot_number = req.get("slot_number")

        # 🔥 update slot → occupied
        slots_collection.update_one(
            {"slot_number": slot_number},
            {
                "$set": {
                    "status": "occupied",
                    "resident_name": req.get("resident_name"),
                    "user_name": req.get("resident_name"),
                    "vehicle_number": req.get("vehicle_number")
                }
            }
        )

        # 🔥 update request → approved
        requests_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": "approved"}}
        )

    return redirect("/admin/parking_slots")


# =========================
# REJECT REQUEST
# =========================
@admin_parking_slot_bp.route("/admin/reject/<id>")
def reject_request(id):

    req = requests_collection.find_one({"_id": ObjectId(id)})

    if req:
        slot_number = req.get("slot_number")

        # 🔥 reset slot → available
        slots_collection.update_one(
            {"slot_number": slot_number},
            {
                "$set": {
                    "status": "available",
                    "resident_name": "",
                    "user_name": "",
                    "vehicle_number": ""
                }
            }
        )

        # 🔥 update request → rejected
        requests_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": "rejected"}}
        )

    return redirect("/admin/parking_slots")