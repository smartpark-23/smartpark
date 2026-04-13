from flask import Blueprint, render_template, request, redirect, session
from db import db
from bson.objectid import ObjectId

resident_profile_bp = Blueprint("resident_profile_bp", __name__)

users_collection = db["users"]


# =========================
# PROFILE PAGE
# =========================
@resident_profile_bp.route("/resident/profile")
def resident_profile():

    if "user_id" not in session:
        return redirect("/login")

    user = users_collection.find_one({
        "_id": ObjectId(session["user_id"])
    })

    return render_template(
        "user/resident_profile.html",
        user=user
    )


# =========================
# EDIT PROFILE
# =========================
@resident_profile_bp.route("/resident/edit-profile", methods=["GET", "POST"])
def edit_resident_profile():

    if "user_id" not in session:
        return redirect("/login")

    user = users_collection.find_one({
        "_id": ObjectId(session["user_id"])
    })

    if request.method == "POST":

        updated_data = {
    "name": request.form.get("name"),
    "email": request.form.get("email"),
    "phone": request.form.get("phone"),
    "flat": request.form.get("flat")
}

        users_collection.update_one(
            {"_id": ObjectId(session["user_id"])},
            {"$set": updated_data}
        )

        return redirect("/resident/profile")

    return render_template(
        "user/edit_resident_profile.html",
        user=user
    )


# =========================
# CHANGE PASSWORD
# =========================
@resident_profile_bp.route("/resident/change-password", methods=["GET", "POST"])
def change_password():

    if "user_id" not in session:
        return redirect("/login")

    user = users_collection.find_one({
        "_id": ObjectId(session["user_id"])
    })

    error = None

    if request.method == "POST":

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if old_password != user["password"]:
            error = "Old password is incorrect"

        elif new_password != confirm_password:
            error = "Passwords do not match"

        else:
            users_collection.update_one(
                {"_id": ObjectId(session["user_id"])},
                {"$set": {"password": new_password}}
            )

            return redirect("/resident/profile")

    return render_template(
        "user/change_password.html",
        error=error
    )