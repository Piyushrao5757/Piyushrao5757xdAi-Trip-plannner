"""
Itinerary Generator - Generates day-by-day travel itineraries
"""
from datetime import datetime, timedelta
import random


DESTINATION_DATA = {
    "paris": {
        "name": "Paris, France",
        "attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Montmartre", "Versailles"],
        "avg_daily_cost": 150,
        "best_season": "spring",
        "timezone": "CET",
    },
    "tokyo": {
        "name": "Tokyo, Japan",
        "attractions": ["Shibuya Crossing", "Senso-ji Temple", "TeamLab Planets", "Shinjuku Gyoen", "Akihabara"],
        "avg_daily_cost": 120,
        "best_season": "spring",
        "timezone": "JST",
    },
    "new york": {
        "name": "New York, USA",
        "attractions": ["Central Park", "Times Square", "Statue of Liberty", "Metropolitan Museum", "Brooklyn Bridge"],
        "avg_daily_cost": 200,
        "best_season": "fall",
        "timezone": "EST",
    },
    "bali": {
        "name": "Bali, Indonesia",
        "attractions": ["Tanah Lot Temple", "Ubud Monkey Forest", "Tegallalang Rice Terraces", "Seminyak Beach", "Mount Batur"],
        "avg_daily_cost": 80,
        "best_season": "summer",
        "timezone": "WITA",
    },
    "london": {
        "name": "London, UK",
        "attractions": ["Big Ben", "Tower of London", "British Museum", "Buckingham Palace", "Hyde Park"],
        "avg_daily_cost": 180,
        "best_season": "summer",
        "timezone": "GMT",
    },
    "default": {
        "name": "Your Destination",
        "attractions": ["City Tour", "Local Museum", "Famous Landmark", "Cultural Site", "Nature Reserve"],
        "avg_daily_cost": 100,
        "best_season": "any",
        "timezone": "UTC",
    }
}

ACTIVITY_TEMPLATES = [
    {"time": "08:00", "type": "breakfast", "description": "Breakfast at a local café"},
    {"time": "09:30", "type": "sightseeing", "description": "Morning sightseeing"},
    {"time": "12:30", "type": "lunch", "description": "Lunch at a recommended restaurant"},
    {"time": "14:00", "type": "activity", "description": "Afternoon activity"},
    {"time": "17:00", "type": "leisure", "description": "Free time / shopping"},
    {"time": "19:30", "type": "dinner", "description": "Dinner at a local restaurant"},
]


class ItineraryGenerator:
    def generate(self, data: dict) -> dict:
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")
        duration = (end_date - start_date).days + 1
        budget = float(data["budget"])
        destinations = data["destinations"]

        dest_info = self._get_destination_info(destinations)
        daily_budget = round(budget / max(duration, 1), 2)

        days = []
        for i in range(duration):
            current_date = start_date + timedelta(days=i)
            dest = dest_info[i % len(dest_info)]
            attractions = dest.get("attractions", DESTINATION_DATA["default"]["attractions"])
            random.shuffle(attractions)

            activities = []
            for j, tmpl in enumerate(ACTIVITY_TEMPLATES):
                act = dict(tmpl)
                if act["type"] == "sightseeing" and attractions:
                    act["description"] = f"Visit {attractions[j % len(attractions)]}"
                elif act["type"] == "activity" and len(attractions) > 1:
                    act["description"] = f"Explore {attractions[(j+1) % len(attractions)]}"
                activities.append(act)

            days.append({
                "day": i + 1,
                "date": current_date.strftime("%Y-%m-%d"),
                "destination": dest.get("name", "Unknown"),
                "estimated_cost": round(daily_budget, 2),
                "activities": activities,
                "accommodation": f"Hotel in {dest.get('name', 'City')}",
            })

        total_estimated_cost = sum(d["estimated_cost"] for d in days)

        return {
            "trip_id": f"TRIP-{random.randint(10000, 99999)}",
            "start_date": data["start_date"],
            "end_date": data["end_date"],
            "duration_days": duration,
            "total_budget": budget,
            "estimated_total_cost": total_estimated_cost,
            "destinations": [d.get("name") for d in dest_info],
            "days": days,
            "generated_at": datetime.utcnow().isoformat(),
        }

    def _get_destination_info(self, destinations: list) -> list:
        result = []
        for dest in destinations:
            key = dest.lower().strip()
            info = DESTINATION_DATA.get(key, dict(DESTINATION_DATA["default"]))
            info["name"] = dest.title() if key not in DESTINATION_DATA else info["name"]
            result.append(info)
        return result if result else [DESTINATION_DATA["default"]]

    def _get_destination_data(self, destinations: list) -> list:
        return self._get_destination_info(destinations)
