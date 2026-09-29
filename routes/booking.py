"""
Booking Blueprint
Handles seat selection, review, checkout, DynamoDB storage, SNS notification, and confirmation voucher.
"""

import uuid
import random
import string
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from routes.auth import login_required
from services.travel_data import get_item_by_id
from services.dynamodb_service import db_service
from services.sns_service import sns_service

booking_bp = Blueprint("booking", __name__)

def generate_booking_id():
    """Generates a clean human-readable booking ID like TG-8A39F12B."""
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"TG-{random_part}"

def generate_payment_ref():
    """Generates a sample payment transaction reference."""
    random_num = "".join(random.choices(string.digits, k=10))
    return f"TXN{random_num}"

@booking_bp.route("/book/<item_id>", methods=["GET"])
@login_required
def book_item(item_id):
    """Render checkout and seat/room selection page."""
    item = get_item_by_id(item_id)
    if not item:
        flash("Selected travel or hotel item not found.", "danger")
        return redirect(url_for("travel.home"))

    travel_date = request.args.get("date", datetime.utcnow().strftime("%Y-%m-%d"))
    preset_seat = request.args.get("seat", "")
    sample_ref = generate_payment_ref()

    return render_template(
        "booking.html",
        item=item,
        travel_date=travel_date,
        preset_seat=preset_seat,
        sample_ref=sample_ref,
        user_email=session.get("user_email"),
        user_name=session.get("user_name")
    )

@booking_bp.route("/book/submit", methods=["POST"])
@login_required
def submit_booking():
    """Process booking submission, save to DynamoDB, trigger SNS, and confirm."""
    item_id = request.form.get("item_id")
    item = get_item_by_id(item_id)

    if not item:
        flash("Invalid booking request: Item not found.", "danger")
        return redirect(url_for("travel.home"))

    user_email = session.get("user_email")
    item_type = item.get("type", "bus")
    
    # Extract form fields
    source = item.get("source", item.get("city", "N/A"))
    destination = item.get("destination", item.get("location", "N/A"))
    travel_date = request.form.get("travel_date") or datetime.utcnow().strftime("%Y-%m-%d")
    seat = request.form.get("seat") or request.form.get("room_type") or "Auto-Assigned"
    price = item.get("price") or item.get("price_per_night") or 0
    payment_method = request.form.get("payment_method", "UPI")
    payment_reference = request.form.get("payment_reference") or generate_payment_ref()
    details = f"{item.get('name')} | {item.get('departure_time', '')} - {item.get('arrival_time', '')}".strip(" | -")

    # Generate primary key for Bookings table
    booking_id = generate_booking_id()

    booking_payload = {
        "booking_id": booking_id,
        "email": user_email,
        "type": item_type,
        "source": source,
        "destination": destination,
        "date": travel_date,
        "seat": seat,
        "details": details,
        "price": price,
        "payment_method": payment_method,
        "payment_reference": payment_reference,
        "status": "CONFIRMED"
    }

    # Step 1: Save to DynamoDB Bookings table (mandatory persistence check)
    success, saved_booking = db_service.create_booking(booking_payload)
    if not success:
        flash("Failed to process booking in database. Please try again.", "danger")
        return redirect(url_for("booking.book_item", item_id=item_id))

    # Step 2: Trigger SNS notification after successful database write
    sns_ok, sns_msg = sns_service.send_booking_confirmation(saved_booking)

    flash("Booking completed successfully!", "success")
    return redirect(url_for("booking.confirmation", booking_id=booking_id))

@booking_bp.route("/confirmation/<booking_id>")
@login_required
def confirmation(booking_id):
    """Render the digital boarding pass / confirmation voucher."""
    booking = db_service.get_booking(booking_id)
    if not booking:
        flash("Booking voucher not found.", "warning")
        return redirect(url_for("dashboard.view_dashboard"))

    # Verify ownership
    if booking.get("email", "").lower() != session.get("user_email", "").lower():
        flash("Unauthorized access to booking.", "danger")
        return redirect(url_for("dashboard.view_dashboard"))

    return render_template("confirmation.html", booking=booking)
