from flask import Blueprint, render_template, request, redirect, session, flash
from db import users_collection

admin_auth_bp = Blueprint("admin_auth_bp", __name__)

@admin_auth_bp.route("/admin/login", methods=["GET","POST"])
def admin_login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # MongoDB mathi user find
        admin = users_collection.find_one({"email": email})

        print(admin)  # DEBUG

        if admin and admin["password"] == password:

            session["admin"] = admin["name"]

            print("LOGIN SUCCESS")

            return redirect("/admin/dashboard")

        else:
            flash("Invalid Login")

    return render_template("admin/admin_login.html")
    # =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
def logout():

    session.clear()
    return redirect("/")