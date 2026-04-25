from flask import Blueprint, render_template, request, redirect
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

    slots = list(slots_collection.find())

    pending_requests = list(
        requests_collection.find({"status": "pending"})
    )

    pending_slot_numbers = [
        r.get("slot_number") for r in pending_requests
    ]

    for slot in slots:
        slot["status"] = slot.get("status", "available")

        if slot["slot_number"] in pending_slot_numbers:
            slot["status"] = "pending"

    normal_slots = [
        s for s in slots if s["status"] != "pending"
    ]

    return render_template(
        "admin/admin_parking_slots.html",
        normal_slots=normal_slots,
        requests=pending_requests
    )


# =========================
# ADD SLOT
# =========================
@admin_parking_slot_bp.route("/admin/add_parking_slot", methods=["GET", "POST"])
def add_slot():

    if request.method == "POST":

        slot_data = {
            "slot_number": request.form.get("slot_number"),
            "tower": request.form.get("tower"),
            "floor": request.form.get("floor"),
            "slot_type": request.form.get("slot_type"),
            "status": "available",
            "resident_name": "",
            "user_name": "",
            "vehicle_number": ""
        }

        slots_collection.insert_one(slot_data)

        return redirect("/admin/parking_slots")

    return render_template("admin/admin_add_parking_slot.html")


# =========================
# EDIT SLOT
# =========================
@admin_parking_slot_bp.route("/admin/edit_parking_slot/<id>", methods=["GET", "POST"])
def edit_slot(id):

    slot = slots_collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":

        user_name = request.form.get("user_name", "")
        vehicle_number = request.form.get("vehicle_number", "")

        status = "occupied" if user_name else "available"

        slots_collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "user_name": user_name,
                    "resident_name": user_name,
                    "vehicle_number": vehicle_number,
                    "status": status
                }
            }
        )

        return redirect("/admin/parking_slots")

    return render_template("admin/admin_edit_parking_slot.html", slot=slot)


# =========================
# DELETE SLOT
# =========================
@admin_parking_slot_bp.route("/admin/delete_slot/<id>")
def delete_slot(id):

    slots_collection.delete_one({"_id": ObjectId(id)})

    return redirect("/admin/parking_slots")


# =========================
# APPROVE REQUEST
# =========================
@admin_parking_slot_bp.route("/admin/approve/<id>")
def approve_request(id):

    req = requests_collection.find_one({"_id": ObjectId(id)})

    if req:
        slot_number = req.get("slot_number")

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