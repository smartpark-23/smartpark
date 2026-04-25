from flask import Blueprint, render_template, request, redirect, flash, url_for
from db import db
from bson.objectid import ObjectId

admin_resident_bp = Blueprint("admin_resident_bp", __name__)

users_collection = db["users"]
towers_collection = db["towers"]


# =========================
# VIEW ALL RESIDENTS
# =========================
@admin_resident_bp.route("/admin/residents")
def manage_residents():

    residents = list(users_collection.find({"role": "resident"}))

    return render_template("admin/admin_resident.html", residents=residents)


# =========================
# ADD RESIDENT
# =========================
@admin_resident_bp.route("/admin/add_resident", methods=["GET", "POST"])
def add_resident():

    towers_data = towers_collection.find()
    towers = [t.get("tower") for t in towers_data]

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        tower = request.form.get("tower")

        if not name or not email or not phone or not tower:
            flash("All fields are required!", "danger")
            return redirect(url_for("admin_resident_bp.add_resident"))

        if users_collection.find_one({"email": email}):
            flash("Email already exists!", "warning")
            return redirect(url_for("admin_resident_bp.add_resident"))

        users_collection.insert_one({
            "name": name,
            "email": email,
            "phone": phone,
            "tower": tower,
            "role": "resident"
        })

        flash("Resident added successfully!", "success")
        return redirect(url_for("admin_resident_bp.manage_residents"))

    return render_template("admin/admin_add_resident.html", towers=towers)


# =========================
# EDIT RESIDENT
# =========================
@admin_resident_bp.route("/admin/edit_resident/<id>", methods=["GET","POST"])
def edit_resident(id):

    user = users_collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":

        updated_data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "tower": request.form.get("tower")   # 🔥 FIX (flat → tower)
        }

        users_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": updated_data}
        )

        return redirect(url_for("admin_resident_bp.manage_residents"))

    return render_template("admin/admin_edit_resident.html", user=user)


# =========================
# DELETE RESIDENT
# =========================
@admin_resident_bp.route("/admin/delete_resident/<id>")
def delete_resident(id):

    users_collection.delete_one({"_id": ObjectId(id)})

    return redirect(url_for("admin_resident_bp.manage_residents"))