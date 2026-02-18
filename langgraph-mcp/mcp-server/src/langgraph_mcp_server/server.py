"""FastMCP server with HTTP transport for hotel search and travel assistance."""

from fastmcp import FastMCP
import json
from typing import Any
from datetime import datetime

# Initialize FastMCP server
mcp = FastMCP("langgraph-mcp-server")


@mcp.tool()
def get_current_system_time() -> dict[str, str]:
    """Get the current system date and time.

    Returns:
        Dictionary containing current date, time, day of week, and ISO format
    """
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day_of_week": now.strftime("%A"),
        "iso_format": now.isoformat(),
        "timezone": "UTC"
    }


@mcp.tool()
def get_weather(location: str, date: str = None) -> dict[str, Any]:
    """Get weather information for a specific location.

    Args:
        location: The location to get weather for (e.g., "Paris", "Eiffel Tower")
        date: Optional date in YYYY-MM-DD format (defaults to today)

    Returns:
        Dictionary containing weather information
    """
    # Dummy weather data for different locations
    weather_data = {
        "paris": {
            "location": "Paris, France",
            "temperature": 18,
            "condition": "Partly Cloudy",
            "humidity": 65,
            "wind_speed": 12,
            "precipitation_chance": 20,
            "forecast": "Pleasant weather with occasional clouds"
        },
        "eiffel tower": {
            "location": "Near Eiffel Tower, Paris",
            "temperature": 18,
            "condition": "Partly Cloudy",
            "humidity": 65,
            "wind_speed": 12,
            "precipitation_chance": 20,
            "forecast": "Perfect weather for sightseeing"
        },
        "default": {
            "location": location,
            "temperature": 20,
            "condition": "Clear",
            "humidity": 60,
            "wind_speed": 10,
            "precipitation_chance": 10,
            "forecast": "Good weather conditions"
        }
    }

    location_key = location.lower()
    weather = weather_data.get(location_key, weather_data["default"])
    weather["date"] = date or datetime.now().strftime("%Y-%m-%d")
    weather["units"] = {"temperature": "Celsius", "wind_speed": "km/h"}

    return weather


@mcp.tool()
def search_hotels(location: str, max_results: int = 10) -> dict[str, Any]:
    """Search for hotels near a specific location.

    Args:
        location: The location to search near (e.g., "Eiffel Tower", "Paris")
        max_results: Maximum number of results to return (default: 10)

    Returns:
        Dictionary containing list of hotels with details
    """
    # Dummy hotel data
    hotels = [
        {
            "hotel_id": "HTL001",
            "name": "Le Grand Hotel Paris",
            "rating": 4.8,
            "price_per_night": 350,
            "distance_km": 0.5,
            "amenities": ["WiFi", "Restaurant", "Spa", "Gym", "Room Service"],
            "address": "12 Rue de Rivoli, 75001 Paris",
            "reviews_count": 2847,
            "description": "Luxury hotel with Eiffel Tower views"
        },
        {
            "hotel_id": "HTL002",
            "name": "Hotel Eiffel Seine",
            "rating": 4.6,
            "price_per_night": 280,
            "distance_km": 0.3,
            "amenities": ["WiFi", "Breakfast", "Bar", "Concierge"],
            "address": "3 Boulevard de Grenelle, 75015 Paris",
            "reviews_count": 1923,
            "description": "Charming boutique hotel steps from the Eiffel Tower"
        },
        {
            "hotel_id": "HTL003",
            "name": "Pullman Paris Tour Eiffel",
            "rating": 4.7,
            "price_per_night": 420,
            "distance_km": 0.2,
            "amenities": ["WiFi", "Restaurant", "Bar", "Fitness Center", "Business Center"],
            "address": "18 Avenue de Suffren, 75015 Paris",
            "reviews_count": 3156,
            "description": "Modern 4-star hotel with panoramic city views"
        },
        {
            "hotel_id": "HTL004",
            "name": "Hotel La Bourdonnais",
            "rating": 4.5,
            "price_per_night": 295,
            "distance_km": 0.4,
            "amenities": ["WiFi", "Breakfast", "Bar", "Garden"],
            "address": "111 Avenue de La Bourdonnais, 75007 Paris",
            "reviews_count": 1654,
            "description": "Elegant hotel near the Eiffel Tower with classic French charm"
        },
        {
            "hotel_id": "HTL005",
            "name": "Shangri-La Hotel Paris",
            "rating": 4.9,
            "price_per_night": 850,
            "distance_km": 0.8,
            "amenities": ["WiFi", "Restaurant", "Spa", "Pool", "Butler Service", "Michelin Star Dining"],
            "address": "10 Avenue d'Iéna, 75116 Paris",
            "reviews_count": 2234,
            "description": "Former palace with unparalleled luxury and Eiffel Tower views"
        },
        {
            "hotel_id": "HTL006",
            "name": "Mercure Paris Centre Tour Eiffel",
            "rating": 4.3,
            "price_per_night": 220,
            "distance_km": 0.6,
            "amenities": ["WiFi", "Breakfast", "Bar", "24h Reception"],
            "address": "20 Rue Jean Rey, 75015 Paris",
            "reviews_count": 1432,
            "description": "Comfortable hotel offering great value near Eiffel Tower"
        }
    ]

    # Limit results
    limited_hotels = hotels[:min(max_results, len(hotels))]

    return {
        "location": location,
        "total_results": len(limited_hotels),
        "currency": "EUR",
        "hotels": limited_hotels
    }


@mcp.tool()
def get_availability(hotel_id: str, check_in: str, check_out: str) -> dict[str, Any]:
    """Check availability for a specific hotel and date range.

    Args:
        hotel_id: The unique identifier for the hotel (e.g., "HTL001")
        check_in: Check-in date in YYYY-MM-DD format (Mandatory)
        check_out: Check-out date in YYYY-MM-DD format (Mandatory)

    Returns:
        Dictionary containing availability information and room options
    """
    # Dummy availability data
    availability = {
        "hotel_id": hotel_id,
        "check_in": check_in,
        "check_out": check_out,
        "available": True,
        "rooms": [
            {
                "room_type": "Standard Double Room",
                "available_rooms": 5,
                "price_per_night": 280,
                "max_occupancy": 2,
                "bed_type": "1 Double Bed",
                "size_sqm": 22,
                "features": ["City View", "Air Conditioning", "Flat-screen TV"]
            },
            {
                "room_type": "Deluxe Room with Eiffel Tower View",
                "available_rooms": 3,
                "price_per_night": 420,
                "max_occupancy": 2,
                "bed_type": "1 King Bed",
                "size_sqm": 30,
                "features": ["Eiffel Tower View", "Mini Bar", "Bathrobe & Slippers"]
            },
            {
                "room_type": "Junior Suite",
                "available_rooms": 2,
                "price_per_night": 580,
                "max_occupancy": 3,
                "bed_type": "1 King Bed + Sofa Bed",
                "size_sqm": 45,
                "features": ["Eiffel Tower View", "Separate Living Area", "Nespresso Machine"]
            }
        ],
        "cancellation_policy": "Free cancellation up to 24 hours before check-in",
        "booking_policies": [
            "Valid credit card required",
            "Check-in from 15:00",
            "Check-out until 11:00"
        ]
    }

    return availability


if __name__ == "__main__":
    # Run the server with HTTP transport
    import uvicorn

    # Get the HTTP app from FastMCP
    app = mcp.http_app

    print("Starting LangGraph MCP Server (Travel & Hotel Assistant)...")
    print("Server running at http://localhost:8000")
    print("MCP endpoint: http://localhost:8000/mcp")
    print("\nAvailable tools:")
    print("  - get_current_system_time: Get current date and time")
    print("  - get_weather: Get weather information for a location")
    print("  - search_hotels: Search for hotels near a location")
    print("  - get_availability: Check hotel availability and room options")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
