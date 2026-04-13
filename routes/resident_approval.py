from flask import Blueprint, render_template, request, redirect
from db import db
from bson.objectid import ObjectId

resident_bp = Blueprint("resident_bp", __name__)

guest_collection = db["guest_parking"]
users_collection = db["users"]

@resident_bp.route("/resident/approval_form/<id>", methods=["GET", "POST"])
def approval_form(id):

    guest = guest_collection.find_one({"_id": ObjectId(id)})
    users = list(users_collection.find({"role": "resident"}))

    if request.method == "POST":

        resident_name = request.form.get("resident_name")

        guest_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "resident_name": resident_name,
                "resident_approval": "pending"
            }}
        )

        return redirect("/admin/guest_requests")

    return render_template("admin/resident_approval_form.html", guest=guest, users=users)