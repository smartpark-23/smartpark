from flask import Blueprint, render_template, request, redirect, session
from db import db

auth_bp = Blueprint("auth_bp", __name__)

users_collection = db["users"]


# =========================
# DEFAULT ROUTE (OPEN LOGIN FIRST)
# =========================
@auth_bp.route("/")
def home_redirect():
    return redirect("/login")


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        flat = request.form.get("flat")

        # Duplicate email check
        existing_user = users_collection.find_one({"email": email})

        if existing_user:
            return "⚠️ Email already exists!"

        # Save user
        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": password,
            "phone": phone,
            "flat": flat,
            "role": "resident"
        })

        return redirect("/login")

    return render_template("register.html")


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = users_collection.find_one({
            "email": email,
            "password": password
        })

        if user:

            # SESSION STORE
            session["user_id"] = str(user["_id"])
            session["name"] = user["name"]
            session["role"] = user["role"]

            # ROLE BASED REDIRECT
            if user["role"] == "admin":
                return redirect("/admin/dashboard")
            else:
                return redirect("/user/home")   # 🔥 user home page

        else:
            return "❌ Invalid Email or Password"

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
def logout():

    session.clear()
    return redirect("/")