from flask import Blueprint, render_template, request, redirect
from db import db
from bson.objectid import ObjectId

admin_parking_slot_bp = Blueprint("admin_parking_slot_bp", __name__)

slots_collection = db["parking_slots"]
users_collection = db["users"]
requests_collection = db["parking_requests"]


# =========================
# VIEW SLOTS + REQUESTS
# =========================
@admin_parking_slot_bp.route("/admin/parking_slots")
def manage_slots():

    slots = list(slots_collection.find())

    # normalize status for UI
    for slot in slots:
        slot["status"] = slot.get("status", "available").lower().strip()

    requests = list(
        requests_collection.find({"status": "pending"})
    )

    return render_template(
        "admin/admin_parking_slots.html",
        slots=slots,
        requests=requests
    )


# =========================
# ADD PARKING SLOT
# =========================
@admin_parking_slot_bp.route("/admin/add_parking_slot", methods=["GET", "POST"])
def add_parking_slot():

    residents = list(
        users_collection.find({"role": "resident"})
    )

    if request.method == "POST":

        slot_number = request.form.get("slot_number")
        tower = request.form.get("tower")
        floor = request.form.get("floor")
        slot_type = request.form.get("slot_type")
        user_name = request.form.get("user_name", "").strip()

        # auto status based on resident selection
        if user_name:
            status = "occupied"
            resident_name = user_name
        else:
            status = "available"
            resident_name = ""

        slot_data = {
            "slot_number": slot_number,
            "tower": tower,
            "floor": floor,
            "slot_type": slot_type,
            "status": status,
            "resident_name": resident_name,
            "user_name": user_name,
            "vehicle_number": ""
        }

        slots_collection.insert_one(slot_data)

        return redirect("/admin/parking_slots")

    return render_template(
        "admin/admin_add_parking_slot.html",
        residents=residents
    )


# =========================
# APPROVE REQUEST
# =========================
@admin_parking_slot_bp.route("/admin/approve/<id>")
def approve_request(id):

    req = requests_collection.find_one({"_id": ObjectId(id)})

    if req:
        slot_number = req.get("slot_number")
        resident_name = req.get("resident_name", "")
        vehicle_number = req.get("vehicle_number", "")

        # AUTO UPDATE SLOT
        slots_collection.update_one(
            {"slot_number": slot_number},
            {
                "$set": {
                    "status": "occupied",
                    "resident_name": resident_name,
                    "user_name": resident_name,
                    "vehicle_number": vehicle_number
                }
            }
        )

        # UPDATE REQUEST STATUS
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

        # RESET SLOT
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

        requests_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": "rejected"}}
        )

    return redirect("/admin/parking_slots")