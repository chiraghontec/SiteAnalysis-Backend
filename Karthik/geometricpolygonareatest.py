import requests
import urllib3
import time
import json

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def debug_geometric_polygon_api():
    """
    Debug the Geometric Polygon Area API with various approaches
    """
    base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/geomForSurveyNum"
    
    print("=== DEBUGGING GEOMETRIC POLYGON AREA API ===")
    print(f"Base URL: {base_url}")
    print()
    
    # Test 1: Try the exact URL from documentation
    print("🔍 Test 1: Using exact parameters from documentation")
    test_urls = [
        f"{base_url}/1/1/DD",
        f"{base_url}/1/1/UTM"
    ]
    
    for test_url in test_urls:
        print(f"\nTesting URL: {test_url}")
        try:
            response = requests.get(test_url, verify=False, timeout=30)
            print(f"Status Code: {response.status_code}")
            print(f"Response Length: {len(response.text)}")
            print(f"Content Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.text:
                if response.text.strip():
                    try:
                        json_data = response.json()
                        print(f"JSON Response: {json.dumps(json_data, indent=2)}")
                    except:
                        print(f"Raw Response: {response.text}")
                else:
                    print("⚠️ Empty response body")
            else:
                print("⚠️ No response content")
                
        except Exception as e:
            print(f"Error: {e}")
    
    # Test 2: Try different parameter combinations
    print(f"\n🔍 Test 2: Trying different parameter combinations")
    
    test_combinations = [
        ("1", "1", "DD"),
        ("1", "2", "DD"), 
        ("2", "1", "DD"),
        ("1", "1", "UTM"),
        ("10", "5", "DD"),
        ("100", "10", "DD")
    ]
    
    for village_id, survey_num, coord_type in test_combinations:
        test_url = f"{base_url}/{village_id}/{survey_num}/{coord_type}"
        print(f"\nTesting: Village={village_id}, Survey={survey_num}, Type={coord_type}")
        
        try:
            response = requests.get(test_url, verify=False, timeout=10)
            print(f"  Status: {response.status_code}, Length: {len(response.text)}")
            
            if response.text and len(response.text) > 10:
                print(f"  ✅ Got response data!")
                try:
                    json_data = response.json()
                    if json_data and len(json_data) > 0:
                        print(f"  Found {len(json_data)} polygon(s)")
                        break  # Found working combination
                except:
                    pass
            else:
                print(f"  ❌ Empty or minimal response")
                
        except Exception as e:
            print(f"  Error: {e}")
    
    # Test 3: Check if the API expects query parameters instead
    print(f"\n🔍 Test 3: Testing with query parameters")
    
    params_test_url = base_url
    test_params = [
        {'villageid': '1', 'surveynumber': '1', 'type': 'DD'},
        {'village_id': '1', 'survey_number': '1', 'type': 'DD'},
        {'villageId': '1', 'surveyNumber': '1', 'type': 'DD'},
        {'kgis_village_id': '1', 'survey_no': '1', 'coordinate_type': 'DD'}
    ]
    
    for params in test_params:
        print(f"\nTesting with query params: {params}")
        try:
            response = requests.get(params_test_url, params=params, verify=False, timeout=10)
            print(f"  Status: {response.status_code}, Length: {len(response.text)}")
            
            if response.text and len(response.text) > 10:
                print(f"  ✅ Got response with query params!")
                try:
                    json_data = response.json()
                    print(f"  Response: {json.dumps(json_data, indent=2)}")
                except:
                    print(f"  Raw response: {response.text}")
                break
                
        except Exception as e:
            print(f"  Error: {e}")

def test_geometric_polygon_area_api():
    """
    Original test function with enhanced debugging
    """
    base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/geomForSurveyNum"
    
    print("=== KGIS Geometric Polygon Area API Test ===")
    print(f"Service URL: {base_url}")
    print()
    
    # Get input parameters from user
    village_id = input("Enter K-GIS Village ID (e.g., 1): ").strip()
    if not village_id:
        village_id = "1"
        print(f"Using default: {village_id}")
    
    survey_number = input("Enter Survey Number (e.g., 1): ").strip()
    if not survey_number:
        survey_number = "1"
        print(f"Using default: {survey_number}")
    
    print("\nCoordinate System Options:")
    print("  DD  - Latitude and Longitude in Decimal degree")
    print("  UTM - UTM zone 43, North Coordinates in Meters (Y, X)")
    coord_type = input("Enter coordinate type (DD or UTM): ").strip().upper()
    if not coord_type or coord_type not in ['DD', 'UTM']:
        coord_type = "DD"
        print(f"Using default: {coord_type}")
    
    # Construct the URL with path parameters
    test_url = f"{base_url}/{village_id}/{survey_number}/{coord_type}"
    
    print(f"\nTesting with parameters:")
    print(f"  K-GIS Village ID: {village_id}")
    print(f"  Survey Number: {survey_number}")
    print(f"  Coordinate Type: {coord_type}")
    print(f"  Full URL: {test_url}")
    print()
    
    try:
        # Record start time
        start_time = time.time()
        
        # Make the API request
        response = requests.get(test_url, verify=False, timeout=30)
        
        # Record end time
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Time: {response_time} ms")
        print(f"Response Content Length: {len(response.text)}")
        print(f"Response Headers: {dict(response.headers)}")
        print()
        
        # Debug the response
        if not response.text or len(response.text) == 0:
            print("❌ EMPTY RESPONSE DETECTED!")
            print("\n🔧 Running debug tests to find working parameters...")
            debug_geometric_polygon_api()
            return
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                print("JSON Response:")
                print(json.dumps(json_response, indent=2))
                print()
                
                # Parse and display the data
                if isinstance(json_response, list) and len(json_response) > 0:
                    print("=== Parsed Polygon Information ===")
                    
                    for i, polygon_data in enumerate(json_response, 1):
                        message = polygon_data.get('message', 'N/A')
                        geom = polygon_data.get('geom', 'N/A')
                        
                        print(f"Polygon {i}:")
                        print(f"  Message: {message}")
                        
                        if message == "200":
                            print(f"  ✓ Status: Data available")
                            if geom and geom != 'N/A':
                                # Extract coordinate count from polygon
                                if geom.startswith('POLYGON'):
                                    coord_count = geom.count(',') + 1
                                    print(f"  Geometry Type: POLYGON")
                                    print(f"  Coordinate Points: {coord_count}")
                                    print(f"  Coordinate System: {coord_type}")
                                    print(f"  Geometry: {geom[:100]}..." if len(geom) > 100 else f"  Geometry: {geom}")
                                else:
                                    print(f"  Geometry: {geom}")
                        elif message == "204":
                            print(f"  ⚠ Status: No data available for given survey number and village ID")
                        else:
                            print(f"  Status: {message}")
                        print()
                    
                    # Overall test result
                    success_count = sum(1 for item in json_response if item.get('message') == "200")
                    if success_count > 0:
                        print(f"✓ Test Result: SUCCESS - Found {success_count} polygon(s) for the survey number!")
                    else:
                        print("⚠ Test Result: WARNING - No polygons found for the given parameters!")
                        
                else:
                    print("⚠ Test Result: WARNING - Empty or invalid response format!")
                    
            except ValueError as e:
                print(f"Error parsing JSON response: {e}")
                print("Raw Response Text:")
                print(response.text)
        else:
            print(f"Error: HTTP {response.status_code}")
            print("Response Text:")
            print(response.text)
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # First try the normal test
    test_geometric_polygon_area_api()
