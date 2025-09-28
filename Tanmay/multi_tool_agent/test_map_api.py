#!/usr/bin/env python3
"""
Test the Map API endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5001"

def test_map_api():
    """Test the map API endpoints"""
    print("🌐 Testing Map API Endpoints...")
    
    try:
        # Test 1: Health check
        print("\n📍 Test 1: Health check...")
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test 2: Save map interaction
        print("\n📍 Test 2: Save map interaction...")
        session_id = f"api_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        map_data = {
            "session_id": session_id,
            "latitude": 28.6139,
            "longitude": 77.2090,
            "location_data": {
                "polygon_id": "test_polygon_api",
                "point_index": 0,
                "geometry_type": "Polygon",
                "source": "api_test"
            },
            "user_id": 1,
            "interaction_type": "polygon_point"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/map-interaction", 
            json=map_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Map interaction saved via API")
            print(f"   Session ID: {result['data']['session_id']}")
            print(f"   Coordinates: {result['data']['coordinates']}")
        else:
            print(f"❌ Failed to save map interaction: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Test 3: Get map data
        print("\n📍 Test 3: Get map data...")
        response = requests.get(f"{BASE_URL}/api/map-data/{session_id}", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Map data retrieved via API")
            print(f"   Total interactions: {result['data']['total_interactions']}")
            print(f"   Coordinates: {len(result['data']['coordinates'])} points")
            
            if result['data']['coordinates']:
                coord = result['data']['coordinates'][0]
                print(f"   First coordinate: lat={coord['lat']}, lng={coord['lng']}")
        else:
            print(f"❌ Failed to get map data: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Test 4: Get all map interactions
        print("\n📍 Test 4: Get all map interactions...")
        response = requests.get(f"{BASE_URL}/api/map-interactions?limit=5", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ All map interactions retrieved via API")
            print(f"   Total interactions: {result['count']}")
        else:
            print(f"❌ Failed to get all interactions: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the Flask app is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_map_api()
    if success:
        print("\n🎉 All API tests PASSED!")
        print("\n📋 Integration Status:")
        print("   ✅ Backend Server: Running")
        print("   ✅ Database Connection: Working")
        print("   ✅ Map API Endpoints: Working")
        print("   ✅ Data Storage: Working")
        print("   ✅ Data Retrieval: Working")
        print("\n🚀 Ready to use with map.html!")
    else:
        print("\n❌ API tests FAILED!")
        print("   Please check the server and database connection.")