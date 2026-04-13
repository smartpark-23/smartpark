from flask import Blueprint, render_template, redirect, request
from db import db
from bson.objectid import ObjectId

guest_dashboard_bp = Blueprint("guest_dashboard_bp", __name__)

guest_collection = db["guest_parking"]
parking_collection = db["parking_slots"]


# =========================
# GUEST DASHBOARD
# =========================
@guest_dashboard_bp.route("/guest-dashboard/<guest_id>")
def guest_dashboard(guest_id):

    guest = guest_collection.find_one({
        "_id": ObjectId(guest_id)
    })

    if not guest:
        return redirect("/guest-access")

    return render_template(
        "guest_dashboard.html",
        guest=guest
    )


# =========================
# CANCEL REQUEST
# =========================
@guest_dashboard_bp.route("/cancel-request/<guest_id>")
def cancel_request(guest_id):

    guest = guest_collection.find_one({
        "_id": ObjectId(guest_id)
    })

    if not guest:
        return redirect("/guest-access")

    selected_slots = guest.get("selected_slots", [])

    # free slots
    if selected_slots:
        parking_collection.update_many(
            {"slot_number": {"$in": selected_slots}},
            {"$set": {"status": "free"}}
        )

    # update guest status
    guest_collection.update_one(
        {"_id": ObjectId(guest_id)},
        {
            "$set": {
                "status": "cancelled",
                "resident_approval": "cancelled",
                "admin_approval": "cancelled"
            }
        }
    )

    return redirect(f"/guest-dashboard/{guest_id}")


# =========================
# EXIT VERIFICATION
# =========================
@guest_dashboard_bp.route("/guest-exit/<guest_id>", methods=["GET", "POST"])
def guest_exit_verification(guest_id):

    guest = guest_collection.find_one({
        "_id": ObjectId(guest_id)
    })

    if not guest:
        return redirect("/guest-access")

    if request.method == "POST":

        vehicle_no = request.form.get("vehicle_no")
        vehicle_type = request.form.get("vehicle_type")
        slot_number = request.form.get("slot_number")

        # request must be approved
        if guest["status"] != "approved":
            return render_template(
                "guest_exit_verification.html",
                error="Exit denied. Request is not approved."
            )

        # vehicle validation
        if vehicle_no != guest["vehicle_no"]:
            return render_template(
                "guest_exit_verification.html",
                error="Vehicle number mismatch."
            )

        # slot validation
        if slot_number not in guest.get("selected_slots", []):
            return render_template(
                "guest_exit_verification.html",
                error="Slot number mismatch."
            )

        # update status
        guest_collection.update_one(
            {"_id": ObjectId(guest_id)},
            {
                "$set": {
                    "status": "checked_out"
                }
            }
        )

        # free slot
        parking_collection.update_one(
            {"slot_number": slot_number},
            {
                "$set": {
                    "status": "free"
                }
            }
        )

        return render_template(
            "guest_exit_verification.html",
            success="Thank you for visiting SMARTPARK. Exit successful."
        )

    return render_template("guest_exit_verification.html")