#!/usr/bin/env python3
"""
KGIS Election Jurisdiction Hierarchy API Test Script
Tests the API endpoint: https://kgis.ksrsac.in:9000/boundarywebservices/ws/getJurisdictionBoundary

This service fetches jurisdiction hierarchy for given layer and coordinates.

Parameters:
- coordinates: Latitude,Longitude (DD) or X,Y (UTM)
- code: Layer code (01-05 for different services)
- type: DD (Decimal Degree) or UTM

Layer Codes:
01 - Election: Polling booth, Assembly & Parliament constituency info
02 - Home: Police station hierarchy
03 - Education: Block and district hierarchy  
04 - Bescom: Power distribution hierarchy
05 - Health: Health center and district hierarchy
"""

import requests
import json
import time
import urllib3
from typing import Dict, Any

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_layer_info():
    """
    Return information about available layer codes
    """
    return {
        "01": {
            "name": "Election",
            "description": "Returns jurisdictional hierarchy of Election/Constituency boundaries",
            "outputs": ["Polling Booth Number", "Polling Booth Name", "Assembly Constituency Number", 
                       "Assembly Constituency Name", "Parliament Constituency Number", "Parliament Constituency Name"]
        },
        "02": {
            "name": "Home",
            "description": "Returns jurisdictional hierarchy of Police Station",
            "outputs": ["Police Station ID", "Police Station Name", "Circle ID", "Circle Name",
                       "Sub Division ID", "Sub Division Name", "Division ID", "Division Name"]
        },
        "03": {
            "name": "Education", 
            "description": "Returns jurisdictional hierarchy for Education",
            "outputs": ["Block Code", "Block Name", "District Code", "District Name"]
        },
        "04": {
            "name": "Bescom",
            "description": "Returns jurisdictional hierarchy of Bescom (Power Distribution)",
            "outputs": ["Section Code", "Section Name", "Sub Division Code", "Sub Division Name",
                       "Division Code", "Division Name", "Circle Code", "Circle Name", 
                       "Zonal Code", "Zonal Name"]
        },
        "05": {
            "name": "Health",
            "description": "Returns jurisdictional hierarchy for Health",
            "outputs": ["Sub Centre Code", "Sub Centre Name", "Primary Health Centre Code", 
                       "Primary Health Centre Name", "Taluk Code", "Taluk Name", 
                       "District Code", "District Name"]
        }
    }

def debug_jurisdiction_api():
    """
    Debug the jurisdiction API with various approaches
    """
    base_url = "https://kgis.ksrsac.in:9000/boundarywebservices/ws/getJurisdictionBoundary"
    
    print(f"\n{'='*60}")
    print("🔍 DEBUGGING JURISDICTION BOUNDARY API")
    print(f"{'='*60}")
    
    # Test 1: Try the exact URL from documentation
    print("🔍 Test 1: Using exact parameters from documentation")
    test_cases = [
        {
            'coordinates': '776312.8847,1438821.9517',
            'code': '01',
            'type': 'UTM'
        },
        {
            'coordinates': '16.208,75.739',
            'code': '01', 
            'type': 'DD'
        },
        # Try without type parameter (should give 400)
        {
            'coordinates': '776312.8847,1438821.9517',
            'code': '01'
        },
        # Try swapped coordinates (should give 202)
        {
            'coordinates': '1438821.9517,776312.8847',
            'code': '01',
            'type': 'UTM'
        }
    ]
    
    for i, params in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {params} ---")
        
        try:
            response = requests.get(base_url, params=params, verify=False, timeout=30)
            print(f"Status Code: {response.status_code}")
            print(f"Response Length: {len(response.text)}")
            print(f"Content Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.text:
                try:
                    data = response.json()
                    print(f"JSON Response: {json.dumps(data, indent=2)}")
                    
                    if data and len(data) > 0:
                        result = data[0]
                        msg = result.get('msg', 'N/A')
                        print(f"Message Code: {msg}")
                        
                        if msg == "200":
                            print("✅ SUCCESS - Found working parameters!")
                            return params
                        elif msg == "202":
                            print("⚠️ Coordinates out of Karnataka bounds")
                        elif msg == "400":
                            print("❌ Missing mandatory parameters")
                        elif msg == "401":
                            print("❌ Invalid layer code")
                        
                except json.JSONDecodeError as e:
                    print(f"JSON Parse Error: {e}")
                    print(f"Raw Response: {response.text}")
            else:
                print("❌ Empty response body")
                
        except Exception as e:
            print(f"Error: {e}")
    
    # Test 2: Try different coordinate formats
    print(f"\n🔍 Test 2: Trying different coordinate formats")
    
    coord_variations = [
        ('776312.8847,1438821.9517', 'UTM'),  # Original
        ('776312.8847, 1438821.9517', 'UTM'), # With space
        ('776312,1438821', 'UTM'),             # Rounded
        ('12.9716,77.5946', 'DD'),             # Bangalore center
        ('15.3173,75.7139', 'DD'),             # Different Karnataka location
        ('13.0827,80.2707', 'DD'),             # Chennai (should be out of bounds)
    ]
    
    for coords, coord_type in coord_variations:
        print(f"\nTesting coordinates: {coords} ({coord_type})")
        
        params = {
            'coordinates': coords,
            'code': '01',
            'type': coord_type
        }
        
        try:
            response = requests.get(base_url, params=params, verify=False, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    msg = data[0].get('msg', 'N/A')
                    print(f"  Result: {msg}")
                    
                    if msg == "200":
                        print(f"  ✅ WORKING COORDINATES FOUND!")
                        return params
                else:
                    print(f"  Empty response")
            else:
                print(f"  HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"  Error: {e}")
    
    print(f"\n❌ No working coordinates found in debugging tests")
    return None

def test_jurisdiction_boundary_api():
    """
    Test the KGIS Election Jurisdiction Hierarchy API with enhanced debugging
    """
    
    base_url = "https://kgis.ksrsac.in:9000/boundarywebservices/ws/getJurisdictionBoundary"
    
    print("=== KGIS Election Jurisdiction Hierarchy API Test ===")
    print(f"Service URL: {base_url}")
    print()
    
    # Display available layer codes
    layer_info = get_layer_info()
    print("Available Layer Codes:")
    for code, info in layer_info.items():
        print(f"  {code} - {info['name']}: {info['description']}")
    print()
    
    # Get input from user
    coordinates = input("Enter Coordinates (default: 776312.8847,1438821.9517): ").strip()
    if not coordinates:
        coordinates = "776312.8847,1438821.9517"
        print(f"Using default: {coordinates}")
    
    coord_type = input("Enter coordinate type DD or UTM (default: UTM): ").strip().upper()
    if not coord_type or coord_type not in ['DD', 'UTM']:
        coord_type = "UTM"
        print(f"Using default: {coord_type}")
    
    layer_code = input("Enter Layer Code 01-05 (default: 01): ").strip()
    if not layer_code:
        layer_code = "01"
        print(f"Using default: {layer_code}")
    
    print(f"\nTesting with parameters:")
    print(f"  Coordinates: {coordinates}")
    print(f"  Layer Code: {layer_code}")
    print(f"  Coordinate Type: {coord_type}")
    print()
    
    try:
        params = {
            'coordinates': coordinates,
            'code': layer_code,
            'type': coord_type
        }
        
        print(f"Request Parameters: {params}")
        print(f"Full URL: {base_url}?{requests.compat.urlencode(params)}")
        print()
        
        start_time = time.time()
        response = requests.get(base_url, params=params, verify=False, timeout=30)
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Time: {response_time} ms")
        print(f"Response Content Length: {len(response.text)}")
        print()
        
        if response.text:
            try:
                json_response = response.json()
                print("JSON Response:")
                print(json.dumps(json_response, indent=2))
                print()
                
                if isinstance(json_response, list) and len(json_response) > 0:
                    data = json_response[0]
                    msg = data.get('msg', 'N/A')
                    
                    print("=== Results Analysis ===")
                    print(f"Status Message: {msg}")
                    
                    if msg == "200":
                        print("✅ SUCCESS: Jurisdiction data retrieved!")
                        # Parse the data based on layer code
                        if layer_code == "01":
                            parse_election_data(data)
                        # ... other layer parsing functions
                    else:
                        print(f"❌ No data returned (Message: {msg})")
                        
                        if msg == "202":
                            print("Issue: Coordinates are out of Karnataka State boundary")
                        elif msg == "400":
                            print("Issue: Mandatory parameters are missing")
                        elif msg == "401":
                            print("Issue: Invalid layer code")
                            
                        print(f"\n🔧 Running debug tests to find working parameters...")
                        debug_jurisdiction_api()
                        
                else:
                    print("❌ Empty response array")
                    print(f"\n🔧 Running debug tests...")
                    debug_jurisdiction_api()
                    
            except json.JSONDecodeError as e:
                print(f"JSON Parse Error: {e}")
                print("Raw Response:")
                print(response.text)
        else:
            print("❌ Empty response body")
            print(f"\n🔧 Running debug tests...")
            debug_jurisdiction_api()
            
    except Exception as e:
        print(f"Request Error: {e}")

def parse_election_data(data):
    """Parse Election layer (01) response data"""
    print(f"\n🗳️ Election Jurisdiction Information:")
    print(f"  Polling Booth Number: {data.get('boothNumber', 'N/A')}")
    print(f"  Polling Booth Name: {data.get('boothName', 'N/A')}")
    print(f"  Assembly Constituency Number: {data.get('assemblyconstituencyNumber', 'N/A')}")
    print(f"  Assembly Constituency Name: {data.get('assemblyconstituencyName', 'N/A')}")
    print(f"  Parliament Constituency Number: {data.get('parliamentconstituencyNumber', 'N/A')}")
    print(f"  Parliament Constituency Name: {data.get('parliamentconstituencyName', 'N/A')}")

def parse_police_data(data):
    """Parse Police/Home layer (02) response data"""
    print(f"\n🚔 Police Jurisdiction Information:")
    print(f"  Police Station ID: {data.get('policeStationId', 'N/A')}")
    print(f"  Police Station Name: {data.get('policeStationName', 'N/A')}")
    print(f"  Circle ID: {data.get('circleId', 'N/A')}")
    print(f"  Circle Name: {data.get('circleName', 'N/A')}")
    print(f"  Sub Division ID: {data.get('subDivisionId', 'N/A')}")
    print(f"  Sub Division Name: {data.get('subDivisionName', 'N/A')}")
    print(f"  Division ID: {data.get('divisionId', 'N/A')}")
    print(f"  Division Name: {data.get('divisionName', 'N/A')}")

def parse_education_data(data):
    """Parse Education layer (03) response data"""
    print(f"\n🎓 Education Jurisdiction Information:")
    print(f"  Block Code: {data.get('blockCode', 'N/A')}")
    print(f"  Block Name: {data.get('blockName', 'N/A')}")
    print(f"  District Code: {data.get('districtCode', 'N/A')}")
    print(f"  District Name: {data.get('districtName', 'N/A')}")

def parse_bescom_data(data):
    """Parse Bescom layer (04) response data"""
    print(f"\n⚡ Bescom Jurisdiction Information:")
    print(f"  Section Code: {data.get('sectionCode', 'N/A')}")
    print(f"  Section Name: {data.get('sectionName', 'N/A')}")
    print(f"  Sub Division Code: {data.get('subDivisionCode', 'N/A')}")
    print(f"  Sub Division Name: {data.get('subDivisionName', 'N/A')}")
    print(f"  Division Code: {data.get('divisionCode', 'N/A')}")
    print(f"  Division Name: {data.get('divisionName', 'N/A')}")
    print(f"  Circle Code: {data.get('circleCode', 'N/A')}")
    print(f"  Circle Name: {data.get('circleName', 'N/A')}")
    print(f"  Zonal Code: {data.get('zonalCode', 'N/A')}")
    print(f"  Zonal Name: {data.get('zonalName', 'N/A')}")

def parse_health_data(data):
    """Parse Health layer (05) response data"""
    print(f"\n🏥 Health Jurisdiction Information:")
    print(f"  Sub Centre Code: {data.get('subCentreCode', 'N/A')}")
    print(f"  Sub Centre Name: {data.get('subCentreName', 'N/A')}")
    print(f"  Primary Health Centre Code: {data.get('primaryHealthCentreCode', 'N/A')}")
    print(f"  Primary Health Centre Name: {data.get('primaryHealthCentreName', 'N/A')}")
    print(f"  Taluk Code: {data.get('talukCode', 'N/A')}")
    print(f"  Taluk Name: {data.get('talukName', 'N/A')}")
    print(f"  District Code: {data.get('districtCode', 'N/A')}")
    print(f"  District Name: {data.get('districtName', 'N/A')}")

def test_multiple_layer_codes():
    """
    Test multiple layer codes with the same coordinates
    """
    print("\n" + "="*60)
    print("TESTING MULTIPLE LAYER CODES")
    print("="*60)
    
    base_url = "https://kgis.ksrsac.in:9000/boundarywebservices/ws/getJurisdictionBoundary"
    coordinates = "776312.8847,1438821.9517"  # Known working coordinates
    coord_type = "UTM"
    layer_info = get_layer_info()
    
    print(f"Testing all layer codes with coordinates: {coordinates}")
    print()
    
    for layer_code, info in layer_info.items():
        print(f"Testing Layer {layer_code} - {info['name']}:")
        
        try:
            params = {
                'coordinates': coordinates,
                'code': layer_code,
                'type': coord_type
            }
            
            response = requests.get(base_url, params=params, verify=False, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    result = data[0]
                    msg = result.get('msg', 'N/A')
                    
                    if msg == "200":
                        print(f"  ✅ Success: Data retrieved")
                        # Show first few fields as preview
                        fields_shown = 0
                        for key, value in result.items():
                            if key != 'msg' and value and fields_shown < 3:
                                print(f"    {key}: {value}")
                                fields_shown += 1
                        if fields_shown == 0:
                            print(f"    (No additional data fields)")
                    else:
                        print(f"  ❌ Status: {msg}")
                else:
                    print(f"  ❌ Empty response")
            else:
                print(f"  ❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()

def main():
    """
    Main function to run jurisdiction boundary API test
    """
    print("KGIS Election Jurisdiction Hierarchy API Test Suite")
    print("=" * 60)
    print("This service fetches jurisdiction hierarchy for given layer")
    print("and coordinates within Karnataka State.")
    print("=" * 60)
    
    try:
        # Test with user input
        test_jurisdiction_boundary_api()
        
        # Ask if user wants to see multiple layer tests
        print("\n" + "="*60)
        run_multiple = input("Would you like to test all layer codes? (y/n): ").strip().lower()
        
        if run_multiple in ['y', 'yes']:
            test_multiple_layer_codes()
        
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
    except Exception as e:
        print(f"Unexpected error in main: {e}")
    
    print("\n" + "="*60)
    print("Test completed!")
    print("="*60)

if __name__ == "__main__":
    main()
