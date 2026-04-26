"""
Location Service - Distance, restaurants, and travel tips
"""
import math
import random
import os

CITY_COORDS = {
    "paris": (48.8566, 2.3522),
    "london": (51.5074, -0.1278),
    "new york": (40.7128, -74.0060),
    "tokyo": (35.6762, 139.6503),
    "bali": (-8.3405, 115.0920),
    "dubai": (25.2048, 55.2708),
    "singapore": (1.3521, 103.8198),
    "sydney": (-33.8688, 151.2093),
    "bangkok": (13.7563, 100.5018),
    "barcelona": (41.3851, 2.1734),
}

TRAVEL_TIPS_DB = {
    "paris": [
        "Buy a Paris Visite transport pass for unlimited metro travel.",
        "Book Eiffel Tower tickets online to skip the queue.",
        "Many museums are free on the first Sunday of the month.",
        "Tipping 5-10% is appreciated but not mandatory in restaurants.",
        "Carry a jacket — evenings can be cool even in summer.",
    ],
    "tokyo": [
        "Get a Suica or Pasmo IC card for seamless train travel.",
        "Convenience stores (7-Eleven, FamilyMart) sell excellent cheap meals.",
        "Restaurants with plastic food displays outside make ordering easy.",
        "JR Pass is worth it if travelling to multiple cities.",
        "Most ATMs in 7-Eleven convenience stores accept foreign cards.",
    ],
    "default": [
        "Always carry some local currency for small vendors.",
        "Research local customs and tipping etiquette before arrival.",
        "Download offline maps before travelling.",
        "Keep digital and physical copies of important documents.",
        "Travel insurance is strongly recommended.",
    ],
}

CUISINE_TYPES = ["Italian", "Japanese", "Mexican", "Indian", "Thai", "French", "Chinese", "Mediterranean"]


class LocationService:
    def calculate_distance(self, location1: str, location2: str) -> dict:
        c1 = CITY_COORDS.get(location1.lower(), self._random_coord())
        c2 = CITY_COORDS.get(location2.lower(), self._random_coord())
        dist_km = self._haversine(c1, c2)
        return {
            "from": location1.title(),
            "to": location2.title(),
            "distance_km": round(dist_km, 1),
            "distance_miles": round(dist_km * 0.621371, 1),
            "estimated_flight_hours": round(dist_km / 800, 1),
            "estimated_drive_hours": round(dist_km / 80, 1) if dist_km < 500 else None,
        }

    def find_restaurants(self, location: str, cuisine: str = None, budget: str = "moderate") -> list:
        price_map = {"budget": "$", "moderate": "$$", "expensive": "$$$", "luxury": "$$$$"}
        price_symbol = price_map.get(budget, "$$")
        cuisines = [cuisine] if cuisine else CUISINE_TYPES

        restaurants = []
        for i in range(5):
            cuis = cuisines[i % len(cuisines)]
            restaurants.append({
                "name": f"{location.title()} {cuis} Kitchen" if i == 0 else f"The {cuis} House {'I'*((i%3)+1)}",
                "cuisine": cuis,
                "location": location.title(),
                "price_range": price_symbol,
                "rating": round(random.uniform(3.8, 5.0), 1),
                "avg_meal_usd": {"$": 10, "$$": 25, "$$$": 50, "$$$$": 100}.get(price_symbol, 25),
                "open_now": random.choice([True, True, True, False]),
            })
        return restaurants

    def get_travel_tips(self, location: str) -> list:
        key = location.lower().strip()
        return TRAVEL_TIPS_DB.get(key, TRAVEL_TIPS_DB["default"])

    def _haversine(self, coord1, coord2) -> float:
        R = 6371
        lat1, lon1 = map(math.radians, coord1)
        lat2, lon2 = map(math.radians, coord2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))

    def _random_coord(self):
        return (random.uniform(-60, 70), random.uniform(-180, 180))
