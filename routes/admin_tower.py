from flask import Blueprint, render_template, request, redirect
from db import db
from bson.objectid import ObjectId

towers_collection = db["towers"]

admin_tower_bp = Blueprint("admin_tower_bp", __name__)

# =========================
# VIEW TOWERS
# =========================
@admin_tower_bp.route("/admin/towers")
def manage_towers():

    towers = list(towers_collection.find())

    return render_template("admin/admin_tower.html", towers=towers)


# =========================
# ADD TOWER
# =========================
@admin_tower_bp.route("/admin/add_tower", methods=["GET","POST"])
def add_tower():

    if request.method == "POST":

        data = {
            "tower_name": request.form.get("tower_name"),
            "total_floors": int(request.form.get("total_floors")),
            "total_flats": int(request.form.get("total_flats"))
        }

        towers_collection.insert_one(data)

        return redirect("/admin/towers")

    return render_template("admin/admin_add_tower.html")


# =========================
# EDIT TOWER
# =========================
@admin_tower_bp.route("/admin/edit_tower/<id>", methods=["GET","POST"])
def edit_tower(id):

    tower = towers_collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":

        updated_data = {
            "tower_name": request.form.get("tower_name"),
            "total_floors": int(request.form.get("total_floors")),
            "total_flats": int(request.form.get("total_flats"))
        }

        towers_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": updated_data}
        )

        return redirect("/admin/towers")

    return render_template("admin/admin_edit_tower.html", tower=tower)


# =========================
# DELETE TOWER
# =========================
@admin_tower_bp.route("/admin/delete_tower/<id>")
def delete_tower(id):

    towers_collection.delete_one({"_id": ObjectId(id)})

    return redirect("/admin/towers")