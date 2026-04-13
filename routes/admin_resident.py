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
# ADD RESIDENT
@admin_resident_bp.route("/admin/add_resident", methods=["GET", "POST"])
def add_resident():

    # 🔽 Fetch flats from DB
    flats_data = users_collection.find()
    flats = [f.get("flat") for f in flats_data]

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        flat = request.form.get("flat")

        # ✅ Validation
        if not name or not email or not phone or not flat:
            flash("All fields are required!", "danger")
            return redirect("/admin/add_resident")

        # ✅ Duplicate email check
        if users_collection.find_one({"email": email}):
            flash("Email already exists!", "warning")
            return redirect("/admin/add_resident")

        # ✅ Insert
        users_collection.insert_one({
            "name": name,
            "email": email,
            "phone": phone,
            "flat": flat,
            "role": "resident"
        })

        flash("Resident added successfully!", "success")
        return redirect("/admin/residents")

    return render_template(
        "admin/admin_add_resident.html",
        flats=flats   # 🔽 send to HTML
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