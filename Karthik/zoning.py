#!/usr/bin/env python3
"""
KGIS Zonation Data API Test Script
Tests the API endpoint: https://kgis.ksrsac.in:9000/genericwebservices/ws/getKGISAdminCodes2

This service fetches K-GIS Zonation codes and administrative hierarchy including:
- GPS coordinates and location type (Urban/Rural)
- Zone, Town, Ward information
- District, Taluk, Hobli codes and names
- Assembly Constituency (AC) and Polling Station (PS) details
- Booth codes

Method: POST
Parameters: JSON payload with ID, Gps_Lat, Gps_Lon
"""

import requests
import json
import time
import urllib3
from typing import Dict, Any, List

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class KGISZonationTester:
    def __init__(self):
        self.base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/getKGISAdminCodes2"
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        
    def test_api_with_coordinates(self, coordinates_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Test the Zonation Data API with coordinate payload
        
        Args:
            coordinates_list: List of dictionaries with ID, Gps_Lat, Gps_Lon
        """
        print(f"\n{'='*60}")
        print(f"Testing KGIS Zonation Data API")
        print(f"{'='*60}")
        print(f"API URL: {self.base_url}")
        print(f"Method: POST")
        print(f"Number of Coordinates: {len(coordinates_list)}")
        print(f"{'='*60}")
        
        try:
            # Prepare JSON payload
            payload = coordinates_list
            
            print(f"Request Payload:")
            print(json.dumps(payload, indent=2))
            print()
            
            # Make API call
            start_time = time.time()
            response = self.session.post(
                self.base_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Time: {response_time:.3f} seconds")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.text:
                try:
                    data = response.json()
                    print(f"\nJSON Response:")
                    print(json.dumps(data, indent=2))
                    
                    if response.status_code == 200:
                        self._parse_zonation_data(data)
                    
                except json.JSONDecodeError:
                    print(f"\nResponse Text: {response.text}")
            
            return {
                'coordinates_count': len(coordinates_list),
                'status_code': response.status_code,
                'data': response.text,
                'response_time': response_time
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return {'error': str(e), 'coordinates_count': len(coordinates_list)}
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return {'error': str(e), 'coordinates_count': len(coordinates_list)}

    def _parse_zonation_data(self, data):
        """
        Parse and display the zonation response data
        """
        print(f"\n{'='*50}")
        print("ZONATION DATA RESULTS")
        print(f"{'='*50}")
        
        if isinstance(data, dict):
            status = data.get('status', False)
            status_code = data.get('statusCode', 'N/A')
            count = data.get('count', 0)
            data_list = data.get('dataList', [])
            
            print(f"📊 Status: {status}")
            print(f"🔢 Status Code: {status_code}")
            print(f"📍 Records Found: {count}")
            
            if status_code == 200 and status:
                print(f"✅ Success: Zonation data retrieved!")
                
                if data_list and len(data_list) > 0:
                    print(f"\n{'='*40}")
                    print("DETAILED ZONATION INFORMATION")
                    print(f"{'='*40}")
                    
                    for i, location in enumerate(data_list, 1):
                        self._display_location_details(i, location)
                        
                    # Summary statistics
                    self._display_summary_statistics(data_list)
                else:
                    print("ℹ️  No location data found in response")
                    
            elif status_code == 500:
                print("❌ Internal server error")
            elif status_code == 101:
                print("❌ Invalid start date")
            elif status_code == 102:
                print("❌ Invalid end date")
            else:
                print(f"⚠️ Unexpected status code: {status_code}")
        else:
            print("❌ Unexpected response format")

    def _display_location_details(self, index: int, location: Dict[str, Any]):
        """
        Display detailed information for a single location
        """
        print(f"\n📍 Location {index}:")
        print(f"{'='*25}")
        
        # Basic location info
        location_id = location.get('ID', 'N/A')
        gps_lat = location.get('Gps_Lat', 'N/A')
        gps_lon = location.get('Gps_Lon', 'N/A')
        location_type = location.get('Type', 'N/A')
        
        print(f"🆔 ID: {location_id}")
        print(f"🌍 GPS Coordinates: {gps_lat}, {gps_lon}")
        print(f"🏙️ Location Type: {location_type}")
        
        # Administrative hierarchy
        print(f"\n🏛️ Administrative Hierarchy:")
        district_code = location.get('KGISDistrictCode', 'N/A')
        district_name = location.get('KGISDistrictName', 'N/A')
        print(f"   District: {district_name} (Code: {district_code})")
        
        taluk_code = location.get('KGISTalukCode', 'N/A')
        taluk_name = location.get('KGISTalukName', 'N/A')
        print(f"   Taluk: {taluk_name} (Code: {taluk_code})")
        
        hobli_code = location.get('KGISHobliCode', 'N/A')
        hobli_name = location.get('KGISHobliName', 'N/A')
        print(f"   Hobli: {hobli_name} (Code: {hobli_code})")
        
        # Urban-specific information
        if location_type == 'Urban':
            print(f"\n🏘️ Urban Information:")
            town_code = location.get('KGISTownCode', 'N/A')
            town_name = location.get('KGISTownName', 'N/A')
            print(f"   Town: {town_name} (Code: {town_code})")
            
            zone_code = location.get('KGISZoneCode', 'N/A')
            zone_name = location.get('KGISZoneName', 'N/A')
            print(f"   Zone: {zone_name} (Code: {zone_code})")
            
            ward_code = location.get('KGISWardCode', 'N/A')
            ward_name = location.get('KGISWardName', 'N/A')
            print(f"   Ward: {ward_name} (Code: {ward_code})")
        
        # Election information
        print(f"\n🗳️ Election Information:")
        ac_code = location.get('AC_CODE', 'N/A')
        ac_name = location.get('AC_Name', 'N/A')
        print(f"   Assembly Constituency: {ac_name} (Code: {ac_code})")
        
        ps_code = location.get('PS_Code', 'N/A')
        ps_name = location.get('PS_Name', 'N/A')
        print(f"   Polling Station: {ps_name} (Code: {ps_code})")
        
        booth_code = location.get('BoothCode', 'N/A')
        print(f"   Booth Code: {booth_code}")

    def _display_summary_statistics(self, data_list: List[Dict[str, Any]]):
        """
        Display summary statistics for the zonation data
        """
        print(f"\n{'='*40}")
        print("SUMMARY STATISTICS")
        print(f"{'='*40}")
        
        # Count location types
        urban_count = sum(1 for loc in data_list if loc.get('Type') == 'Urban')
        rural_count = sum(1 for loc in data_list if loc.get('Type') == 'Rural')
        
        print(f"📊 Total Locations: {len(data_list)}")
        print(f"🏙️ Urban Locations: {urban_count}")
        print(f"🌾 Rural Locations: {rural_count}")
        
        # Count unique districts
        districts = set(loc.get('KGISDistrictName', '') for loc in data_list if loc.get('KGISDistrictName'))
        print(f"🏛️ Unique Districts: {len(districts)}")
        if districts:
            print(f"   Districts: {', '.join(districts)}")
        
        # Count unique assembly constituencies
        constituencies = set(loc.get('AC_Name', '') for loc in data_list if loc.get('AC_Name'))
        print(f"🗳️ Unique Assembly Constituencies: {len(constituencies)}")

    def test_sample_coordinates(self):
        """
        Test with sample coordinates from documentation
        """
        print(f"\n{'='*60}")
        print("TESTING WITH SAMPLE COORDINATES")
        print(f"{'='*60}")
        
        # Sample coordinates from documentation
        sample_coordinates = [
            {
                "ID": 198,
                "Gps_Lat": 13.03063015,
                "Gps_Lon": 77.61886905
            },
            {
                "ID": 200,
                "Gps_Lat": 13.03138907,
                "Gps_Lon": 77.61987634
            }
        ]
        
        print("Testing with documentation sample coordinates...")
        result = self.test_api_with_coordinates(sample_coordinates)
        return result

    def test_multiple_bangalore_locations(self):
        """
        Test with multiple Bangalore locations
        """
        print(f"\n{'='*60}")
        print("TESTING WITH MULTIPLE BANGALORE LOCATIONS")
        print(f"{'='*60}")
        
        bangalore_locations = [
            {
                "ID": 1,
                "Gps_Lat": 12.9716,  # Bangalore center
                "Gps_Lon": 77.5946
            },
            {
                "ID": 2,
                "Gps_Lat": 13.0827,  # North Bangalore
                "Gps_Lon": 77.5877
            },
            {
                "ID": 3,
                "Gps_Lat": 12.8597,  # South Bangalore
                "Gps_Lon": 77.6414
            },
            {
                "ID": 4,
                "Gps_Lat": 12.9698,  # East Bangalore
                "Gps_Lon": 77.7499
            },
            {
                "ID": 5,
                "Gps_Lat": 12.9541,  # West Bangalore
                "Gps_Lon": 77.4905
            }
        ]
        
        print("Testing with multiple Bangalore locations...")
        result = self.test_api_with_coordinates(bangalore_locations)
        return result

def main():
    """
    Main function to run zonation data API test with user input
    """
    print("KGIS Zonation Data API Test Suite")
    print("=" * 60)
    print("This service fetches K-GIS Zonation codes and")
    print("administrative hierarchy for given coordinates")
    print("=" * 60)
    
    tester = KGISZonationTester()
    
    print("\nChoose test mode:")
    print("1. Test with documentation sample coordinates")
    print("2. Test with multiple Bangalore locations") 
    print("3. Enter custom coordinates")
    print()
    
    try:
        choice = input("Enter choice (1-3) or press Enter for option 1: ").strip()
        if not choice:
            choice = "1"
        
        if choice == "1":
            print("\n🧪 Testing with documentation sample coordinates...")
            result = tester.test_sample_coordinates()
            
        elif choice == "2":
            print("\n🧪 Testing with multiple Bangalore locations...")
            result = tester.test_multiple_bangalore_locations()
            
        elif choice == "3":
            print("\n📍 Enter custom coordinates:")
            coordinates_list = []
            
            num_coords = input("How many coordinate pairs to test (default: 2)? ").strip()
            try:
                num_coords = int(num_coords) if num_coords else 2
            except ValueError:
                num_coords = 2
                print(f"Using default: {num_coords}")
            
            for i in range(num_coords):
                print(f"\nCoordinate {i+1}:")
                lat = input(f"  Enter Latitude (e.g., 13.03063015): ").strip()
                lon = input(f"  Enter Longitude (e.g., 77.61886905): ").strip()
                
                try:
                    lat_val = float(lat) if lat else 13.03063015
                    lon_val = float(lon) if lon else 77.61886905
                    
                    coordinates_list.append({
                        "ID": i + 1,
                        "Gps_Lat": lat_val,
                        "Gps_Lon": lon_val
                    })
                    
                except ValueError:
                    print(f"Invalid coordinates, using defaults...")
                    coordinates_list.append({
                        "ID": i + 1,
                        "Gps_Lat": 13.03063015,
                        "Gps_Lon": 77.61886905
                    })
            
            result = tester.test_api_with_coordinates(coordinates_list)
            
        else:
            print("Invalid choice, using option 1...")
            result = tester.test_sample_coordinates()
            
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
        return
    except Exception as e:
        print(f"Input error: {e}")
        print("Using default sample coordinates...")
        result = tester.test_sample_coordinates()
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    if 'error' not in result and result.get('status_code') == 200:
        print(f"✅ Zonation Data API test successful!")
        print(f"   Coordinates Tested: {result['coordinates_count']}")
        print(f"   Response Time: {result.get('response_time', 0):.3f} seconds")
        print("🎉 API is working correctly!")
    else:
        print(f"❌ Zonation Data API test failed")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        else:
            status_code = result.get('status_code', 'Unknown')
            print(f"   Status Code: {status_code}")
        
        print("\n🔍 Troubleshooting suggestions:")
        print("1. Check if coordinates are valid decimal degrees")
        print("2. Verify coordinates are within Karnataka state")
        print("3. Ensure JSON payload format is correct")
        print("4. Check if the API service is currently available")
        print("5. Try with the documentation sample coordinates")

if __name__ == "__main__":
    main()