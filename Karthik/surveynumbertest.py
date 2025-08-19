#!/usr/bin/env python3
"""
KGIS Survey Number API Test Script
Tests the API endpoint: https://kgis.ksrsac.in:9000/genericwebservices/ws/surveyno

This service accepts:
- KGIS Village Code
- Coordinates (latitude, longitude) 
- Distance (search radius)
- Type of Coordinates (DD or UTM)

Returns survey numbers with village name and administrative hierarchy
"""

import requests
import json
import time
from typing import Dict, Any, List
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class KGISSurveyNumberTester:
    def __init__(self):
        self.base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/surveyno"
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        
    def test_api_with_parameters(self, 
                                village_code: str, 
                                coordinates: str, 
                                coord_type: str, 
                                distance: int) -> Dict[str, Any]:
        """
        Test the Survey Number API with required parameters
        
        Args:
            village_code: KGIS Village Code (e.g., 201020003)
            coordinates: Coordinates in format "lat,lon" or "x,y" 
            coord_type: DD (Decimal Degree) or UTM
            distance: Search radius in meters
        """
        print(f"\n{'='*60}")
        print(f"Testing Survey Number API")
        print(f"{'='*60}")
        print(f"Village Code: {village_code}")
        print(f"Coordinates: {coordinates}")
        print(f"Coordinate Type: {coord_type}")
        print(f"Distance: {distance} meters")
        print(f"{'='*60}")
        
        try:
            # Prepare parameters based on API documentation
            params = {
                'villagecode': village_code,
                'coordinates': coordinates,
                'type': coord_type,
                'distance': distance
            }
            
            print("Testing GET request with survey number parameters...")
            print(f"Parameters: {params}")
            
            start_time = time.time()
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=30
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"\nStatus Code: {response.status_code}")
            print(f"Response Time: {response_time:.3f} seconds")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.text:
                try:
                    data = response.json()
                    print(f"\nResponse JSON: {json.dumps(data, indent=2)}")
                    
                    # Parse and display survey numbers and admin hierarchy
                    self._parse_survey_response(data)
                    
                    # If no survey numbers found, suggest alternatives
                    if isinstance(data, dict) and not data.get('surveynumber'):
                        print(f"\n⚠️  WARNING: No survey numbers found in response!")
                        print(f"📍 Administrative hierarchy is available, but survey data is empty.")
                        print(f"💡 This could mean:")
                        print(f"   - Coordinates are outside survey boundaries")
                        print(f"   - Village code doesn't match the coordinate location")
                        print(f"   - Survey data is not available for this area")
                        print(f"   - Distance radius needs to be adjusted")
                    
                except json.JSONDecodeError:
                    print(f"\nResponse Text: {response.text}")
                    
            return {
                'village_code': village_code,
                'coordinates': coordinates,
                'coord_type': coord_type,
                'distance': distance,
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

    def _parse_survey_response(self, data: Dict[str, Any]):
        """
        Parse and display the survey number response data
        """
        print(f"\n{'='*50}")
        print("SURVEY NUMBER RESULTS")
        print(f"{'='*50}")
        
        if isinstance(data, dict):
            # Parse administrative hierarchy
            if 'adminhierarchy' in data and isinstance(data['adminhierarchy'], list):
                print("\n🏛️ ADMINISTRATIVE HIERARCHY:")
                for i, admin in enumerate(data['adminhierarchy'], 1):
                    print(f"\nLocation {i}:")
                    print(f"  District: {admin.get('districtName', 'N/A')}")
                    print(f"  Taluk: {admin.get('talukName', 'N/A')}")
                    print(f"  Hobli: {admin.get('hobliName', 'N/A')}")
                    print(f"  Village: {admin.get('villageName', 'N/A')}")
            
            # Parse survey numbers
            if 'surveynumber' in data and isinstance(data['surveynumber'], list):
                survey_numbers = data['surveynumber']
                print(f"\n📋 SURVEY NUMBERS ({len(survey_numbers)} found):")
                
                # Group survey numbers by type
                regular_numbers = []
                special_features = []
                
                for survey in survey_numbers:
                    sno = survey.get('sno', '')
                    if sno.upper() in ['STREAM', 'ROAD', 'SETTLEMENT']:
                        special_features.append(sno)
                    else:
                        regular_numbers.append(sno)
                
                # Display regular survey numbers
                if regular_numbers:
                    print(f"\n📍 Regular Survey Numbers ({len(regular_numbers)}):")
                    # Display in rows of 10 for better readability
                    for i in range(0, len(regular_numbers), 10):
                        row = regular_numbers[i:i+10]
                        print(f"  {', '.join(row)}")
                
                # Display special features
                if special_features:
                    print(f"\n🌍 Special Features ({len(special_features)}):")
                    feature_counts = {}
                    for feature in special_features:
                        feature_counts[feature] = feature_counts.get(feature, 0) + 1
                    
                    for feature, count in feature_counts.items():
                        print(f"  {feature}: {count} occurrences")
                        
                print(f"\n📊 SUMMARY:")
                print(f"  Total Survey Numbers: {len(survey_numbers)}")
                print(f"  Regular Numbers: {len(regular_numbers)}")
                print(f"  Special Features: {len(special_features)}")
        
        print(f"{'='*50}")

    def test_alternative_parameters(self, base_village_code: str, base_coordinates: str, coord_type: str, distance: int):
        """
        Test with alternative parameter combinations to find working survey data
        """
        print(f"\n{'='*60}")
        print("TESTING ALTERNATIVE PARAMETER COMBINATIONS")
        print(f"{'='*60}")
        
        # Try different village code formats
        village_codes = [
            base_village_code,
            base_village_code.lstrip('0'),  # Remove leading zeros
            '0' + base_village_code if not base_village_code.startswith('0') else base_village_code[1:],
            '02' + base_village_code.lstrip('0'),  # Different prefix
        ]
        
        # Try different distances
        distances = [distance, 1000, 2000, 5000, 10000]
        
        working_combinations = []
        
        for vc in village_codes:
            for dist in distances:
                print(f"\n🔍 Testing: Village Code={vc}, Distance={dist}m")
                
                params = {
                    'villagecode': vc,
                    'coordinates': base_coordinates,
                    'type': coord_type,
                    'distance': dist
                }
                
                try:
                    response = self.session.get(self.base_url, params=params, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        survey_count = len(data.get('surveynumber', []))
                        admin_count = len(data.get('adminhierarchy', []))
                        
                        print(f"   ✅ Status: 200, Admin: {admin_count}, Surveys: {survey_count}")
                        
                        if survey_count > 0:
                            working_combinations.append({
                                'village_code': vc,
                                'distance': dist,
                                'survey_count': survey_count,
                                'admin_count': admin_count,
                                'data': data
                            })
                            print(f"   🎉 FOUND SURVEY DATA! {survey_count} survey numbers")
                        else:
                            print(f"   ⚠️  No survey data found")
                    else:
                        print(f"   ❌ Status: {response.status_code}")
                        
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                
                # Don't test all combinations if we found working ones
                if len(working_combinations) >= 2:
                    break
            
            if len(working_combinations) >= 2:
                break
        
        return working_combinations

    def test_different_coordinate_types(self, village_code: str, distance: int):
        """
        Test the API with different coordinate types (DD and UTM)
        """
        print(f"\n{'='*60}")
        print("TESTING DIFFERENT COORDINATE TYPES")
        print(f"{'='*60}")
        
        # Sample coordinates from the API documentation
        test_cases = [
            {
                'name': 'Decimal Degree (DD)',
                'coordinates': '16.208,75.739',
                'type': 'DD'
            },
            {
                'name': 'UTM Coordinates',
                'coordinates': '1853272.6735999994,546739.9227999998',
                'type': 'UTM'
            }
        ]
        
        results = []
        for test_case in test_cases:
            print(f"\n🧪 Testing {test_case['name']}:")
            result = self.test_api_with_parameters(
                village_code, 
                test_case['coordinates'], 
                test_case['type'], 
                distance
            )
            results.append({
                'test_name': test_case['name'],
                'result': result
            })
            time.sleep(1)  # Small delay between requests
        
        return results

    def test_different_distances(self, village_code: str, coordinates: str, coord_type: str):
        """
        Test the API with different search distances
        """
        print(f"\n{'='*60}")
        print("TESTING DIFFERENT SEARCH DISTANCES")
        print(f"{'='*60}")
        
        distances = [1000, 2500, 5000, 10000]  # Different distances in meters
        
        results = []
        for distance in distances:
            print(f"\n🎯 Testing distance: {distance} meters")
            result = self.test_api_with_parameters(village_code, coordinates, coord_type, distance)
            
            # Count survey numbers if successful
            if result.get('status_code') == 200 and result.get('data'):
                try:
                    data = json.loads(result['data'])
                    survey_count = len(data.get('surveynumber', []))
                    print(f"   📊 Found {survey_count} survey numbers at {distance}m radius")
                except:
                    pass
            
            results.append({
                'distance': distance,
                'result': result
            })
            time.sleep(1)  # Small delay between requests
        
        return results

def main():
    """
    Main function to run survey number API test with user input
    """
    print("KGIS Survey Number API Test Suite")
    print("=" * 60)
    print("This service fetches survey numbers with village name")
    print("based on KGIS village code, coordinates, coordinate type and distance")
    print("=" * 60)
    
    tester = KGISSurveyNumberTester()
    
    # Get user input for parameters
    print("\nEnter the required parameters:")
    print()
    
    try:
        # Get village code
        village_code = input("Enter KGIS Village Code (e.g., 0201020003): ").strip()
        if not village_code:
            village_code = "0201020003"
            print(f"Using default: {village_code}")
        
        # Get coordinate type first to determine coordinate format
        coord_type = input("Enter Coordinate Type (DD or UTM): ").strip().upper()
        if coord_type not in ['DD', 'UTM']:
            coord_type = "DD"
            print(f"Using default: {coord_type}")
        
        # Get coordinates based on type
        if coord_type == "DD":
            print("Enter coordinates in Decimal Degree format (latitude,longitude):")
            coordinates = input("Coordinates (e.g., 16.208,75.739): ").strip()
            if not coordinates:
                coordinates = "16.208,75.739"
                print(f"Using default: {coordinates}")
        else:  # UTM
            print("Enter coordinates in UTM format (x,y):")
            coordinates = input("Coordinates (e.g., 1853272.6735999994,546739.9227999998): ").strip()
            if not coordinates:
                coordinates = "1853272.6735999994,546739.9227999998"
                print(f"Using default: {coordinates}")
        
        # Get distance
        distance_input = input("Enter Distance in meters (e.g., 5000): ").strip()
        distance = int(distance_input) if distance_input else 5000
        
    except ValueError as e:
        print(f"Invalid input: {e}")
        print("Using default values...")
        village_code = "0201020003"
        coordinates = "16.208,75.739"
        coord_type = "DD"
        distance = 5000
    
    print(f"\nUsing values:")
    print(f"Village Code: {village_code}")
    print(f"Coordinates: {coordinates}")
    print(f"Coordinate Type: {coord_type}")
    print(f"Distance: {distance} meters")
    
    # Test with user provided parameters
    print("\nTesting API with your parameters...")
    result = tester.test_api_with_parameters(village_code, coordinates, coord_type, distance)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    if 'error' not in result and result.get('status_code') == 200:
        print("✅ Survey Number API test successful!")
        print("🎉 API is working correctly!")
        print(f"Village Code: {village_code}")
        print(f"Coordinates: {coordinates} ({coord_type})")
        print(f"Search Distance: {distance} meters")
        print("\n💡 Check the response data above for survey numbers and administrative hierarchy")
    else:
        print("❌ Survey Number API test failed")
        print(f"Status Code: {result.get('status_code', 'Unknown')}")
        print(f"Village Code: {village_code}")
        print("\n🔍 Try these troubleshooting steps:")
        print("- Verify the KGIS Village Code is correct")
        print("- Check coordinate format matches the type (DD or UTM)")
        print("- Ensure coordinates are within Karnataka state")
        print("- Try different distance values")

if __name__ == "__main__":
    main()
