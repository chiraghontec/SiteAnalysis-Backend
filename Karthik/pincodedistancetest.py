#!/usr/bin/env python3
"""
KGIS Distance Between PIN Codes API Test Script
Tests the API endpoint: https://kgis.ksrsac.in:9000/genericwebservices/ws/getDistanceBtwPincode

This service calculates the distance in meters between two 6-digit PIN codes
within Karnataka State.

Parameters:
- pincodes: Two 6-digit PIN codes separated by comma (e.g., 560097,560091)

Response:
- keymsg: 200 (success) or 401 (invalid PIN code)
- distance: Distance in meters (only on success)
"""

import requests
import json
import time
import urllib3
from typing import Dict, Any

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_pincode_distance_api():
    """
    Test the KGIS Distance Between PIN Codes API
    Service URL: https://kgis.ksrsac.in:9000/genericwebservices/ws/getDistanceBtwPincode
    Method: GET
    Parameters: pincodes (comma-separated 6-digit PIN codes)
    """
    
    base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/getDistanceBtwPincode"
    
    print("=== KGIS Distance Between PIN Codes API Test ===")
    print(f"Service URL: {base_url}")
    print()
    
    # Get PIN codes from user
    print("Enter two 6-digit PIN codes within Karnataka State:")
    print("Examples:")
    print("  560079, 560091 (Bangalore areas)")
    print("  560097, 560091 (Bangalore areas)")
    print("  570001, 571201 (Mysore areas)")
    print()
    
    pincode1 = input("Enter first PIN code (6 digits): ").strip()
    pincode2 = input("Enter second PIN code (6 digits): ").strip()
    
    # Validate PIN codes
    if not pincode1 or not pincode2:
        print("Error: Both PIN codes are required!")
        return
    
    # Remove any spaces and validate format
    pincode1 = pincode1.replace(" ", "")
    pincode2 = pincode2.replace(" ", "")
    
    if not (pincode1.isdigit() and len(pincode1) == 6):
        print(f"Error: First PIN code '{pincode1}' must be exactly 6 digits!")
        return
    
    if not (pincode2.isdigit() and len(pincode2) == 6):
        print(f"Error: Second PIN code '{pincode2}' must be exactly 6 digits!")
        return
    
    # Prepare parameter (comma-separated PIN codes)
    pincodes_param = f"{pincode1},{pincode2}"
    
    print(f"\nTesting with parameters:")
    print(f"  PIN Codes: {pincodes_param}")
    print(f"  First PIN: {pincode1}")
    print(f"  Second PIN: {pincode2}")
    print()
    
    try:
        # Prepare parameters
        params = {
            'pincodes': pincodes_param
        }
        
        print(f"Request URL: {base_url}")
        print(f"Request Parameters: {params}")
        print()
        
        # Record start time
        start_time = time.time()
        
        # Make the API request
        response = requests.get(base_url, params=params, verify=False, timeout=30)
        
        # Record end time
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Time: {response_time} ms")
        print(f"Response Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            try:
                # Try to parse JSON response
                json_response = response.json()
                print("JSON Response:")
                print(json.dumps(json_response, indent=2))
                print()
                
                # Parse and display the data
                if isinstance(json_response, list) and len(json_response) > 0:
                    data = json_response[0]
                    
                    print("=== Distance Calculation Results ===")
                    
                    keymsg = data.get('keymsg', 'N/A')
                    print(f"Status Code: {keymsg}")
                    
                    if keymsg == "200":
                        distance = data.get('distance', 'N/A')
                        print(f"✅ Success: Distance calculated successfully!")
                        print(f"Distance: {distance} meters")
                        
                        # Convert to other units for better understanding
                        if distance != 'N/A':
                            try:
                                distance_float = float(distance)
                                distance_km = distance_float / 1000
                                print(f"Distance: {distance_km:.3f} kilometers")
                                
                                # Provide context
                                if distance_float < 1000:
                                    print(f"📏 Very close locations (less than 1 km apart)")
                                elif distance_float < 5000:
                                    print(f"📏 Nearby locations (within 5 km)")
                                elif distance_float < 25000:
                                    print(f"📏 Same city/district range (within 25 km)")
                                else:
                                    print(f"📏 Different cities/regions (more than 25 km apart)")
                                    
                            except ValueError:
                                print(f"⚠ Warning: Could not convert distance to number")
                                
                    elif keymsg == "401":
                        print(f"❌ Error: Invalid PIN code(s)")
                        print(f"One or both PIN codes are not valid or not within Karnataka State")
                        print(f"Please check:")
                        print(f"  • PIN codes are exactly 6 digits")
                        print(f"  • PIN codes belong to Karnataka State")
                        print(f"  • PIN codes are currently active/valid")
                        
                    else:
                        print(f"⚠ Unexpected status code: {keymsg}")
                        
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
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def test_multiple_pincode_combinations():
    """
    Test multiple PIN code combinations to demonstrate different scenarios
    """
    print("\n" + "="*60)
    print("TESTING MULTIPLE PIN CODE COMBINATIONS")
    print("="*60)
    
    base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/getDistanceBtwPincode"
    
    # Test cases: (pincode1, pincode2, description)
    test_cases = [
        ("560079", "560091", "Bangalore areas (from documentation)"),
        ("560097", "560091", "Bangalore areas (from documentation)"),
        ("560001", "560002", "Close Bangalore PIN codes"),
        ("570001", "571201", "Mysore area PIN codes"),
        ("560001", "570001", "Bangalore to Mysore"),
        ("560079", "123456", "Valid Karnataka + Invalid PIN"),
        ("000000", "111111", "Invalid PIN codes"),
    ]
    
    print("Testing various PIN code combinations:")
    print()
    
    for i, (pin1, pin2, description) in enumerate(test_cases, 1):
        print(f"Test {i}: {description}")
        print(f"PIN Codes: {pin1}, {pin2}")
        
        try:
            params = {'pincodes': f"{pin1},{pin2}"}
            response = requests.get(base_url, params=params, verify=False, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    result = data[0]
                    keymsg = result.get('keymsg', 'N/A')
                    
                    if keymsg == "200":
                        distance = result.get('distance', 'N/A')
                        print(f"  ✅ Success: {distance} meters")
                    elif keymsg == "401":
                        print(f"  ❌ Invalid PIN code(s)")
                    else:
                        print(f"  ⚠ Unexpected response: {keymsg}")
                else:
                    print(f"  ❌ Empty response")
            else:
                print(f"  ❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()

def main():
    """
    Main function to run PIN code distance API test
    """
    print("KGIS Distance Between PIN Codes API Test Suite")
    print("=" * 60)
    print("This service calculates the distance between two PIN codes")
    print("within Karnataka State in meters.")
    print("=" * 60)
    
    try:
        # Test with user input
        test_pincode_distance_api()
        
        # Ask if user wants to see multiple test cases
        print("\n" + "="*60)
        run_multiple = input("Would you like to run multiple test cases? (y/n): ").strip().lower()
        
        if run_multiple in ['y', 'yes']:
            test_multiple_pincode_combinations()
        
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
    except Exception as e:
        print(f"Unexpected error in main: {e}")
    
    print("\n" + "="*60)
    print("Test completed!")
    print("="*60)

if __name__ == "__main__":
    main()
