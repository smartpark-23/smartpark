from flask import Blueprint, render_template, request, redirect, session
from db import db
from bson.objectid import ObjectId

user_vehicle_bp = Blueprint("user_vehicle_bp", __name__)

vehicles_collection = db["vehicles"]


# =========================
# VIEW VEHICLES
# =========================
@user_vehicle_bp.route("/user/vehicles")
def user_vehicles():

    if "user_id" not in session:
        return redirect("/login")

    name = session["name"]

    vehicles = list(vehicles_collection.find({
        "owner_name": name
    }))

    return render_template("user/user_vehicles.html", vehicles=vehicles)


# =========================
# ADD VEHICLE
# =========================
@user_vehicle_bp.route("/user/add_vehicle", methods=["GET", "POST"])
def add_vehicle():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        vehicle_data = {
            "owner_name": session["name"],

            "vehicle_number": request.form.get("vehicle_number"),
            "vehicle_name": request.form.get("vehicle_name"),
            "vehicle_type": request.form.get("vehicle_type"),
            "model": request.form.get("model"),
            "color": request.form.get("color")
        }

        vehicles_collection.insert_one(vehicle_data)

        return redirect("/user/vehicles")

    return render_template("user/add_vehicle.html")


# =========================
# DELETE VEHICLE
# =========================
@user_vehicle_bp.route("/user/delete_vehicle/<id>")
def delete_vehicle(id):

    vehicles_collection.delete_one({"_id": ObjectId(id)})

    return redirect("/user/vehicles")