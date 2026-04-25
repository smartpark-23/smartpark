from flask import Blueprint, render_template, request, redirect
from db import users_collection
from bson.objectid import ObjectId

admin_resident_bp = Blueprint("admin_resident_bp", __name__)

# =========================
# VIEW ALL RESIDENTS
# =========================
@admin_resident_bp.route("/admin/residents")
def manage_residents():

    residents = list(users_collection.find({"role": "resident"}))

    return render_template("admin/admin_resident.html", residents=residents)


# =========================
from flask import Blueprint, render_template, request, redirect, flash
from db import db

admin_resident_bp = Blueprint("admin_resident_bp", __name__)

users_collection = db["users"]
towers_collection = db["towers"]   # 🔥 towers use


# =========================
# ADD RESIDENT
# =========================
@admin_resident_bp.route("/admin/add_resident", methods=["GET", "POST"])
def add_resident():

    # 🔥 Fetch towers (A / B)
    towers_data = towers_collection.find()
    towers = [t.get("tower") for t in towers_data]

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        tower = request.form.get("tower")   # 🔥 flat → tower

        # ✅ Validation
        if not name or not email or not phone or not tower:
            flash("All fields are required!", "danger")
            return redirect("/admin/add_resident")

        # ✅ Duplicate email
        if users_collection.find_one({"email": email}):
            flash("Email already exists!", "warning")
            return redirect("/admin/add_resident")

        # ✅ Insert
        users_collection.insert_one({
            "name": name,
            "email": email,
            "phone": phone,
            "tower": tower,   # 🔥 store tower
            "role": "resident"
        })

        flash("Resident added successfully!", "success")
        return redirect("/admin/residents")

    return render_template(
        "admin/admin_add_resident.html",
        towers=towers
    )


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
            "flat": request.form.get("flat")
        }

        users_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": updated_data}
        )

        return redirect("/admin/residents")

    return render_template("admin/admin_edit_resident.html", user=user)


# =========================
# DELETE RESIDENT
# =========================
@admin_resident_bp.route("/admin/delete_resident/<id>")
def delete_resident(id):

    users_collection.delete_one({"_id": ObjectId(id)})

    return redirect("/admin/residents")