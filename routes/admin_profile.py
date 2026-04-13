from flask import Blueprint, render_template, request, redirect
from db import db

admin_profile_bp = Blueprint("admin_profile_bp", __name__)

admin_collection = db["users"]   # assuming admin also in users


# ======================
# PROFILE PAGE
# ======================
@admin_profile_bp.route("/admin/profile")
def admin_profile():

    admin = admin_collection.find_one({"role": "admin"})

    return render_template("admin/admin_profile.html", admin=admin)


# ======================
# EDIT PROFILE
# ======================
@admin_profile_bp.route("/admin/profile/edit", methods=["GET", "POST"])
def edit_profile():

    admin = admin_collection.find_one({"role": "admin"})

    if request.method == "POST":

        updated_data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "location": request.form.get("location")
        }

        admin_collection.update_one(
            {"role": "admin"},
            {"$set": updated_data}
        )

        return redirect("/admin/profile")

    return render_template("admin/admin_edit_profile.html", admin=admin)