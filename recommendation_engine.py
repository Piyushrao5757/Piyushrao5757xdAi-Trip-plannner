"""
Integrated Travel API Client
Wraps external APIs (flights, hotels, weather) with mock fallbacks
"""
import os
import random
import requests
from datetime import datetime, timedelta


class FlightAPI:
    def search_flights(self, origin: str, destination: str, departure_date: str) -> list:
        key = os.environ.get("AMADEUS_API_KEY", "")
        if key:
            return self._real_search(origin, destination, departure_date, key)
        return self._mock_flights(origin, destination, departure_date)

    def _mock_flights(self, origin, destination, departure_date) -> list:
        airlines = ["Air India", "IndiGo", "Emirates", "Singapore Airlines", "British Airways"]
        flights = []
        for i in range(4):
            dep_hour = 6 + i * 4
            price = random.randint(250, 1200)
            flights.append({
                "flight_id": f"FL{random.randint(1000,9999)}",
                "airline": random.choice(airlines),
                "origin": origin.upper(),
                "destination": destination.upper(),
                "departure": f"{departure_date}T{dep_hour:02d}:00:00",
                "arrival": f"{departure_date}T{(dep_hour+8)%24:02d}:30:00",
                "duration_hours": round(random.uniform(2, 14), 1),
                "price_usd": price,
                "seats_available": random.randint(5, 50),
                "class": "Economy",
            })
        return sorted(flights, key=lambda x: x["price_usd"])

    def _real_search(self, origin, destination, departure_date, api_key):
        # Amadeus API integration point
        return self._mock_flights(origin, destination, departure_date)


class HotelAPI:
    def search_hotels(self, city: str, check_in: str, check_out: str) -> list:
        key = os.environ.get("BOOKING_COM_API_KEY", "")
        if key:
            return self._real_search(city, check_in, check_out, key)
        return self._mock_hotels(city, check_in, check_out)

    def _mock_hotels(self, city, check_in, check_out) -> list:
        ci = datetime.strptime(check_in, "%Y-%m-%d")
        co = datetime.strptime(check_out, "%Y-%m-%d")
        nights = max((co - ci).days, 1)

        hotel_types = [
            ("Budget Inn", 1, 40),
            ("City Hostel", 1, 25),
            ("Comfort Stay", 3, 80),
            ("Grand Hotel", 4, 150),
            ("Luxury Palace", 5, 300),
        ]
        hotels = []
        for name, stars, base_price in hotel_types:
            nightly = base_price + random.randint(-10, 30)
            hotels.append({
                "hotel_id": f"HTL{random.randint(1000,9999)}",
                "name": f"{city.title()} {name}",
                "city": city.title(),
                "stars": stars,
                "rating": round(random.uniform(3.5, 5.0), 1),
                "price_per_night_usd": nightly,
                "total_price_usd": nightly * nights,
                "nights": nights,
                "amenities": self._amenities(stars),
                "free_cancellation": stars >= 3,
            })
        return hotels

    def _amenities(self, stars):
        base = ["WiFi", "24h Reception"]
        if stars >= 3:
            base += ["Breakfast", "AC", "Room Service"]
        if stars >= 4:
            base += ["Pool", "Gym", "Spa"]
        if stars >= 5:
            base += ["Concierge", "Fine Dining", "Airport Transfer"]
        return base

    def _real_search(self, city, check_in, check_out, api_key):
        return self._mock_hotels(city, check_in, check_out)


class WeatherAPI:
    def get_forecast(self, city: str, days: int = 7) -> list:
        key = os.environ.get("OPENWEATHER_API_KEY", "")
        if key:
            return self._real_forecast(city, days, key)
        return self._mock_forecast(city, days)

    def _mock_forecast(self, city, days) -> list:
        conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Clear"]
        forecast = []
        for i in range(days):
            date = (datetime.utcnow() + timedelta(days=i)).strftime("%Y-%m-%d")
            forecast.append({
                "date": date,
                "condition": random.choice(conditions),
                "temp_high_c": random.randint(18, 35),
                "temp_low_c": random.randint(10, 22),
                "humidity_pct": random.randint(40, 85),
                "rain_chance_pct": random.randint(0, 60),
                "wind_kmh": random.randint(5, 30),
            })
        return forecast

    def _real_forecast(self, city, days, api_key):
        try:
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {"q": city, "appid": api_key, "units": "metric", "cnt": days * 8}
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                raw = resp.json().get("list", [])
                seen = {}
                for item in raw:
                    date = item["dt_txt"][:10]
                    if date not in seen:
                        seen[date] = {
                            "date": date,
                            "condition": item["weather"][0]["main"],
                            "temp_high_c": item["main"]["temp_max"],
                            "temp_low_c": item["main"]["temp_min"],
                            "humidity_pct": item["main"]["humidity"],
                            "rain_chance_pct": int(item.get("pop", 0) * 100),
                            "wind_kmh": round(item["wind"]["speed"] * 3.6, 1),
                        }
                return list(seen.values())[:days]
        except Exception:
            pass
        return self._mock_forecast(city, days)


class LocationsAPI:
    def get_attractions(self, location: str) -> list:
        attractions_db = {
            "paris": ["Eiffel Tower", "Louvre Museum", "Arc de Triomphe", "Musée d'Orsay", "Sainte-Chapelle"],
            "tokyo": ["Senso-ji Temple", "Tokyo Skytree", "Shibuya Crossing", "Meiji Shrine", "Shinjuku Gyoen"],
            "london": ["Big Ben", "Tower of London", "British Museum", "Tate Modern", "Covent Garden"],
            "new york": ["Central Park", "Statue of Liberty", "Times Square", "Brooklyn Bridge", "High Line"],
            "bali": ["Tanah Lot", "Ubud Palace", "Tegallalang", "Uluwatu Temple", "Mount Batur"],
        }
        key = location.lower().strip()
        names = attractions_db.get(key, [f"{location.title()} Museum", f"{location.title()} Park", "Historic Center", "Local Market", "Viewpoint"])
        return [
            {
                "name": name,
                "location": location.title(),
                "rating": round(random.uniform(4.0, 5.0), 1),
                "entry_fee_usd": random.choice([0, 0, 10, 15, 20, 25]),
                "duration_hours": round(random.uniform(1, 4), 1),
                "category": random.choice(["Museum", "Landmark", "Nature", "Culture", "Historic"]),
            }
            for name in names
        ]


class IntegratedTravelAPI:
    def __init__(self):
        self.flights = FlightAPI()
        self.hotels = HotelAPI()
        self.weather = WeatherAPI()
        self.locations = LocationsAPI()
