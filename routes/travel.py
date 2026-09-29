"""
Travel & Accommodation Blueprint
Handles home page, search queries, and listings for Buses, Trains, Flights, and Hotels.
"""

from flask import Blueprint, render_template, request
from services.travel_data import search_travel, search_hotels, SAMPLE_CITIES

travel_bp = Blueprint("travel", __name__)

@travel_bp.route("/")
def home():
    """Render home landing page."""
    return render_template("index.html", cities=SAMPLE_CITIES)

@travel_bp.route("/search")
def search():
    """Unified search endpoint for all travel and hotel services."""
    category = request.args.get("category", "bus").lower()
    source = request.args.get("source", "").strip()
    destination = request.args.get("destination", "").strip()
    travel_date = request.args.get("date", "")
    
    # Hotel specific filters
    hotel_city = request.args.get("hotel_city", source or destination or "").strip()
    hotel_type = request.args.get("hotel_type", "all").lower()
    max_price = request.args.get("max_price")
    try:
        max_price = float(max_price) if max_price else None
    except ValueError:
        max_price = None

    if category == "hotels":
        results = search_hotels(city=hotel_city, category=hotel_type, max_price=max_price)
    else:
        results = search_travel(travel_type=category, source=source, destination=destination, travel_date=travel_date)

    return render_template(
        "search.html",
        results=results,
        category=category,
        source=source,
        destination=destination,
        travel_date=travel_date,
        hotel_city=hotel_city,
        hotel_type=hotel_type,
        max_price=max_price,
        cities=SAMPLE_CITIES
    )

@travel_bp.route("/bus")
def bus_list():
    return search_travel_page("bus")

@travel_bp.route("/train")
def train_list():
    return search_travel_page("train")

@travel_bp.route("/flight")
def flight_list():
    return search_travel_page("flight")

@travel_bp.route("/hotels")
def hotels_list():
    results = search_hotels(category="all")
    return render_template("search.html", results=results, category="hotels", cities=SAMPLE_CITIES)

def search_travel_page(cat):
    results = search_travel(travel_type=cat)
    return render_template("search.html", results=results, category=cat, cities=SAMPLE_CITIES)
