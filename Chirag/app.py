from flask import Flask, request, jsonify
from src.api.thematic_statistics import ThematicStatisticsAPI
from src.api.routing import RoutingAPI
from src.api.geoid import GeoidAPI
from src.api.postal_hospital import PostalHospitalAPI
from src.utils.benchmark import benchmark_api_call
import os
import sys
from dotenv import load_dotenv

# Add the Tanmay directory to the path to import database_manager
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Tanmay', 'multi_tool_agent'))

try:
    from database_manager import DatabaseManager
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Database manager not available: {e}")
    DATABASE_AVAILABLE = False

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"}), 200

@app.route('/api/thematic-stats', methods=['POST'])
def thematic_stats():
    try:
        data = request.get_json()
        coordinates = data.get('coordinates')
        parameters = data.get('parameters', {})
        
        if not coordinates:
            return jsonify({"error": "Coordinates are required"}), 400
            
        api = ThematicStatisticsAPI()
        result, query_time = benchmark_api_call(api.get_statistics, coordinates, parameters)
        
        return jsonify({
            "result": result,
            "query_time_ms": query_time,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/routing', methods=['POST'])
def routing():
    try:
        data = request.get_json()
        origin = data.get('origin')
        destination = data.get('destination')
        parameters = data.get('parameters', {})
        
        if not origin or not destination:
            return jsonify({"error": "Origin and destination coordinates are required"}), 400
            
        api = RoutingAPI()
        result, query_time = benchmark_api_call(api.get_route, origin, destination, parameters)
        
        return jsonify({
            "result": result,
            "query_time_ms": query_time,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/geoid', methods=['POST'])
def geoid():
    try:
        data = request.get_json()
        coordinates = data.get('coordinates')
        parameters = data.get('parameters', {})
        
        if not coordinates:
            return jsonify({"error": "Coordinates are required"}), 400
            
        api = GeoidAPI()
        result, query_time = benchmark_api_call(api.get_geoid_data, coordinates, parameters)
        
        return jsonify({
            "result": result,
            "query_time_ms": query_time,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/postal-hospital', methods=['POST'])
def postal_hospital():
    try:
        data = request.get_json()
        lat = data.get('lat')
        lng = data.get('lng')
        buffer = data.get('buffer', 3000)
        theme = data.get('theme', 'all')
        parameters = data.get('parameters', {})
        
        if lat is None or lng is None:
            return jsonify({"error": "Latitude and longitude are required"}), 400
            
        coordinates = {'lat': lat, 'lng': lng}
        api = PostalHospitalAPI()
        result, query_time = benchmark_api_call(api.get_proximity_data, coordinates, theme, buffer, parameters)
        
        return jsonify({
            "result": result,
            "query_time_ms": query_time,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/benchmark', methods=['POST'])
def benchmark_all():
    try:
        data = request.get_json()
        coordinates = data.get('coordinates')
        parameters = data.get('parameters', {})
        
        if not coordinates:
            return jsonify({"error": "Coordinates are required"}), 400
            
        results = {}
        
        # Thematic Statistics API
        thematic_api = ThematicStatisticsAPI()
        thematic_result, thematic_time = benchmark_api_call(thematic_api.get_statistics, coordinates, parameters)
        results["thematic_statistics"] = {
            "result": thematic_result,
            "query_time_ms": thematic_time
        }
        
        # Geoid API
        geoid_api = GeoidAPI()
        geoid_result, geoid_time = benchmark_api_call(geoid_api.get_geoid_data, coordinates, parameters)
        results["geoid"] = {
            "result": geoid_result,
            "query_time_ms": geoid_time
        }
        
        # For routing, we need origin and destination
        if 'destination' in data:
            routing_api = RoutingAPI()
            routing_result, routing_time = benchmark_api_call(routing_api.get_route, coordinates, data['destination'], parameters)
            results["routing"] = {
                "result": routing_result,
                "query_time_ms": routing_time
            }
        
        return jsonify({
            "results": results,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/map-interaction', methods=['POST'])
def save_map_interaction():
    """Save map interaction coordinates to the database"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available", "status": "error"}), 500
    
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        location_data = data.get('location_data')
        user_id = data.get('user_id')  # Optional user_id
        interaction_type = data.get('interaction_type', 'polygon_point')  # Default type
        
        if not session_id or latitude is None or longitude is None:
            return jsonify({
                "error": "session_id, latitude, and longitude are required", 
                "status": "error"
            }), 400
        
        # Convert coordinates to float
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            return jsonify({
                "error": "Invalid latitude or longitude format", 
                "status": "error"
            }), 400
            
        # Save to database
        db = DatabaseManager()
        success = db.save_map_interaction(session_id, latitude, longitude, location_data, user_id, interaction_type)
        
        if success:
            return jsonify({
                "message": "Map interaction saved successfully",
                "status": "success",
                "data": {
                    "session_id": session_id,
                    "coordinates": {"lat": latitude, "lng": longitude},
                    "interaction_type": interaction_type
                }
            }), 200
        else:
            return jsonify({
                "error": "Failed to save map interaction", 
                "status": "error"
            }), 500
            
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/map-data/<session_id>', methods=['GET'])
def get_map_data(session_id):
    """Get all map data for a specific session"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available", "status": "error"}), 500
    
    try:
        db = DatabaseManager()
        map_data = db.get_session_map_data(session_id)
        
        return jsonify({
            "status": "success",
            "data": map_data
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/map-interactions', methods=['GET'])
def get_all_map_interactions():
    """Get all map interactions with optional session filtering"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available", "status": "error"}), 500
    
    try:
        session_id = request.args.get('session_id')
        limit = request.args.get('limit', 100)
        
        try:
            limit = int(limit)
        except (ValueError, TypeError):
            limit = 100
            
        db = DatabaseManager()
        interactions = db.get_map_interactions(session_id, limit)
        
        return jsonify({
            "status": "success",
            "data": interactions,
            "count": len(interactions)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Changed to port 5001
    app.run(debug=True, host='0.0.0.0', port=port)
