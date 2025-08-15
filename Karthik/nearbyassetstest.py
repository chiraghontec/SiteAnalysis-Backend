#!/usr/bin/env python3
"""
KGIS Nearby Assets API Test Script
Tests the API endpoint: https://kgis.ksrsac.in:9000/NearbyAssets/ws/getNearbyAssetData

This service accepts:
- Coordinates (latitude, longitude)
- Layer Code (asset type identifier)
- Number (number of assets to return)
- Type (DD or UTM coordinate system)

Returns nearby assets with names, coordinates, distances, and addresses
"""

import requests
import json
import time
from typing import Dict, Any, List
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class KGISNearbyAssetsTester:
    def __init__(self):
        self.base_url = "https://kgis.ksrsac.in:9000/NearbyAssets/ws/getNearbyAssetData"
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        
    def test_api_with_parameters(self, 
                                coordinates: str, 
                                layer_code: str, 
                                number: int,
                                coord_type: str) -> Dict[str, Any]:
        """
        Test the Nearby Assets API with required parameters
        
        Args:
            coordinates: Coordinates in format "lat,lon" or "x,y"
            layer_code: Layer code for asset type (e.g., 1312130)
            number: Number of assets to return (e.g., 5)
            coord_type: DD (Decimal Degree) or UTM
        """
        print(f"\n{'='*60}")
        print(f"Testing KGIS Nearby Assets API")
        print(f"{'='*60}")
        print(f"Coordinates: {coordinates}")
        print(f"Layer Code: {layer_code}")
        print(f"Number of Assets: {number}")
        print(f"Coordinate Type: {coord_type}")
        print(f"API URL: {self.base_url}")
        print(f"{'='*60}")
        
        try:
            # Prepare parameters
            params = {
                'coordinates': coordinates,
                'code': layer_code,
                'number': number,
                'type': coord_type
            }
            
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
                        self._parse_assets_data(data, coord_type)
                    
                except json.JSONDecodeError:
                    print(f"\nResponse Text: {response.text}")
            
            return {
                'coordinates': coordinates,
                'layer_code': layer_code,
                'number': number,
                'coord_type': coord_type,
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

    def _parse_assets_data(self, data, coord_type):
        """
        Parse and display the nearby assets response data
        """
        print(f"\n{'='*50}")
        print("NEARBY ASSETS RESULTS")
        print(f"{'='*50}")
        
        if isinstance(data, list) and len(data) > 0:
            print(f"Found {len(data)} nearby asset(s):")
            
            for i, asset in enumerate(data, 1):
                if isinstance(asset, dict):
                    print(f"\n🏢 Asset {i}:")
                    print(f"  📍 Name: {asset.get('assetName', 'N/A')}")
                    print(f"  📏 Distance: {asset.get('distance', 'N/A')} meters")
                    
                    # Coordinates
                    x_coord = asset.get('x', 'N/A')
                    y_coord = asset.get('y', 'N/A')
                    if coord_type == 'DD':
                        print(f"  🌍 Location: Lat {y_coord}, Lon {x_coord}")
                    else:
                        print(f"  🗺️  UTM Coordinates: X {x_coord}, Y {y_coord}")
                    
                    # Address and type
                    address = asset.get('address', '').strip()
                    if address:
                        print(f"  🏠 Address: {address}")
                    else:
                        print(f"  🏠 Address: Not available")
                    
                    asset_type = asset.get('asseType', '').strip()
                    if asset_type:
                        print(f"  🏷️  Type: {asset_type}")
                    else:
                        print(f"  🏷️  Type: Not specified")
                    
                    # Message/Status
                    msg = asset.get('msg', '')
                    if msg == '200':
                        print(f"  ✅ Status: Success")
                    else:
                        print(f"  ℹ️  Message: {msg}")
                else:
                    print(f"Unexpected asset data format: {asset}")
            
            # Summary statistics
            print(f"\n{'='*30}")
            print("SUMMARY STATISTICS")
            print(f"{'='*30}")
            
            distances = [float(asset.get('distance', 0)) for asset in data if isinstance(asset, dict) and asset.get('distance')]
            if distances:
                print(f"📊 Total Assets Found: {len(data)}")
                print(f"📏 Closest Asset: {min(distances):.2f} meters")
                print(f"📏 Farthest Asset: {max(distances):.2f} meters")
                print(f"📏 Average Distance: {sum(distances)/len(distances):.2f} meters")
            
            # Count assets with addresses
            assets_with_address = [asset for asset in data if isinstance(asset, dict) and asset.get('address', '').strip()]
            print(f"🏠 Assets with Address: {len(assets_with_address)}/{len(data)}")
            
        elif isinstance(data, dict):
            # Single asset response
            msg = data.get('msg', '')
            if msg == '204':
                print("ℹ️  No assets found for the given coordinates and layer code")
            elif msg == '400':
                print("❌ Bad request - mandatory parameters are missing")
            else:
                print(f"Single Asset Response: {data}")
        else:
            print("❌ No valid assets data found in response")

def main():
    """
    Main function to run nearby assets API test with user input
    """
    print("KGIS Nearby Assets API Test Suite")
    print("=" * 60)
    print("This service finds nearby assets for given coordinates")
    print("and layer code (asset type)")
    print("=" * 60)
    
    tester = KGISNearbyAssetsTester()
    
    print("\nEnter the required parameters:")
    print("(Examples from documentation)")
    print()
    
    try:
        # Get coordinates
        print("Coordinate Examples:")
        print("  DD format: 16.208,75.739")
        print("  UTM format: 777774.04,1448858.96")
        coordinates = input("Enter Coordinates: ").strip()
        if not coordinates:
            coordinates = "777774.04,1448858.96"
            print(f"Using default: {coordinates}")
        
        # Get coordinate type first
        print("\nCoordinate System Options:")
        print("  DD  - Latitude and Longitude in Decimal degree")
        print("  UTM - UTM zone 43, North Coordinates in Meters (Y, X)")
        coord_type = input("Enter coordinate type (DD or UTM): ").strip().upper()
        if not coord_type or coord_type not in ['DD', 'UTM']:
            coord_type = "UTM"
            print(f"Using default: {coord_type}")
        
        # Get layer code
        print("\nLayer Code Examples:")
        print("  1312130 - Schools/Educational institutions")
        print("  (Different codes represent different asset types)")
        layer_code = input("Enter Layer Code (e.g., 1312130): ").strip()
        if not layer_code:
            layer_code = "1312130"
            print(f"Using default: {layer_code}")
        
        # Get number of assets
        number_input = input("Enter Number of assets to return (e.g., 5): ").strip()
        try:
            number = int(number_input) if number_input else 5
        except ValueError:
            number = 5
            print(f"Using default: {number}")
        
        print(f"\nTesting with parameters:")
        print(f"Coordinates: {coordinates}")
        print(f"Layer Code: {layer_code}")
        print(f"Number: {number}")
        print(f"Type: {coord_type}")
        
        # Test with user provided parameters
        result = tester.test_api_with_parameters(coordinates, layer_code, number, coord_type)
            
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
        return
    except Exception as e:
        print(f"Input error: {e}")
        result = {'error': str(e)}
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    if 'error' not in result and result.get('status_code') == 200:
        print(f"✅ Nearby Assets API test successful!")
        print(f"   Coordinates: {result.get('coordinates', 'N/A')}")
        print(f"   Layer Code: {result.get('layer_code', 'N/A')}")
        print(f"   Response Time: {result.get('response_time', 0):.3f} seconds")
        print("🎉 API is working correctly!")
    else:
        print(f"❌ Nearby Assets API test failed")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        else:
            status_code = result.get('status_code', 'Unknown')
            print(f"   Status Code: {status_code}")
            
            if status_code == 400:
                print("   Issue: Mandatory parameters are missing")
            elif status_code == 204:
                print("   Issue: No content for the given layer code/coordinates")
        
        print(f"\n🔍 Troubleshooting suggestions:")
        print("1. Check if coordinates are in the correct format")
        print("2. Verify the layer code is valid for the area")
        print("3. Try different coordinates within Karnataka")
        print("4. Ensure coordinate type (DD/UTM) matches coordinate format")
        print("5. Check if the API service is currently available")

if __name__ == "__main__":
    main()