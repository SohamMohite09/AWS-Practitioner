"""
Dashboard Blueprint
Handles User Profile, Booking History, Active Reservations, and Cancellation with Ownership Verification.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from routes.auth import login_required
from services.dynamodb_service import db_service
from services.sns_service import sns_service

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def view_dashboard():
    """Display user bookings and profile stats."""
    user_email = session.get("user_email")
    user = db_service.get_user(user_email)
    bookings = db_service.get_user_bookings(user_email)

    active_bookings = [b for b in bookings if b.get("status") != "CANCELLED"]
    cancelled_bookings = [b for b in bookings if b.get("status") == "CANCELLED"]

    stats = {
        "total": len(bookings),
        "active": len(active_bookings),
        "cancelled": len(cancelled_bookings),
        "logins": user.get("logins", 1) if user else 1
    }

    return render_template(
        "dashboard.html",
        user=user,
        active_bookings=active_bookings,
        cancelled_bookings=cancelled_bookings,
        stats=stats
    )

@dashboard_bp.route("/booking/<booking_id>/cancel", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    """Cancel a booking securely with server-side ownership verification."""
    user_email = session.get("user_email")
    
    success, result = db_service.cancel_booking(booking_id, user_email)
    if not success:
        flash(f"Cancellation failed: {result}", "danger")
        return redirect(url_for("dashboard.view_dashboard"))

    # Trigger SNS cancellation notification
    sns_service.send_cancellation_notification(result)

    flash(f"Booking #{booking_id} has been cancelled successfully.", "info")
    return redirect(url_for("dashboard.view_dashboard"))
