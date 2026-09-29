"""
Authentication Blueprint
Handles User Registration, Login, Logout, and Session Management.
Passwords are securely hashed using Werkzeug.
"""

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from services.dynamodb_service import db_service

auth_bp = Blueprint("auth", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_email" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_email" in session:
        return redirect(url_for("dashboard.view_dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Form Validation
        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html", name=name, email=email)

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html", name=name, email=email)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("register.html", name=name, email=email)

        # Hash password securely
        password_hash = generate_password_hash(password)

        # Store in DynamoDB Users table
        success, result = db_service.create_user(email, name, password_hash)
        if not success:
            flash(result, "danger")
            return render_template("register.html", name=name, email=email)

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_email" in session:
        return redirect(url_for("dashboard.view_dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        next_url = request.args.get("next") or url_for("dashboard.view_dashboard")

        if not email or not password:
            flash("Please provide both email and password.", "danger")
            return render_template("login.html", email=email)

        # Lookup user in DynamoDB
        user = db_service.get_user(email)
        if not user or not check_password_hash(user.get("password", ""), password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html", email=email)

        # Increment login counter in DynamoDB
        db_service.increment_user_logins(email)

        # Set session variables
        session["user_email"] = user["email"]
        session["user_name"] = user.get("name", email.split("@")[0])
        
        flash(f"Welcome back, {session['user_name']}!", "success")
        return redirect(next_url)

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("travel.home"))
