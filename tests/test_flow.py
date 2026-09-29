"""
End-to-End Test Suite for TravelGo
"""

import uuid
import unittest
from app import create_app
from config import Config

class TestConfig(Config):
    TESTING = True
    USE_LOCAL_MOCK_DB = "true"

class TravelGoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.random_email = f"test.user.{uuid.uuid4().hex[:6]}@example.com"

    def test_01_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "TravelGo")
        print(" [PASS] 1. Health check verified (/health)")

    def test_02_home_and_search(self):
        # Home
        res_home = self.client.get("/")
        self.assertEqual(res_home.status_code, 200)
        self.assertIn(b"Plan Your Journey With Ease", res_home.data)

        # Bus Search
        res_bus = self.client.get("/search?category=bus&source=Mumbai&destination=Pune")
        self.assertEqual(res_bus.status_code, 200)
        self.assertIn(b"SmartBus", res_bus.data)

        # Train Search
        res_train = self.client.get("/train")
        self.assertEqual(res_train.status_code, 200)
        self.assertIn(b"Vande Bharat", res_train.data)

        # Flight Search
        res_flight = self.client.get("/flight")
        self.assertEqual(res_flight.status_code, 200)
        self.assertIn(b"IndiGo", res_flight.data)

        # Hotels Search
        res_hotel = self.client.get("/hotels")
        self.assertEqual(res_hotel.status_code, 200)
        self.assertIn(b"Taj Mahal Palace", res_hotel.data)
        print(" [PASS] 2. Home and multi-category search verified (Bus, Train, Flight, Hotel)")

    def test_03_auth_and_booking_lifecycle(self):
        # 1. Register User
        reg_res = self.client.post("/register", data={
            "name": "Mohit Test",
            "email": self.random_email,
            "password": "SecretPassword123",
            "confirm_password": "SecretPassword123"
        }, follow_redirects=True)
        self.assertEqual(reg_res.status_code, 200)
        self.assertIn(b"Account created successfully", reg_res.data)
        print(" [PASS] 3. User registration verified")

        # 2. Login User
        login_res = self.client.post("/login", data={
            "email": self.random_email,
            "password": "SecretPassword123"
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertIn(b"My Travel Dashboard", login_res.data)
        print(" [PASS] 4. User login & session creation verified")

        # 3. Create a Flight Booking
        book_res = self.client.post("/book/submit", data={
            "item_id": "FLT-301",
            "travel_date": "2026-10-15",
            "seat": "Seat-12A",
            "payment_method": "UPI",
            "payment_reference": "TXN9876543210"
        }, follow_redirects=True)
        self.assertEqual(book_res.status_code, 200)
        self.assertIn(b"Booking Confirmed!", book_res.data)
        self.assertIn(b"Seat-12A", book_res.data)
        self.assertIn(b"E-Ticket Voucher", book_res.data)
        print(" [PASS] 5. Booking reservation and digital boarding pass verified")

        # 4. Check Dashboard for Active Bookings
        dash_res = self.client.get("/dashboard")
        self.assertEqual(dash_res.status_code, 200)
        self.assertIn(b"Active & Upcoming Trips", dash_res.data)
        self.assertIn(b"CONFIRMED", dash_res.data)
        print(" [PASS] 6. User dashboard history verified")

if __name__ == "__main__":
    unittest.main()
