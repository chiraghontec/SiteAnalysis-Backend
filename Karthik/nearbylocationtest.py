#!/usr/bin/env python3
"""
KGIS Nearby Location Details API Test Script
Tests the API endpoint: https://kgis.ksrsac.in:9000/genericwebservices/ws/getlocationdetails

This service provides administrative hierarchy for any point within Karnataka:
- Urban areas: Ward, Zone, Town, District information
- Rural areas: Village, Hobli, Taluk, District, Survey numbers

Parameters:
- coordinates: Latitude,Longitude (DD) or X,Y (UTM)
- type: DD (Decimal Degree) or UTM
- aoi: Area of Interest (optional) - d/t/h/w or combinations
"""

import requests
import json
import time
import urllib3
from typing import Dict, Any, Optional

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class KGISLocationDetailsTester:
    def __init__(self):
        self.base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/getlocationdetails"
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        
    def test_api_with_parameters(self, 
                                coordinates: str, 
                                coord_type: str,
                                aoi: Optional[str] = None) -> Dict[str, Any]:
        """
        Test the Location Details API with required parameters
        
        Args:
            coordinates: Coordinates in format "lat,lon" or "x,y"
            coord_type: DD (Decimal Degree) or UTM
            aoi: Area of Interest (optional) - d/t/h/w or combinations
        """
        print(f"\n{'='*60}")
        print(f"Testing KGIS Location Details API")
        print(f"{'='*60}")
        print(f"Coordinates: {coordinates}")
        print(f"Coordinate Type: {coord_type}")
        print(f"Area of Interest: {aoi if aoi else 'Complete hierarchy (default)'}")
        print(f"API URL: {self.base_url}")
        print(f"{'='*60}")
        
        try:
            # Prepare parameters
            params = {
                'coordinates': coordinates,
                'type': coord_type
            }
            
            # Add optional AOI parameter if provided
            if aoi:
                params['aoi'] = aoi
            
            print(f"Request Parameters: {params}")
            
            # Make API call
            start_time = time.time()
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=30
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"\nResponse Status Code: {response.status_code}")
            print(f"Response Time: {response_time:.3f} seconds")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.text:
                try:
                    data = response.json()
                    print(f"\nJSON Response:")
                    print(json.dumps(data, indent=2))
                    
                    if response.status_code == 200:
                        self._parse_location_data(data)
                    
                except json.JSONDecodeError:
                    print(f"\nResponse Text: {response.text}")
            
            return {
                'coordinates': coordinates,
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

    def _parse_location_data(self, data):
        """
        Parse and display the location details response data
        """
        print(f"\n{'='*50}")
        print("LOCATION DETAILS RESULTS")
        print(f"{'='*50}")
        
        if isinstance(data, list) and len(data) > 0:
            location_info = data[0]
            
            if isinstance(location_info, dict):
                message = location_info.get('message', '')
                location_type = location_info.get('type', '')
                
                print(f"📍 Location Type: {location_type}")
                print(f"📊 Status Message: {message}")
                
                if message.startswith('200'):
                    print(f"✅ Success: Location data retrieved!")
                    
                    if location_type == 'Urban':
                        self._parse_urban_data(location_info)
                    elif location_type == 'Rural':
                        self._parse_rural_data(location_info)
                    else:
                        print("ℹ️  Location type not specified")
                        
                elif message.startswith('204'):
                    print(f"⚠️ {message}")
                    if 'outside urban boundary' in message:
                        print("   The coordinates are in a rural area, not urban")
                    
                elif message.startswith('202'):
                    print(f"❌ Coordinates out of Karnataka State boundary")
                    
                elif message.startswith('400'):
                    print(f"❌ Mandatory parameters are missing")
                    
                elif message.startswith('401'):
                    print(f"❌ Invalid parameter code")
                    
                else:
                    print(f"ℹ️ Unexpected message: {message}")
                    
            else:
                print("❌ Unexpected response format")
        else:
            print("❌ No location data found in response")

    def _parse_urban_data(self, data):
        """
        Parse and display urban area data
        """
        print(f"\n🏙️ URBAN AREA DETAILS")
        print(f"{'='*30}")
        
        # District information
        district_code = data.get('districtCode', 'N/A')
        district_name = data.get('districtName', 'N/A')
        print(f"🏛️  District: {district_name} (Code: {district_code})")
        
        # Town information
        town_code = data.get('townCode', 'N/A')
        town_name = data.get('townName', 'N/A')
        print(f"🏘️  Town: {town_name} (Code: {town_code})")
        
        # Zone information
        zone_code = data.get('zoneCode', 'N/A')
        zone_name = data.get('zoneName', 'N/A')
        print(f"🗺️  Zone: {zone_name} (Code: {zone_code})")
        
        # Ward information
        ward_code = data.get('wardCode', 'N/A')
        ward_name = data.get('wardName', 'N/A')
        lgd_ward_code = data.get('LGD_WardCode', 'N/A')
        print(f"🏠 Ward: {ward_name} (Code: {ward_code})")
        print(f"🆔 LGD Ward Code: {lgd_ward_code}")

    def _parse_rural_data(self, data):
        """
        Parse and display rural area data
        """
        print(f"\n🌾 RURAL AREA DETAILS")
        print(f"{'='*30}")
        
        # District information
        district_code = data.get('districtCode', 'N/A')
        district_name = data.get('districtName', 'N/A')
        print(f"🏛️  District: {district_name} (Code: {district_code})")
        
        # Taluk information
        taluk_code = data.get('talukCode', 'N/A')
        taluk_name = data.get('talukName', 'N/A')
        print(f"🏘️  Taluk: {taluk_name} (Code: {taluk_code})")
        
        # Hobli information
        hobli_code = data.get('hobliCode', 'N/A')
        hobli_name = data.get('hobliName', 'N/A')
        print(f"🗺️  Hobli: {hobli_name} (Code: {hobli_code})")
        
        # Village information
        village_code = data.get('villageCode', 'N/A')
        village_name = data.get('villageName', 'N/A')
        lgd_village_code = data.get('LGD_VillageCode', 'N/A')
        print(f"🏡 Village: {village_name} (Code: {village_code})")
        print(f"🆔 LGD Village Code: {lgd_village_code}")
        
        # Survey number
        survey_num = data.get('surveynum', 'N/A')
        print(f"📋 Survey Number: {survey_num}")

    def test_multiple_locations(self):
        """
        Test with multiple sample locations from documentation
        """
        print(f"\n{'='*60}")
        print("TESTING MULTIPLE SAMPLE LOCATIONS")
        print(f"{'='*60}")
        
        # Test cases from documentation
        test_cases = [
            {
                'name': 'Urban Area (DD) - Bangalore',
                'coordinates': '13.0743352,77.557323',
                'type': 'DD',
                'aoi': None
            },
            {
                'name': 'Urban Area (UTM) - Bangalore',
                'coordinates': '777774.04,1448858.96', 
                'type': 'UTM',
                'aoi': None
            },
            {
                'name': 'Rural Area (UTM) - Vijayapura',
                'coordinates': '546739.9227999998,1853272.6735999994',
                'type': 'UTM',
                'aoi': None
            },
            {
                'name': 'Urban Ward Only (UTM)',
                'coordinates': '777774.04,1448858.96',
                'type': 'UTM', 
                'aoi': 'w'
            },
            {
                'name': 'Rural Ward Query (should give 204)',
                'coordinates': '546739.9227999998,1853272.6735999994',
                'type': 'UTM',
                'aoi': 'w'
            }
        ]
        
        successful_tests = 0
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{'='*40}")
            print(f"Test {i}: {test_case['name']}")
            print(f"{'='*40}")
            
            try:
                result = self.test_api_with_parameters(
                    test_case['coordinates'],
                    test_case['type'],
                    test_case.get('aoi')
                )
                
                if 'error' not in result and result.get('status_code') == 200:
                    successful_tests += 1
                    print(f"✅ Test {i}: SUCCESS")
                else:
                    print(f"❌ Test {i}: FAILED")
                    
            except Exception as e:
                print(f"❌ Test {i}: ERROR - {e}")
        
        print(f"\n{'='*50}")
        print(f"MULTIPLE LOCATION TEST SUMMARY")
        print(f"{'='*50}")
        print(f"✅ Successful: {successful_tests}/{len(test_cases)}")
        print(f"❌ Failed: {len(test_cases) - successful_tests}/{len(test_cases)}")

def main():
    """
    Main function to run location details API test with user input
    """
    print("KGIS Nearby Location Details API Test Suite")
    print("=" * 60)
    print("This service provides administrative hierarchy for any")
    print("point within Karnataka (Urban/Rural classification)")
    print("=" * 60)
    
    tester = KGISLocationDetailsTester()
    
    print("\nEnter the required parameters:")
    print("(Examples from documentation)")
    print()
    
    try:
        # Get coordinates
        print("Coordinate Examples:")
        print("  Urban DD: 13.0743352,77.557323 (Bangalore)")
        print("  Urban UTM: 777774.04,1448858.96 (Bangalore)")
        print("  Rural UTM: 546739.9227999998,1853272.6735999994 (Vijayapura)")
        coordinates = input("Enter Coordinates: ").strip()
        if not coordinates:
            coordinates = "13.0743352,77.557323"
            print(f"Using default: {coordinates}")
        
        # Get coordinate type
        print("\nCoordinate System Options:")
        print("  DD  - Latitude and Longitude in Decimal degree")
        print("  UTM - UTM zone 43, North Coordinates in Meters (Y, X)")
        coord_type = input("Enter coordinate type (DD or UTM): ").strip().upper()
        if not coord_type or coord_type not in ['DD', 'UTM']:
            coord_type = "DD"
            print(f"Using default: {coord_type}")
        
        # Get Area of Interest (optional)
        print("\nArea of Interest (AOI) Options (optional):")
        print("  d - District only")
        print("  t - Taluk only") 
        print("  h - Hobli only")
        print("  w - Ward only (for urban areas)")
        print("  Combinations: d,t or t,h etc.")
        print("  Leave empty for complete hierarchy")
        aoi = input("Enter AOI (optional): ").strip()
        if not aoi:
            aoi = None
            print("Using default: Complete hierarchy")
            
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
        return
    except Exception as e:
        print(f"Input error: {e}")
        print("Using default values...")
        coordinates = "13.0743352,77.557323"
        coord_type = "DD"
        aoi = None
    
    print(f"\nTesting with parameters:")
    print(f"Coordinates: {coordinates}")
    print(f"Type: {coord_type}")
    print(f"AOI: {aoi if aoi else 'Complete hierarchy'}")
    
    # Test with user provided parameters
    result = tester.test_api_with_parameters(coordinates, coord_type, aoi)
    
    # Ask if user wants to run sample tests
    print(f"\n{'='*60}")
    try:
        run_samples = input("Would you like to test multiple sample locations? (y/n): ").strip().lower()
        if run_samples in ['y', 'yes']:
            tester.test_multiple_locations()
    except KeyboardInterrupt:
        print("\nSkipping sample tests.")
    except:
        pass
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    if 'error' not in result and result.get('status_code') == 200:
        print(f"✅ Location Details API test successful!")
        print(f"   Coordinates: {result['coordinates']}")
        print(f"   Coordinate Type: {result['coord_type']}")
        print(f"   AOI: {result['aoi'] if result['aoi'] else 'Complete hierarchy'}")
        print(f"   Response Time: {result.get('response_time', 0):.3f} seconds")
        print("🎉 API is working correctly!")
    else:
        print(f"❌ Location Details API test failed")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        
        print("\n🔍 Troubleshooting suggestions:")
        print("1. Check if coordinates are in the correct format")
        print("2. Verify coordinates are within Karnataka state")
        print("3. Ensure coordinate type (DD/UTM) matches coordinate format")
        print("4. Try coordinates from documentation examples")
        print("5. Check if AOI parameter is valid (d/t/h/w)")

if __name__ == "__main__":
    main()