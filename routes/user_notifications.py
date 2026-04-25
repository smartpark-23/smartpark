from flask import Blueprint, render_template, session, redirect, request
from db import db
from bson import ObjectId

user_notifications_bp = Blueprint("user_notifications_bp", __name__)

guest_collection = db["guest_parking"]
parking_collection = db["parking_slots"]


# =========================
# NOTIFICATIONS PAGE
# =========================
@user_notifications_bp.route("/user/notifications")
def notifications():

    if "user_id" not in session:
        return redirect("/login")

    # 🔥 show only guest requests pending for this resident
    requests = list(guest_collection.find({
        "resident_name": {"$regex": f"^{session['name']}$", "$options": "i"},
        "resident_approval": "pending",
        "request_sent_by": "guest"
    }))

    return render_template(
        "user/user_notifications.html",
        requests=requests
    )


# =========================
# APPROVE / DENY ACTION
# =========================
@user_notifications_bp.route("/user/guest_action", methods=["POST"])
def guest_action():

    if "user_id" not in session:
        return redirect("/login")

    req_id = request.form.get("id")
    action = request.form.get("action")

    if req_id and action in ["yes", "no"]:

        request_data = guest_collection.find_one({
            "_id": ObjectId(req_id)
        })

        if action == "yes":

            # 🔥 request approved
            guest_collection.update_one(
                {"_id": ObjectId(req_id)},
                {
                    "$set": {
                        "resident_approval": "approved",
                        "status": "approved"
                    }
                }
            )

            # 🔥 selected slots occupied
            if request_data and request_data.get("selected_slots"):
                parking_collection.update_many(
                    {
                        "slot_number": {
                            "$in": request_data["selected_slots"]
                        }
                    },
                    {
                        "$set": {
                            "status": "occupied"
                        }
                    }
                )

        else:
            # 🔥 denied
            guest_collection.update_one(
                {"_id": ObjectId(req_id)},
                {
                    "$set": {
                        "resident_approval": "denied",
                        "status": "denied"
                    }
                }
            )

    return redirect("/user/notifications")
