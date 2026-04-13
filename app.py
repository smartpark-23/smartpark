from flask import Flask
from routes.auth import auth_bp

# 🔥 Admin routes
from routes.admin_dashboard import admin_dashboard_bp
from routes.admin_resident import admin_resident_bp
from routes.admin_vehicle import admin_vehicle_bp
from routes.admin_tower import admin_tower_bp
from routes.admin_parking_slots import admin_parking_slot_bp
from routes.resident_approval import resident_bp
from routes.admin_reports import admin_reports_bp
from routes.admin_profile import admin_profile_bp
from routes.admin_guest import admin_guest_bp

# 👤 User routes
from routes.user_dashboard import user_dashboard_bp
from routes.user_vehicle import user_vehicle_bp
from routes.user_booking import user_booking_bp
from routes.user_parking import user_parking_bp
from routes.user_guest import user_guest_bp
from routes.resident_profile import resident_profile_bp
from routes.user_notifications import user_notifications_bp

# 🚗 Guest Landing Page
from routes.guest_homepage import guest_parking_bp
from routes.guest_parking_request import guest_request_bp
from routes.guest_dashboard import guest_dashboard_bp
from routes.guest_receipt import guest_receipt_bp


# =========================
# APP INITIALIZATION
# =========================
app = Flask(__name__)

# 🔐 Secret Key
app.secret_key = "smartpark_secret"


# =========================
# REGISTER BLUEPRINTS
# =========================

# Guest landing page (HOME PAGE)
app.register_blueprint(guest_parking_bp)

# Auth
app.register_blueprint(auth_bp)

# Admin
app.register_blueprint(admin_dashboard_bp)
app.register_blueprint(admin_resident_bp)
app.register_blueprint(admin_vehicle_bp)
app.register_blueprint(admin_tower_bp)
app.register_blueprint(admin_parking_slot_bp)
app.register_blueprint(resident_bp)
app.register_blueprint(admin_reports_bp)
app.register_blueprint(admin_profile_bp)

# User
app.register_blueprint(user_dashboard_bp)
app.register_blueprint(user_vehicle_bp)
app.register_blueprint(user_booking_bp)
app.register_blueprint(user_parking_bp)
app.register_blueprint(user_guest_bp)
app.register_blueprint(user_notifications_bp)
app.register_blueprint(resident_profile_bp)

# Guest public form
app.register_blueprint(guest_request_bp)
app.register_blueprint(admin_guest_bp)
app.register_blueprint(guest_dashboard_bp)
app.register_blueprint(guest_receipt_bp)

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)