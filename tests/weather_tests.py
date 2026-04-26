"""
Weather Dashboard Unit Tests
Comprehensive test suite for weather functionality
"""

import unittest
import json
from unittest.mock import patch, MagicMock
from app.services.weather_service import (
    WeatherDashboardService,
    WeatherDataProcessor,
    OpenWeatherMapAPI,
    WeatherAPIClient
)

class TestWeatherDataProcessor(unittest.TestCase):
    """Test weather data formatting and processing"""
    
    def setUp(self):
        self.processor = WeatherDataProcessor()
    
    def test_format_openweather_data(self):
        """Test OpenWeatherMap data formatting"""
        mock_data = {
            'name': 'Paris',
            'sys': {'country': 'FR', 'sunrise': 1619329200, 'sunset': 1619380800},
            'main': {
                'temp': 15.5,
                'feels_like': 14.2,
                'humidity': 65,
                'pressure': 1013
            },
            'weather': [{'description': 'partly cloudy', 'icon': '02d'}],
            'wind': {'speed': 12, 'deg': 230},
            'visibility': 10000,
            'clouds': {'all': 40},
            'dt': 1619351400
        }
        
        result = self.processor.format_openweather_data(mock_data)
        
        self.assertEqual(result['city'], 'Paris')
        self.assertEqual(result['country'], 'FR')
        self.assertEqual(result['temperature'], 15.5)
        self.assertEqual(result['description'], 'partly cloudy')
    
    def test_format_air_quality(self):
        """Test air quality data formatting"""
        mock_data = {
            'list': [{
                'dt': 1619351400,
                'main': {'aqi': 2},
                'components': {
                    'pm2_5': 12.5,
                    'pm10': 25.3
                }
            }]
        }
        
        result = self.processor.format_air_quality(mock_data)
        
        self.assertEqual(result['aqi_index'], 2)
        self.assertEqual(result['aqi_level'], 'Fair')
        self.assertIn('components', result)
    
    def test_format_forecast_data(self):
        """Test forecast data formatting"""
        mock_data = {
            'city': {'name': 'Paris', 'country': 'FR'},
            'list': [
                {
                    'dt': 1619351400,
                    'main': {'temp': 15.5, 'humidity': 65},
                    'weather': [{'description': 'cloudy'}],
                    'wind': {'speed': 12}
                },
                {
                    'dt': 1619437800,
                    'main': {'temp': 16.2, 'humidity': 60},
                    'weather': [{'description': 'cloudy'}],
                    'wind': {'speed': 14}
                }
            ]
        }
        
        result = self.processor.format_forecast_data(mock_data)
        
        self.assertEqual(result['city'], 'Paris')
        self.assertGreater(len(result['forecast']), 0)

class TestWeatherAPIIntegration(unittest.TestCase):
    """Test API integration"""
    
    @patch('app.services.weather_service.requests.Session.get')
    def test_openweather_current_weather(self, mock_get):
        """Test OpenWeatherMap current weather fetch"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'name': 'Paris',
            'main': {'temp': 15.5}
        }
        mock_get.return_value = mock_response
        
        api = OpenWeatherMapAPI()
        result = api.get_current_weather('Paris')
        
        self.assertIn('name', result)
    
    @patch('app.services.weather_service.requests.Session.get')
    def test_weather_comparison(self, mock_get):
        """Test comparing weather across cities"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'name': 'Paris',
            'main': {'temp': 15.5}
        }
        mock_get.return_value = mock_response
        
        service = WeatherDashboardService()
        cities = ['Paris', 'London']
        result = service.compare_weather(cities)
        
        self.assertEqual(len(result), 2)

class TestWeatherDashboardService(unittest.TestCase):
    """Test dashboard service"""
    
    @patch.object(WeatherDashboardService, 'get_weather_dashboard')
    def test_travel_recommendation(self, mock_dashboard):
        """Test travel weather recommendation"""
        mock_dashboard.return_value = {
            'city': 'Paris',
            'current_weather': {
                'temperature': 15.5,
                'wind_speed': 12,
                'description': 'clear'
            },
            'forecast': [
                {'common_description': 'clear'},
                {'common_description': 'clear'},
                {'common_description': 'clear'}
            ]
        }
        
        service = WeatherDashboardService()
        result = service.get_travel_weather_recommendation('Paris', 3)
        
        self.assertIn('suitable_for_travel', result)
        self.assertIn('recommendations', result)

class TestErrorHandling(unittest.TestCase):
    """Test error handling"""
    
    def test_invalid_city_error(self):
        """Test handling invalid city"""
        processor = WeatherDataProcessor()
        error_data = {'error': 'City not found'}
        
        result = processor.format_openweather_data(error_data)
        
        self.assertIn('error', result)
    
    def test_api_timeout_handling(self):
        """Test API timeout handling"""
        with patch('app.services.weather_service.requests.Session.get') as mock_get:
            mock_get.side_effect = Exception('Timeout')
            
            api = OpenWeatherMapAPI()
            result = api.get_current_weather('Paris')
            
            self.assertIn('error', result)

if __name__ == '__main__':
    unittest.main()
