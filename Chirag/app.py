from flask import Flask, request, jsonify
from src.api.thematic_statistics import ThematicStatisticsAPI
from src.api.routing import RoutingAPI
from src.api.geoid import GeoidAPI
from src.utils.benchmark import benchmark_api_call
import os
from dotenv import load_dotenv

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Changed to port 5001
    app.run(debug=True, host='0.0.0.0', port=port)
