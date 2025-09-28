"""
Simple test Flask server for map integration
"""
import sys
import os
import json
from flask import Flask, request, jsonify

# Add the Tanmay directory to the path to import database_manager
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Tanmay', 'multi_tool_agent'))

try:
    from database_manager import DatabaseManager
    DATABASE_AVAILABLE = True
    print("Database manager imported successfully")
except ImportError as e:
    print(f"Warning: Database manager not available: {e}")
    DATABASE_AVAILABLE = False

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"}), 200

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
        user_id = data.get('user_id', 1)  # Default user_id
        interaction_type = data.get('interaction_type', 'polygon_point')
        
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
        
        # Try to create agent session if it doesn't exist (ignore if it fails - might already exist)
        try:
            db.create_agent_session(session_id=session_id, user_id=user_id)
        except:
            pass  # Session might already exist
        
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
        print(f"Error in save_map_interaction: {e}")
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
        print(f"Error in get_map_data: {e}")
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    print("Starting Map Integration Test Server...")
    print("Database available:", DATABASE_AVAILABLE)
    app.run(debug=True, host='127.0.0.1', port=5001)