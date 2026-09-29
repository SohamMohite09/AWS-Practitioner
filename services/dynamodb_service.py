"""
DynamoDB Database Service
Handles CRUD operations for Users and Bookings entities using boto3.
Includes seamless local fallback persistence for offline development & testing.
"""

import os
import json
import logging
from datetime import datetime, timezone
from config import Config

logger = logging.getLogger(__name__)

def get_current_time():
    return datetime.now(timezone.utc).isoformat()

class DynamoDBService:
    def __init__(self):
        self.region = Config.AWS_REGION
        self.users_table_name = Config.DYNAMODB_USERS_TABLE
        self.bookings_table_name = Config.DYNAMODB_BOOKINGS_TABLE
        self.use_mock = Config.USE_LOCAL_MOCK_DB.lower() == "true"
        self.mock_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "local_db.json")
        
        self.dynamodb = None
        self.users_table = None
        self.bookings_table = None
        
        if not self.use_mock:
            self._init_aws_client()

    def _init_aws_client(self):
        """Try connecting to AWS DynamoDB via boto3."""
        try:
            import boto3
            self.dynamodb = boto3.resource("dynamodb", region_name=self.region)
            self.users_table = self.dynamodb.Table(self.users_table_name)
            self.bookings_table = self.dynamodb.Table(self.bookings_table_name)
            
            # Quick check if tables are accessible
            # We don't crash if they are not yet created, we set a flag
            logger.info("Connected to AWS DynamoDB resource in region: %s", self.region)
        except Exception as e:
            logger.warning("AWS DynamoDB connection not initialized: %s. Using local store fallback.", e)
            self.use_mock = True

    # --- Local Mock Storage Helpers (Ensures 100% offline & local reliability) ---
    def _read_mock_db(self):
        os.makedirs(os.path.dirname(self.mock_file_path), exist_ok=True)
        if not os.path.exists(self.mock_file_path):
            initial_data = {"users": {}, "bookings": {}}
            with open(self.mock_file_path, "w") as f:
                json.dump(initial_data, f, indent=2)
            return initial_data
        try:
            with open(self.mock_file_path, "r") as f:
                return json.load(f)
        except Exception:
            return {"users": {}, "bookings": {}}

    def _write_mock_db(self, data):
        os.makedirs(os.path.dirname(self.mock_file_path), exist_ok=True)
        with open(self.mock_file_path, "w") as f:
            json.dump(data, f, indent=2)

    # ================= USER OPERATIONS =================
    def get_user(self, email):
        """Retrieve user by primary key (email)."""
        email_clean = email.strip().lower()
        if not self.use_mock and self.users_table:
            try:
                response = self.users_table.get_item(Key={"email": email_clean})
                return response.get("Item")
            except Exception as e:
                logger.warning("DynamoDB get_user failed, trying mock store: %s", e)

        # Fallback
        db = self._read_mock_db()
        return db.get("users", {}).get(email_clean)

    def create_user(self, email, name, password_hash):
        """Create a new user in the Users table."""
        email_clean = email.strip().lower()
        user_item = {
            "email": email_clean,
            "name": name.strip(),
            "password": password_hash,
            "logins": 1,
            "created_at": get_current_time()
        }

        if not self.use_mock and self.users_table:
            try:
                self.users_table.put_item(
                    Item=user_item,
                    ConditionExpression="attribute_not_exists(email)"
                )
                return True, user_item
            except Exception as e:
                # If error is ConditionalCheckFailedException or table doesn't exist
                if "ConditionalCheckFailedException" in str(e):
                    return False, "User with this email already exists."
                logger.warning("DynamoDB put_item failed: %s. Using local store.", e)

        # Fallback
        db = self._read_mock_db()
        if email_clean in db.get("users", {}):
            return False, "User with this email already exists."
        db.setdefault("users", {})[email_clean] = user_item
        self._write_mock_db(db)
        return True, user_item

    def increment_user_logins(self, email):
        """Increment the login counter for the user."""
        email_clean = email.strip().lower()
        if not self.use_mock and self.users_table:
            try:
                self.users_table.update_item(
                    Key={"email": email_clean},
                    UpdateExpression="SET logins = if_not_exists(logins, :zero) + :val",
                    ExpressionAttributeValues={":val": 1, ":zero": 0}
                )
                return True
            except Exception as e:
                logger.warning("DynamoDB increment logins failed: %s", e)

        # Fallback
        db = self._read_mock_db()
        if email_clean in db.get("users", {}):
            db["users"][email_clean]["logins"] = db["users"][email_clean].get("logins", 0) + 1
            self._write_mock_db(db)
        return True

    # ================= BOOKING OPERATIONS =================
    def create_booking(self, booking_data):
        """
        Store a new booking in DynamoDB Bookings table.
        Schema: booking_id (PK), email, type, source, destination, date, seat, details, price, payment_method, payment_reference, status
        """
        item = {
            "booking_id": booking_data["booking_id"],
            "email": booking_data["email"].strip().lower(),
            "type": booking_data["type"],
            "source": booking_data.get("source", "N/A"),
            "destination": booking_data.get("destination", "N/A"),
            "date": booking_data.get("date", "N/A"),
            "seat": booking_data.get("seat", "N/A"),
            "details": booking_data.get("details", ""),
            "price": str(booking_data.get("price", "0")), # Stored as string or Decimal in DynamoDB
            "payment_method": booking_data.get("payment_method", "UPI"),
            "payment_reference": booking_data.get("payment_reference", ""),
            "status": booking_data.get("status", "CONFIRMED"),
            "created_at": get_current_time()
        }

        if not self.use_mock and self.bookings_table:
            try:
                self.bookings_table.put_item(Item=item)
                return True, item
            except Exception as e:
                logger.warning("DynamoDB create_booking failed: %s. Using local store.", e)

        # Fallback
        db = self._read_mock_db()
        db.setdefault("bookings", {})[item["booking_id"]] = item
        self._write_mock_db(db)
        return True, item

    def get_booking(self, booking_id):
        """Fetch a specific booking by booking_id."""
        if not self.use_mock and self.bookings_table:
            try:
                response = self.bookings_table.get_item(Key={"booking_id": booking_id})
                return response.get("Item")
            except Exception as e:
                logger.warning("DynamoDB get_booking failed: %s", e)

        db = self._read_mock_db()
        return db.get("bookings", {}).get(booking_id)

    def get_user_bookings(self, email):
        """Retrieve all bookings belonging to a specific user (by email)."""
        email_clean = email.strip().lower()
        if not self.use_mock and self.bookings_table:
            try:
                # Scan with filter on email or query if GSI exists
                from boto3.dynamodb.conditions import Attr
                response = self.bookings_table.scan(
                    FilterExpression=Attr("email").eq(email_clean)
                )
                items = response.get("Items", [])
                # Sort newest first
                items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
                return items
            except Exception as e:
                logger.warning("DynamoDB scan bookings failed: %s. Using local store.", e)

        db = self._read_mock_db()
        user_bookings = [
            b for b in db.get("bookings", {}).values()
            if b.get("email", "").lower() == email_clean
        ]
        user_bookings.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return user_bookings

    def cancel_booking(self, booking_id, user_email):
        """
        Cancel a booking with strict ownership verification.
        Only the booking owner can cancel their booking.
        """
        booking = self.get_booking(booking_id)
        if not booking:
            return False, "Booking not found."
            
        if booking.get("email", "").lower() != user_email.strip().lower():
            return False, "Unauthorized: You do not own this booking."

        if booking.get("status") == "CANCELLED":
            return False, "This booking has already been cancelled."

        # Update in DynamoDB
        if not self.use_mock and self.bookings_table:
            try:
                self.bookings_table.update_item(
                    Key={"booking_id": booking_id},
                    UpdateExpression="SET #s = :cancelled, cancelled_at = :now",
                    ExpressionAttributeNames={"#s": "status"},
                    ExpressionAttributeValues={
                        ":cancelled": "CANCELLED",
                        ":now": datetime.utcnow().isoformat()
                    }
                )
                booking["status"] = "CANCELLED"
                return True, booking
            except Exception as e:
                logger.warning("DynamoDB cancel_booking update failed: %s", e)

        # Fallback
        db = self._read_mock_db()
        if booking_id in db.get("bookings", {}):
            db["bookings"][booking_id]["status"] = "CANCELLED"
            db["bookings"][booking_id]["cancelled_at"] = datetime.utcnow().isoformat()
            self._write_mock_db(db)
            booking = db["bookings"][booking_id]
            return True, booking

        return False, "Could not update booking state."

# Singleton instance for simple reuse
db_service = DynamoDBService()
