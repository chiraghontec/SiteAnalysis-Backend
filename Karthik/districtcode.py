#!/usr/bin/env python3
"""
KGIS District Code API Test Script
Tests the API endpoint: https://kgis.ksrsac.in:9000/genericwebservices/ws/districtcode
"""

import requests
import json
import time
from typing import Dict, Any
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class KGISDistrictCodeTester:
    def __init__(self):
        self.base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/districtcode"
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        
    def test_api_with_district_name(self, district_name: str) -> Dict[str, Any]:
        """
        Test the API with a district name parameter
        """
        print(f"\n{'='*50}")
        print(f"Testing District Code API with district name: {district_name}")
        print(f"{'='*50}")
        
        try:
            # Test with district name parameter
            print("Testing GET request with district name...")
            get_start_time = time.time()
            get_response = self.session.get(
                self.base_url,
                params={'districtname': district_name},
                timeout=30
            )
            get_end_time = time.time()
            get_response_time = get_end_time - get_start_time
            
            print(f"Status Code: {get_response.status_code}")
            print(f"Response Time: {get_response_time:.3f} seconds")
            print(f"Response Headers: {dict(get_response.headers)}")
            
            if get_response.text:
                try:
                    get_data = get_response.json()
                    print(f"Response JSON: {json.dumps(get_data, indent=2)}")
                except json.JSONDecodeError:
                    print(f"Response Text: {get_response.text}")
                    
            return {
                'district_name': district_name,
                'status_code': get_response.status_code,
                'data': get_response.text,
                'response_time': get_response_time
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return {'error': str(e), 'district_name': district_name}
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return {'error': str(e), 'district_name': district_name}

def main():
    """
    Main function to run district code API test with user input
    """
    print("KGIS District Code API Test Suite - District Name Lookup")
    print("=" * 60)
    
    tester = KGISDistrictCodeTester()
    
    # Get user input for district name
    print("Enter district name to lookup:")
    print()
    
    district_name = input("Enter District Name (e.g., Bangalore, Mysore, Hubli): ").strip()
    if not district_name:
        district_name = "Bangalore"
        print(f"Using default: {district_name}")
    
    print()
    print("Testing with your provided district name...")
    
    # Test with user provided district name
    result = tester.test_api_with_district_name(district_name)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    if 'error' not in result and result.get('status_code') == 200:
        print("✓ District Code API test successful!")
        print("🎉 API is working correctly!")
        print(f"District name used: {district_name}")
        print("\n💡 Check the response data above for the district code results")
    else:
        print("❌ District Code API test failed")
        print(f"Status Code: {result.get('status_code', 'Unknown')}")
        print(f"District name tested: {district_name}")
        print("\n🔍 The API may require different parameter values")

if __name__ == "__main__":
    main()
