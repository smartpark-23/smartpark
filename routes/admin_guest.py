from flask import Blueprint, render_template, redirect
from db import db
from bson.objectid import ObjectId

admin_guest_bp = Blueprint("admin_guest_bp", __name__)

guest_collection = db["guest_parking"]


# =========================
# VIEW ALL GUEST REQUESTS
# =========================
@admin_guest_bp.route("/admin/guest_requests")
def guest_requests():

    guests = list(
        guest_collection.find().sort("_id", -1)
    )

    return render_template(
        "admin/admin_guest.html",
        guests=guests
    )


# =========================
# ADMIN APPROVE
# =========================
@admin_guest_bp.route("/admin/final_approve/<id>")
def final_approve(id):

    guest_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "status": "approved",
                "resident_approval": "approved"
            }
        }
    )

    return redirect("/admin/guest_requests")


# =========================
# ADMIN DENY
# =========================
@admin_guest_bp.route("/admin/final_deny/<id>")
def final_deny(id):

    guest_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "status": "denied",
                "resident_approval": "denied"
            }
        }
    )

    return redirect("/admin/guest_requests")


# =========================
# DELETE REQUEST
# =========================
@admin_guest_bp.route("/admin/delete_guest_request/<id>")
def delete_guest_request(id):

    guest_collection.delete_one({
        "_id": ObjectId(id)
    })

    return redirect("/admin/guest_requests")