#!/usr/bin/env python3
"""Test routing API with same-state coordinates"""

import sys
import os

# Add the src directory to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Add current directory for relative imports
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)

from src.api.routing import RoutingAPI
import json

def test_same_state_routing():
    """Test routing with coordinates from the same state"""
    api = RoutingAPI()
    
    # Test cases with same-state coordinates
    test_cases = [
        {
            "name": "Karnataka (Bangalore to Mysore)",
            "origin": {"lat": 12.9716, "lng": 77.5946},  # Bangalore
            "destination": {"lat": 12.3056, "lng": 76.6550}  # Mysore
        },
        {
            "name": "Delhi (Central Delhi to Gurgaon)",
            "origin": {"lat": 28.6139, "lng": 77.2090},  # Delhi
            "destination": {"lat": 28.4595, "lng": 77.0266}  # Gurgaon
        },
        {
            "name": "Maharashtra (Mumbai to Pune)",
            "origin": {"lat": 19.0760, "lng": 72.8777},  # Mumbai
            "destination": {"lat": 18.5204, "lng": 73.8567}  # Pune
        },
        {
            "name": "Tamil Nadu (Chennai to Coimbatore)",
            "origin": {"lat": 13.0827, "lng": 80.2707},  # Chennai
            "destination": {"lat": 11.0168, "lng": 76.9558}  # Coimbatore
        }
    ]
    
    print("Testing Routing API with same-state coordinates...\n")
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        print(f"  Origin: {test['origin']}")
        print(f"  Destination: {test['destination']}")
        
        try:
            result = api.get_route(test['origin'], test['destination'])
            
            if result and 'route_data' in result and result['route_data']:
                print(f"  ✅ Success! Route found")
                print(f"  Route type: {type(result['route_data'])}")
                if isinstance(result['route_data'], dict) and 'type' in result['route_data']:
                    print(f"  GeoJSON type: {result['route_data']['type']}")
                    if 'features' in result['route_data']:
                        print(f"  Features count: {len(result['route_data']['features'])}")
            elif 'error' in result:
                print(f"  ❌ Error: {result['error']}")
            else:
                print(f"  ⚠️  No route data returned")
                
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")
        
        print()

if __name__ == "__main__":
    test_same_state_routing()
