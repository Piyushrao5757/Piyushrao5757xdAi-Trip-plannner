# Weather Dashboard API Documentation

## Overview
The Weather Dashboard provides comprehensive real-time weather data, forecasts, and travel recommendations using OpenWeatherMap API integration.

## Features
- ✅ Real-time weather data
- ✅ 5-day weather forecasts
- ✅ Air quality monitoring
- ✅ Multi-city comparison
- ✅ Travel suitability assessment
- ✅ Weather alerts and warnings
- ✅ Interactive web dashboard

## API Endpoints

### 1. Weather Dashboard
**Endpoint:** `GET /api/weather/dashboard/<city>`

Returns complete weather overview for a city including current weather, forecast, and air quality.

**Example Request:**
```bash
curl http://localhost:5000/api/weather/dashboard/Paris
```

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "city": "Paris",
    "current_weather": {
      "city": "Paris",
      "country": "FR",
      "temperature": 15.5,
      "feels_like": 14.2,
      "humidity": 65,
      "wind_speed": 12,
      "description": "partly cloudy"
    },
    "forecast": [
      {
        "date": "2026-04-26",
        "min_temp": 13.2,
        "max_temp": 18.5,
        "common_description": "cloudy"
      }
    ],
    "air_quality": {
      "aqi_level": "Fair",
      "aqi_index": 2
    }
  }
}
```

### 2. Current Weather
**Endpoint:** `GET /api/weather/current/<city>`

Returns only current weather conditions.

**Example Request:**
```bash
curl http://localhost:5000/api/weather/current/London
```

### 3. Forecast
**Endpoint:** `GET /api/weather/forecast/<city>?days=5`

Returns weather forecast for specified number of days (default: 5).

**Parameters:**
- `days` (optional): Number of days to forecast (1-5)

**Example Request:**
```bash
curl http://localhost:5000/api/weather/forecast/Tokyo?days=3
```

### 4. Air Quality
**Endpoint:** `GET /api/weather/air-quality/<city>`

Returns air quality index and pollutant levels.

**Example Request:**
```bash
curl http://localhost:5000/api/weather/air-quality/Delhi
```

### 5. Compare Cities
**Endpoint:** `POST /api/weather/compare`

Compare weather across multiple cities.

**Request Body:**
```json
{
  "cities": ["Paris", "London", "Tokyo"]
}
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/weather/compare \
  -H "Content-Type: application/json" \
  -d '{"cities": ["Paris", "London", "Tokyo"]}'
```

### 6. Travel Recommendation
**Endpoint:** `GET /api/weather/travel-recommendation/<city>?duration=3`

Returns travel suitability assessment and recommendations.

**Parameters:**
- `duration` (optional): Trip duration in days (default: 3)

**Example Request:**
```bash
curl http://localhost:5000/api/weather/travel-recommendation/Barcelona?duration=5
```

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "city": "Barcelona",
    "suitable_for_travel": true,
    "suitability_score": 85.5,
    "recommendations": [
      "Perfect weather for outdoor activities!",
      "Bring light clothing"
    ],
    "warnings": []
  }
}
```

### 7. Weather Alerts
**Endpoint:** `GET /api/weather/alerts/<city>`

Returns weather warnings and alerts.

**Example Request:**
```bash
curl http://localhost:5000/api/weather/alerts/Miami
```

### 8. Multi-City Dashboard
**Endpoint:** `POST /api/weather/multi-city`

Get dashboards for multiple cities in one request.

**Request Body:**
```json
{
  "cities": ["Paris", "Rome", "Barcelona"]
}
```

### 9. Extreme Weather Detection
**Endpoint:** `GET /api/weather/extreme-weather?cities=Miami&cities=NewYork`

Detect extreme weather conditions across multiple cities.

**Example Request:**
```bash
curl "http://localhost:5000/api/weather/extreme-weather?cities=Miami&cities=NewYork"
```

## Response Codes

- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters or missing data
- `500 Internal Server Error` - Server error

## Data Fields

### Current Weather Object
```json
{
  "city": "string",
  "country": "string",
  "coordinates": {
    "latitude": "float",
    "longitude": "float"
  },
  "temperature": "float (°C)",
  "feels_like": "float (°C)",
  "humidity": "integer (%)",
  "pressure": "integer (mb)",
  "description": "string",
  "wind_speed": "float (m/s)",
  "wind_direction": "integer (degrees)",
  "visibility": "integer (meters)",
  "clouds": "integer (%)",
  "sunrise": "unix timestamp",
  "sunset": "unix timestamp"
}
```

### Forecast Day Object
```json
{
  "date": "YYYY-MM-DD",
  "min_temp": "float (°C)",
  "max_temp": "float (°C)",
  "avg_temp": "float (°C)",
  "common_description": "string",
  "max_wind_speed": "float (m/s)"
}
```

### Air Quality Object
```json
{
  "aqi_index": "integer (1-5)",
  "aqi_level": "string (Good/Fair/Moderate/Poor/Very Poor)",
  "components": {
    "pm2_5": "float",
    "pm10": "float",
    "no2": "float",
    "o3": "float"
  }
}
```

## Travel Suitability Scores

- **Excellent** (85-100): Perfect travel conditions
- **Good** (60-84): Suitable for most activities
- **Moderate** (40-59): Variable conditions, plan accordingly
- **Poor** (0-39): Not recommended

## Air Quality Index (AQI)

- **1 - Good**: Air pollution poses little to no risk
- **2 - Fair**: Air quality is acceptable
- **3 - Moderate**: Sensitive groups may experience health effects
- **4 - Poor**: General public may begin to experience health effects
- **5 - Very Poor**: Health alert; health effects are severe

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Create `.env` file:
```
OPENWEATHER_API_KEY=your_key_here
WEATHER_API_KEY=your_weatherapi_key_here
FLASK_ENV=development
```

Get free API keys:
- OpenWeatherMap: https://openweathermap.org/api
- WeatherAPI: https://www.weatherapi.com/

### 3. Run Application
```bash
python app/main.py
```

### 4. Access Dashboard
```
http://localhost:5000/api/weather/dashboard-view
```

## Testing

### Run Tests
```bash
python -m pytest tests/weather_tests.py -v
```

### Test Current Weather
```bash
curl http://localhost:5000/api/weather/current/Paris
```

### Test Forecast
```bash
curl http://localhost:5000/api/weather/forecast/London?days=5
```

### Test Comparison
```bash
curl -X POST http://localhost:5000/api/weather/compare \
  -H "Content-Type: application/json" \
  -d '{"cities": ["Paris", "London", "New York"]}'
```

## Integration with Trip Planner

The weather dashboard integrates seamlessly with the AI Trip Planner:

```python
from app.services.weather_service import WeatherDashboardService

service = WeatherDashboardService()

# Get weather for trip destination
weather = service.get_weather_dashboard('Barcelona')

# Get travel recommendation
recommendation = service.get_travel_weather_recommendation('Barcelona', trip_duration=5)

# Compare multiple destinations
comparison = service.compare_weather(['Paris', 'Barcelona', 'Rome'])
```

## Error Handling

All endpoints return error responses in the format:
```json
{
  "status": "error",
  "error": "Error description"
}
```

## Rate Limiting

- OpenWeatherMap Free: 1000 calls/day
- WeatherAPI Free: 1,000,000 calls/month

## Caching

Weather data is cached for optimal performance:
- Current weather: 10 minutes
- Forecast: 1 hour
- Air quality: 30 minutes

## Performance Tips

1. Use city names or coordinates consistently
2. Batch requests when comparing multiple cities
3. Cache results on the client side
4. Use appropriate update intervals (avoid unnecessary API calls)

## Support

For issues or feature requests, please refer to the main project README.
