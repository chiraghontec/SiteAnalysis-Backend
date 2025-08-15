#!/usr/bin/env python3
"""
KGIS Nearby Admin Hierarchy API Test Script
Tests the API endpoint: https://kgis.ksrsac.in:9000/genericwebservices/ws/nearbyadminhierarchy

This service accepts:
- Coordinates (latitude, longitude)
- Distance (search radius)
- Type of Coordinates (coordinate system)
- AOI (Area of Interest)

Returns administrative hierarchy: District, Taluk, Hobli and survey numbers
"""

import requests
import json
import time
from typing import Dict, Any, Optional
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class KGISNearbyAdminHierarchyTester:
    def __init__(self):
        self.base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/nearbyadminhierarchy"
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        
    def test_api_with_coordinates(self, 
                                 latitude: float, 
                                 longitude: float, 
                                 distance: float, 
                                 coord_type: str, 
                                 aoi: str) -> Dict[str, Any]:
        """
        Test the API with coordinate-based parameters
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate  
            distance: Search radius/distance
            coord_type: Type of coordinate system
            aoi: Area of Interest
        """
        print(f"\n{'='*60}")
        print(f"Testing Nearby Admin Hierarchy API")
        print(f"{'='*60}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Distance: {distance}")
        print(f"Coordinate Type: {coord_type}")
        print(f"AOI: {aoi}")
        print(f"{'='*60}")
        
        # Based on API documentation, use the correct parameter format
        try:
            print("Testing with correct API parameters...")
            params = {
                'coordinates': f"{latitude},{longitude}",  # Combined as per API doc
                'distance': int(distance),  # In meters
                'type': coord_type,  # DD or UTM
                'aoi': aoi  # d/t/h combinations
            }
            
            print(f"Parameters: {params}")
            
            start_time = time.time()
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=30
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Time: {response_time:.3f} seconds")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.text:
                try:
                    data = response.json()
                    print(f"Response JSON: {json.dumps(data, indent=2)}")
                    
                    # Parse and display administrative hierarchy if available
                    self._parse_admin_hierarchy(data)
                    
                except json.JSONDecodeError:
                    print(f"Response Text: {response.text}")
                    
            return {
                'latitude': latitude,
                'longitude': longitude,
                'distance': distance,
                'coord_type': coord_type,
                'aoi': aoi,
                'status_code': response.status_code,
                'data': response.text,
                'response_time': response_time
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return {'error': str(e), 'parameters': params}
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return {'error': str(e), 'parameters': params}

    def _parse_admin_hierarchy(self, data):
        """
        Parse and display the administrative hierarchy from the response
        """
        print(f"\n{'='*40}")
        print("ADMINISTRATIVE HIERARCHY RESULTS")
        print(f"{'='*40}")
        
        if isinstance(data, list):
            # Response is a list of administrative units
            for i, item in enumerate(data, 1):
                print(f"\nResult {i}:")
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"  {key}: {value}")
        
        elif isinstance(data, dict):
            # Look for common fields that might contain admin hierarchy
            hierarchy_fields = ['district', 'taluk', 'hobli', 'village', 'surveynumber', 'districtName', 'districtCode', 'talukName', 'talukCode', 'hobliName', 'hobliCode']
            
            for field in hierarchy_fields:
                if field in data:
                    print(f"{field}: {data[field]}")
            
            # If data is nested, try to extract hierarchy information
            if 'features' in data and isinstance(data['features'], list):
                print("\nFeatures found:")
                for i, feature in enumerate(data['features'][:5]):  # Show first 5 features
                    print(f"\nFeature {i+1}:")
                    if 'properties' in feature:
                        props = feature['properties']
                        for key, value in props.items():
                            print(f"  {key}: {value}")
            
            # Look for any other relevant administrative data
            admin_keys = [k for k in data.keys() if any(h in k.lower() for h in ['district', 'taluk', 'hobli', 'survey', 'name', 'code'])]
            if admin_keys:
                print("\nOther Administrative Data:")
                for key in admin_keys:
                    print(f"  {key}: {data[key]}")
        
        print(f"{'='*40}")
        
    def test_different_coordinate_systems(self, latitude: float, longitude: float, distance: float, aoi: str):
        """
        Test the API with different coordinate system types
        """
        coord_types = ['DD', 'UTM']  # Based on API documentation
        
        print(f"\n{'='*60}")
        print("TESTING DIFFERENT COORDINATE SYSTEMS")
        print(f"{'='*60}")
        
        results = []
        for coord_type in coord_types:
            print(f"\nTesting with coordinate type: {coord_type}")
            result = self.test_api_with_coordinates(latitude, longitude, distance, coord_type, aoi)
            results.append(result)
            time.sleep(1)  # Small delay between requests
        
        return results
        """
        Test the API with different coordinate system types
        """
        coord_types = ['WGS84', 'UTM', 'Geographic', 'Projected']
        
        print(f"\n{'='*60}")
        print("TESTING DIFFERENT COORDINATE SYSTEMS")
        print(f"{'='*60}")
        
        results = []
        for coord_type in coord_types:
            print(f"\nTesting with coordinate type: {coord_type}")
            result = self.test_api_with_coordinates(latitude, longitude, distance, coord_type, aoi)
            results.append(result)
            time.sleep(1)  # Small delay between requests
        
        return results

def main():
    """
    Main function to run nearby admin hierarchy API test with user input
    """
    print("KGIS Nearby Admin Hierarchy API Test Suite")
    print("=" * 60)
    print("This service finds District, Taluk, Hobli and survey numbers")
    print("based on coordinates, distance, coordinate type and AOI")
    print("=" * 60)
    
    tester = KGISNearbyAdminHierarchyTester()
    
    # Get user input for coordinates
    print("\nEnter the required parameters:")
    print()
    
    try:
        # Get latitude
        lat_input = input("Enter Latitude (e.g., 12.9716): ").strip()
        latitude = float(lat_input) if lat_input else 12.9716
        
        # Get longitude  
        lon_input = input("Enter Longitude (e.g., 77.5946): ").strip()
        longitude = float(lon_input) if lon_input else 77.5946
        
        # Get distance
        dist_input = input("Enter Distance/Radius in meters (e.g., 1000): ").strip()
        distance = float(dist_input) if dist_input else 1000.0
        
        # Get coordinate type
        coord_type = input("Enter Coordinate Type (DD for Decimal Degrees or UTM): ").strip()
        if not coord_type:
            coord_type = "DD"
        
        # Get AOI
        aoi = input("Enter AOI (d=District, t=Taluk, h=Hobli, e.g., 'd' or 'd,t,h'): ").strip()
        if not aoi:
            aoi = "d"
            
    except ValueError as e:
        print(f"Invalid input: {e}")
        print("Using default values...")
        latitude = 12.9716  # Bangalore coordinates
        longitude = 77.5946
        distance = 1000.0
        coord_type = "DD"
        aoi = "d"
    
    print(f"\nUsing values:")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    print(f"Distance: {distance}")
    print(f"Coordinate Type: {coord_type}")
    print(f"AOI: {aoi}")
    
    # Test with user provided parameters
    print("\nTesting API with your parameters...")
    result = tester.test_api_with_coordinates(latitude, longitude, distance, coord_type, aoi)
    
    # Ask if user wants to test different coordinate systems
    print(f"\n{'='*60}")
    test_more = input("Do you want to test with different coordinate systems? (y/n): ").strip().lower()
    
    if test_more in ['y', 'yes']:
        print("\nTesting with different coordinate systems...")
        coord_results = tester.test_different_coordinate_systems(latitude, longitude, distance, aoi)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    if 'error' not in result and result.get('status_code') == 200:
        print("✓ Nearby Admin Hierarchy API test successful!")
        print("🎉 API is working correctly!")
        print(f"Coordinates tested: ({latitude}, {longitude})")
        print(f"Search distance: {distance} meters")
        print(f"AOI: {aoi}")
        print("\n💡 Check the response data above for District, Taluk, Hobli and survey numbers")
    else:
        print("❌ Nearby Admin Hierarchy API test failed")
        print(f"Status Code: {result.get('status_code', 'Unknown')}")
        print(f"Coordinates tested: ({latitude}, {longitude})")
        print("\n🔍 The API may require different parameter values or coordinate format")
        
        # Suggest alternatives
        print("\n💡 Try these alternatives:")
        print("- Different coordinate system (WGS84, UTM)")
        print("- Different distance values")
        print("- Verify coordinate format and range")

if __name__ == "__main__":
    main()
