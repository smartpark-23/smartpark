from flask import Blueprint, render_template, request, redirect, jsonify
from db import db
from bson.objectid import ObjectId

admin_vehicle_bp = Blueprint("admin_vehicle_bp", __name__)

vehicles_collection = db["vehicles"]
users_collection = db["users"]


# =========================
# VIEW VEHICLES
# =========================
@admin_vehicle_bp.route("/admin/vehicles")
def manage_vehicles():

    vehicles = list(vehicles_collection.find())

    return render_template("admin/admin_vehicle.html", vehicles=vehicles)


# =========================
# ADD VEHICLE
# =========================
@admin_vehicle_bp.route("/admin/add_vehicle", methods=["GET","POST"])
def add_vehicle():

    if request.method == "POST":

        vehicle_number = request.form.get("vehicle_number")

        # ✅ Duplicate vehicle check
        if vehicles_collection.find_one({"vehicle_number": vehicle_number}):
            return "Vehicle already exists!"

        data = {
            "vehicle_number": vehicle_number,
            "vehicle_name": request.form.get("vehicle_name"),
            "owner_name": request.form.get("owner_name"),
            "flat": request.form.get("flat"),
            "vehicle_type": request.form.get("vehicle_type"),
            "model": request.form.get("model"),
            "color": request.form.get("color")
        }

        vehicles_collection.insert_one(data)

        return redirect("/admin/vehicles")

    return render_template("admin/admin_add_vehicle.html")


# =========================
# 🔥 AUTO FLAT FETCH API
# =========================
@admin_vehicle_bp.route("/get-flat")
def get_flat():

    owner_name = request.args.get("owner_name")

    user = users_collection.find_one({
        "name": owner_name,
        "role": "resident"
    })

    if user:
        return jsonify({"flat": user.get("flat")})
    else:
        return jsonify({"flat": None})


# =========================
# EDIT VEHICLE
# =========================
@admin_vehicle_bp.route("/admin/edit_vehicle/<id>", methods=["GET","POST"])
def edit_vehicle(id):

    vehicle = vehicles_collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":

        updated_data = {
            "vehicle_number": request.form.get("vehicle_number"),
            "vehicle_name": request.form.get("vehicle_name"),
            "owner_name": request.form.get("owner_name"),
            "vehicle_type": request.form.get("vehicle_type"),
            "model": request.form.get("model"),
            "color": request.form.get("color")
        }

        vehicles_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": updated_data}
        )

        return redirect("/admin/vehicles")

    return render_template("admin/admin_edit_vehicle.html", vehicle=vehicle)


# =========================
# DELETE VEHICLE
# =========================
@admin_vehicle_bp.route("/admin/delete_vehicle/<id>")
def delete_vehicle(id):

    vehicles_collection.delete_one({"_id": ObjectId(id)})

    return redirect("/admin/vehicles")