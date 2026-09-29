"""
Travel Data Repository
Provides mock travel inventory for Buses, Trains, Flights, and Hotels.
"""

SAMPLE_CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Goa", "Jaipur", "Ahmedabad"
]

BUS_INVENTORY = [
    {
        "id": "BUS-101",
        "name": "InterCity SmartBus Volvo A/C Multi-Axle",
        "type": "bus",
        "source": "Mumbai",
        "destination": "Pune",
        "departure_time": "06:30 AM",
        "arrival_time": "10:00 AM",
        "duration": "3h 30m",
        "price": 650,
        "rating": 4.6,
        "amenities": ["WiFi", "Water Bottle", "Charging Point", "Recliner Seats"],
        "total_seats": 24,
    },
    {
        "id": "BUS-102",
        "name": "Zingbus Luxury Sleeper (2+1)",
        "type": "bus",
        "source": "Delhi",
        "destination": "Jaipur",
        "departure_time": "07:00 AM",
        "arrival_time": "12:30 PM",
        "duration": "5h 30m",
        "price": 850,
        "rating": 4.5,
        "amenities": ["Live Tracking", "Emergency Contact", "AC", "Blanket"],
        "total_seats": 24,
    },
    {
        "id": "BUS-103",
        "name": "SRS Travels Scania Multi-Axle",
        "type": "bus",
        "source": "Bengaluru",
        "destination": "Chennai",
        "departure_time": "08:15 AM",
        "arrival_time": "02:00 PM",
        "duration": "5h 45m",
        "price": 920,
        "rating": 4.4,
        "amenities": ["Movie Screen", "Snacks", "AC", "Reading Lamp"],
        "total_seats": 24,
    },
    {
        "id": "BUS-104",
        "name": "Orange Tours BharatBenz Sleeper",
        "type": "bus",
        "source": "Hyderabad",
        "destination": "Bengaluru",
        "departure_time": "09:30 PM",
        "arrival_time": "06:30 AM",
        "duration": "9h 00m",
        "price": 1250,
        "rating": 4.7,
        "amenities": ["Pillow", "WiFi", "Emergency Alarm", "CCTV"],
        "total_seats": 24,
    },
    {
        "id": "BUS-105",
        "name": "Paulo Travels AC Seater/Sleeper",
        "type": "bus",
        "source": "Mumbai",
        "destination": "Goa",
        "departure_time": "08:00 PM",
        "arrival_time": "07:30 AM",
        "duration": "11h 30m",
        "price": 1400,
        "rating": 4.3,
        "amenities": ["AC", "Charging Port", "Music", "Luggage Storage"],
        "total_seats": 24,
    },
]

TRAIN_INVENTORY = [
    {
        "id": "TRN-201",
        "name": "Vande Bharat Express (20901)",
        "type": "train",
        "source": "Mumbai",
        "destination": "Ahmedabad",
        "departure_time": "06:00 AM",
        "arrival_time": "11:25 AM",
        "duration": "5h 25m",
        "price": 1380,
        "rating": 4.8,
        "amenities": ["High-speed Travel", "Catering Included", "CCTV", "Bio-vacuum Toilets"],
        "total_seats": 24,
    },
    {
        "id": "TRN-202",
        "name": "Rajdhani Special Express (12951)",
        "type": "train",
        "source": "Delhi",
        "destination": "Mumbai",
        "departure_time": "04:55 PM",
        "arrival_time": "08:35 AM",
        "duration": "15h 40m",
        "price": 2450,
        "rating": 4.7,
        "amenities": ["Full Meals", "Bedding Kit", "AC 2 Tier", "Security Guard"],
        "total_seats": 24,
    },
    {
        "id": "TRN-203",
        "name": "Shatabdi Express (12027)",
        "type": "train",
        "source": "Bengaluru",
        "destination": "Chennai",
        "departure_time": "06:00 AM",
        "arrival_time": "11:00 AM",
        "duration": "5h 00m",
        "price": 970,
        "rating": 4.6,
        "amenities": ["Morning Tea & Breakfast", "Newspaper", "Executive Chairs"],
        "total_seats": 24,
    },
    {
        "id": "TRN-204",
        "name": "Duronto Express (12285)",
        "type": "train",
        "source": "Hyderabad",
        "destination": "Delhi",
        "departure_time": "01:10 PM",
        "arrival_time": "10:35 AM",
        "duration": "21h 25m",
        "price": 2850,
        "rating": 4.5,
        "amenities": ["Non-stop Run", "Gourmet Meals", "Doctor On-board"],
        "total_seats": 24,
    },
]

FLIGHT_INVENTORY = [
    {
        "id": "FLT-301",
        "name": "IndiGo 6E-205",
        "type": "flight",
        "source": "Mumbai",
        "destination": "Delhi",
        "departure_time": "07:15 AM",
        "arrival_time": "09:30 AM",
        "duration": "2h 15m",
        "price": 4200,
        "rating": 4.5,
        "amenities": ["7kg Cabin Bag", "15kg Check-in", "In-flight Snacks"],
        "total_seats": 24,
    },
    {
        "id": "FLT-302",
        "name": "Air India AI-582",
        "type": "flight",
        "source": "Bengaluru",
        "destination": "Hyderabad",
        "departure_time": "08:45 AM",
        "arrival_time": "09:55 AM",
        "duration": "1h 10m",
        "price": 3100,
        "rating": 4.4,
        "amenities": ["Complimentary Meal", "25kg Baggage", "Extra Legroom"],
        "total_seats": 24,
    },
    {
        "id": "FLT-303",
        "name": "Akasa Air QP-1124",
        "type": "flight",
        "source": "Delhi",
        "destination": "Goa",
        "departure_time": "11:20 AM",
        "arrival_time": "01:55 PM",
        "duration": "2h 35m",
        "price": 5400,
        "rating": 4.7,
        "amenities": ["USB Port on Seat", "Pet-friendly", "Cafe Akasa menu"],
        "total_seats": 24,
    },
    {
        "id": "FLT-304",
        "name": "Vistara UK-945",
        "type": "flight",
        "source": "Mumbai",
        "destination": "Kolkata",
        "departure_time": "05:40 PM",
        "arrival_time": "08:15 PM",
        "duration": "2h 35m",
        "price": 4890,
        "rating": 4.8,
        "amenities": ["Premium Economy", "Starbucks Coffee", "Inflight Entertainment"],
        "total_seats": 24,
    },
]

HOTEL_INVENTORY = [
    {
        "id": "HTL-401",
        "name": "The Taj Mahal Palace & Tower",
        "type": "hotel",
        "category": "luxury",
        "city": "Mumbai",
        "location": "Apollo Bunder, Colaba",
        "price_per_night": 12500,
        "rating": 4.9,
        "amenities": ["Sea View", "Infinity Pool", "Spa", "Valet Parking", "Fine Dining"],
        "room_types": ["Deluxe Sea View", "Luxury Suite"],
    },
    {
        "id": "HTL-402",
        "name": "Zostel Backpacker Hub",
        "type": "hotel",
        "category": "budget",
        "city": "Mumbai",
        "location": "Andheri East",
        "price_per_night": 1200,
        "rating": 4.4,
        "amenities": ["High-speed WiFi", "Rooftop Cafe", "Shared Lounge", "Lockers"],
        "room_types": ["Standard Private AC", "Dorm Bed"],
    },
    {
        "id": "HTL-403",
        "name": "ITC Maurya, A Luxury Collection Hotel",
        "type": "hotel",
        "category": "luxury",
        "city": "Delhi",
        "location": "Diplomatic Enclave, Chanakyapuri",
        "price_per_night": 10800,
        "rating": 4.8,
        "amenities": ["Bukhara Restaurant", "Kaya Kalp Spa", "Outdoor Pool", "Fitness Club"],
        "room_types": ["Executive Club Room", "ITC One Suite"],
    },
    {
        "id": "HTL-404",
        "name": "Bloom Boutique Heritage Villa",
        "type": "hotel",
        "category": "budget",
        "city": "Delhi",
        "location": "Connaught Place",
        "price_per_night": 2200,
        "rating": 4.5,
        "amenities": ["Free Breakfast", "CloudBeds", "Digital Check-in", "Work Desk"],
        "room_types": ["Queen Room", "Deluxe Twin"],
    },
    {
        "id": "HTL-405",
        "name": "The Leela Palace Bengaluru",
        "type": "hotel",
        "category": "luxury",
        "city": "Bengaluru",
        "location": "Old Airport Road, HAL",
        "price_per_night": 11500,
        "rating": 4.9,
        "amenities": ["Royal Gardens", "Michelin-style Dining", "Spa", "Heated Pool"],
        "room_types": ["Royal Premier Room", "Palace Suite"],
    },
    {
        "id": "HTL-406",
        "name": "FabHotel Prime Stay",
        "type": "hotel",
        "category": "budget",
        "city": "Bengaluru",
        "location": "Koramangala 4th Block",
        "price_per_night": 1600,
        "rating": 4.2,
        "amenities": ["Free WiFi", "AC", "Room Service", "Power Backup"],
        "room_types": ["Standard AC Room"],
    },
    {
        "id": "HTL-407",
        "name": "W Goa Resort & Beachfront",
        "type": "hotel",
        "category": "luxury",
        "city": "Goa",
        "location": "Vagator Beach",
        "price_per_night": 15000,
        "rating": 4.8,
        "amenities": ["Private Beach", "Rock Pool", "Sunset Bar", "Spa by Clarins"],
        "room_types": ["Wonderful Garden View", "Fabulous Villa"],
    },
    {
        "id": "HTL-408",
        "name": "Roadhouse Hostels & Co-Living",
        "type": "hotel",
        "category": "budget",
        "city": "Goa",
        "location": "Anjuna",
        "price_per_night": 950,
        "rating": 4.3,
        "amenities": ["Garden Cafe", "Bike Rental", "WiFi", "Community Kitchen"],
        "room_types": ["Private Room AC", "Bunk Bed"],
    },
]

def search_travel(travel_type="all", source="", destination="", travel_date=""):
    """Search bus, train, and flight inventory matching criteria."""
    results = []
    
    types_to_search = []
    if travel_type in ("bus", "all"):
        types_to_search.extend(BUS_INVENTORY)
    if travel_type in ("train", "all"):
        types_to_search.extend(TRAIN_INVENTORY)
    if travel_type in ("flight", "all"):
        types_to_search.extend(FLIGHT_INVENTORY)
    
    src = source.strip().lower()
    dst = destination.strip().lower()
    
    for item in types_to_search:
        # Match source and destination if supplied, else return all available options
        src_match = not src or src in item["source"].lower()
        dst_match = not dst or dst in item["destination"].lower()
        
        # If user searched specific cities and both match, or if search was open
        if (src_match and dst_match) or (not src and not dst):
            result_item = dict(item)
            result_item["date"] = travel_date or "Flexible Date"
            results.append(result_item)
            
    return results

def search_hotels(city="", category="all", max_price=None):
    """Search hotel inventory matching city and optional category/price."""
    results = []
    c = city.strip().lower()
    cat = category.strip().lower()
    
    for item in HOTEL_INVENTORY:
        city_match = not c or c in item["city"].lower() or c in item["location"].lower()
        cat_match = (cat == "all") or (cat == item["category"].lower())
        price_match = True
        if max_price is not None and max_price > 0:
            price_match = item["price_per_night"] <= max_price
            
        if city_match and cat_match and price_match:
            results.append(dict(item))
            
    return results

def get_item_by_id(item_id):
    """Lookup an item from any inventory list by ID."""
    all_items = BUS_INVENTORY + TRAIN_INVENTORY + FLIGHT_INVENTORY + HOTEL_INVENTORY
    for item in all_items:
        if item["id"] == item_id:
            return dict(item)
    return None
