"""
Main Flask Application
Entry point for the AI-Based Trip Planner
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

# Import models
from app.models.itinerary_generator import ItineraryGenerator
from app.models.recommendation_engine import RecommendationEngine
from app.models.budget_optimizer import BudgetOptimizer

# Import services
from app.services.api_client import IntegratedTravelAPI
from app.services.location_service import LocationService

# Import config
from app.config import config

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Initialize services
    itinerary_generator = ItineraryGenerator()
    recommendation_engine = RecommendationEngine()
    budget_optimizer = BudgetOptimizer()
    travel_api = IntegratedTravelAPI()
    location_service = LocationService()
    
    # Store in app context
    app.itinerary_generator = itinerary_generator
    app.recommendation_engine = recommendation_engine
    app.budget_optimizer = budget_optimizer
    app.travel_api = travel_api
    app.location_service = location_service
    
    # Routes
    
    @app.route('/', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'AI-Based Trip Planner',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/api/trips', methods=['POST'])
    def create_trip():
        """Create a new trip plan"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['start_date', 'end_date', 'budget', 'destinations']
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Missing required fields'}), 400
            
            # Generate itinerary
            itinerary = app.itinerary_generator.generate(data)
            
            return jsonify({
                'status': 'success',
                'itinerary': itinerary
            }), 201
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/recommendations', methods=['POST'])
    def get_recommendations():
        """Get personalized recommendations"""
        try:
            data = request.get_json()
            
            # Extract parameters
            user_preferences = data.get('preferences', {})
            destinations = data.get('destinations', [])
            top_n = data.get('top_n', 5)
            
            # Get recommendations
            recommendations = app.recommendation_engine.hybrid_recommendation(
                user_preferences,
                app.itinerary_generator._get_destination_data(destinations),
                top_n
            )
            
            return jsonify({
                'status': 'success',
                'recommendations': recommendations
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/budget/allocate', methods=['POST'])
    def allocate_budget():
        """Allocate budget across categories"""
        try:
            data = request.get_json()
            total_budget = data.get('budget', 5000)
            trip_duration = data.get('duration_days', 7)
            
            allocation = app.budget_optimizer.allocate_budget(
                total_budget, trip_duration
            )
            
            return jsonify({
                'status': 'success',
                'budget_allocation': allocation
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/budget/optimize', methods=['POST'])
    def optimize_budget():
        """Optimize itinerary for budget"""
        try:
            data = request.get_json()
            itinerary = data.get('itinerary', [])
            total_budget = data.get('budget', 5000)
            
            optimization = app.budget_optimizer.optimize_itinerary_cost(
                itinerary, total_budget
            )
            
            return jsonify({
                'status': 'success',
                'optimization': optimization
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/search/flights', methods=['GET'])
    def search_flights():
        """Search for flights"""
        try:
            origin = request.args.get('origin')
            destination = request.args.get('destination')
            departure_date = request.args.get('departure_date')
            
            if not all([origin, destination, departure_date]):
                return jsonify({'error': 'Missing required parameters'}), 400
            
            flights = app.travel_api.flights.search_flights(
                origin, destination, departure_date
            )
            
            return jsonify({
                'status': 'success',
                'flights': flights
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/search/hotels', methods=['GET'])
    def search_hotels():
        """Search for hotels"""
        try:
            city = request.args.get('city')
            check_in = request.args.get('check_in')
            check_out = request.args.get('check_out')
            
            if not all([city, check_in, check_out]):
                return jsonify({'error': 'Missing required parameters'}), 400
            
            hotels = app.travel_api.hotels.search_hotels(
                city, check_in, check_out
            )
            
            return jsonify({
                'status': 'success',
                'hotels': hotels
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/search/attractions', methods=['GET'])
    def search_attractions():
        """Search for attractions"""
        try:
            location = request.args.get('location')
            
            if not location:
                return jsonify({'error': 'Location parameter required'}), 400
            
            attractions = app.travel_api.locations.get_attractions(location)
            
            return jsonify({
                'status': 'success',
                'attractions': attractions
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/location/distance', methods=['GET'])
    def get_distance():
        """Calculate distance between locations"""
        try:
            location1 = request.args.get('from')
            location2 = request.args.get('to')
            
            if not all([location1, location2]):
                return jsonify({'error': 'Missing location parameters'}), 400
            
            distance = app.location_service.calculate_distance(
                location1, location2
            )
            
            return jsonify({
                'status': 'success',
                'distance': distance
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/location/restaurants', methods=['GET'])
    def find_restaurants():
        """Find restaurants in location"""
        try:
            location = request.args.get('location')
            cuisine = request.args.get('cuisine')
            budget = request.args.get('budget', 'moderate')
            
            if not location:
                return jsonify({'error': 'Location parameter required'}), 400
            
            restaurants = app.location_service.find_restaurants(
                location, cuisine, budget
            )
            
            return jsonify({
                'status': 'success',
                'restaurants': restaurants
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/location/tips', methods=['GET'])
    def get_travel_tips():
        """Get travel tips for location"""
        try:
            location = request.args.get('location')
            
            if not location:
                return jsonify({'error': 'Location parameter required'}), 400
            
            tips = app.location_service.get_travel_tips(location)
            
            return jsonify({
                'status': 'success',
                'tips': tips
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/weather', methods=['GET'])
    def get_weather():
        """Get weather forecast"""
        try:
            city = request.args.get('city')
            days = request.args.get('days', 7, type=int)
            
            if not city:
                return jsonify({'error': 'City parameter required'}), 400
            
            forecast = app.travel_api.weather.get_forecast(city, days)
            
            return jsonify({
                'status': 'success',
                'forecast': forecast
            }), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)
