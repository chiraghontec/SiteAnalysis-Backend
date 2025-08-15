#!/usr/bin/env python3
"""
KGIS Taluk Code API Test Script
Tests the API endpoint: https://kgis.ksrsac.in:9000/genericwebservices/ws/talukcode

This service accepts:
- Taluk Name (e.g., Bangalore-South)

Returns KGIS District Code, District Name, Taluk Code, and Taluk Name
"""

import requests
import json
import time
from typing import Dict, Any, Optional
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class KGISTalukCodeTester:
    def __init__(self):
        self.base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/talukcode"
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        
    def test_api_with_taluk_name(self, taluk_name: str) -> Dict[str, Any]:
        """
        Test the Taluk Code API with taluk name parameter
        
        Args:
            taluk_name: Name of the taluk (e.g., "Bangalore-South")
        """
        print(f"\n{'='*60}")
        print(f"Testing KGIS Taluk Code API")
        print(f"{'='*60}")
        print(f"Taluk Name: {taluk_name}")
        print(f"API URL: {self.base_url}")
        print(f"{'='*60}")
        
        try:
            # Prepare parameters
            params = {'talukname': taluk_name}
            
            print(f"Making API call with parameters: {params}")
            
            # Make API call
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
                    
                    if response.status_code == 200:
                        self._parse_taluk_data(data)
                    
                except json.JSONDecodeError:
                    print(f"\nResponse Text: {response.text}")
            
            return {
                'taluk_name': taluk_name,
                'status_code': response.status_code,
                'data': response.text,
                'response_time': response_time
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return {'error': str(e), 'taluk_name': taluk_name}
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return {'error': str(e), 'taluk_name': taluk_name}

    def _parse_taluk_data(self, data):
        """
        Parse and display the taluk code response data
        """
        print(f"\n{'='*50}")
        print("TALUK CODE API RESULTS")
        print(f"{'='*50}")
        
        if isinstance(data, list) and len(data) > 0:
            for i, item in enumerate(data, 1):
                if isinstance(item, dict):
                    print(f"\nResult {i}:")
                    print(f"  🏛️  District Name: {item.get('districtName', 'N/A')}")
                    print(f"  🔢 District Code: {item.get('districtCode', 'N/A')}")
                    print(f"  🏘️  Taluk Name: {item.get('talukName', 'N/A')}")
                    print(f"  🔢 Taluk Code: {item.get('talukCode', 'N/A')}")
                    
                    message = item.get('message', '')
                    if message:
                        if 'available' in message.lower():
                            print(f"  ✅ Status: {message}")
                        else:
                            print(f"  ℹ️  Message: {message}")
                else:
                    print(f"Unexpected data format: {item}")
        
        elif isinstance(data, dict):
            print(f"  🏛️  District Name: {data.get('districtName', 'N/A')}")
            print(f"  🔢 District Code: {data.get('districtCode', 'N/A')}")
            print(f"  🏘️  Taluk Name: {data.get('talukName', 'N/A')}")
            print(f"  🔢 Taluk Code: {data.get('talukCode', 'N/A')}")
            
            message = data.get('message', '')
            if message:
                if 'available' in message.lower():
                    print(f"  ✅ Status: {message}")
                else:
                    print(f"  ℹ️  Message: {message}")
        else:
            print("No valid taluk data found in response")

    def test_sample_taluk_names(self):
        """
        Test with multiple sample taluk names for comprehensive testing
        """
        print(f"\n{'='*60}")
        print("TESTING MULTIPLE TALUK NAMES")
        print(f"{'='*60}")
        
        # Sample taluk names from different districts in Karnataka
        sample_taluks = [
            "Bangalore-South",     # Bengaluru Urban
            "Mysore",             # Mysuru
            "Hubli",              # Dharwad
            "Mangalore",          # Dakshina Kannada
            "Belgaum",            # Belagavi
            "Shimoga",            # Shivamogga
            "Tumkur",             # Tumakuru
            "Gulbarga",           # Kalaburagi
            "Bijapur",            # Vijayapura
            "Bellary"             # Ballari
        ]
        
        successful_tests = []
        failed_tests = []
        
        for taluk in sample_taluks:
            print(f"\n--- Testing: {taluk} ---")
            try:
                result = self.test_api_with_taluk_name(taluk)
                
                if 'error' not in result and result.get('status_code') == 200:
                    successful_tests.append(taluk)
                    print(f"✅ {taluk}: SUCCESS")
                else:
                    failed_tests.append(taluk)
                    print(f"❌ {taluk}: FAILED")
                    
            except Exception as e:
                failed_tests.append(taluk)
                print(f"❌ {taluk}: ERROR - {e}")
        
        # Summary
        print(f"\n{'='*60}")
        print("SAMPLE TESTING SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Successful: {len(successful_tests)}/{len(sample_taluks)}")
        print(f"❌ Failed: {len(failed_tests)}/{len(sample_taluks)}")
        
        if successful_tests:
            print(f"\nWorking Taluks: {', '.join(successful_tests)}")
        
        if failed_tests:
            print(f"\nFailed Taluks: {', '.join(failed_tests)}")

def main():
    """
    Main function to run taluk code API test with user input
    """
    print("KGIS Taluk Code API Test Suite")
    print("=" * 60)
    print("This service fetches District and Taluk codes/names")
    print("for a given Taluk Name")
    print("=" * 60)
    
    tester = KGISTalukCodeTester()
    
    # Get user input for taluk name
    print("\nEnter the Taluk Name to lookup:")
    print("(Examples: Bangalore-South, Mysore, Hubli, Mangalore)")
    print()
    
    try:
        # Get taluk name
        taluk_input = input("Enter Taluk Name (e.g., Bangalore-South): ").strip()
        if not taluk_input:
            taluk_input = "Bangalore-South"
            print(f"Using default: {taluk_input}")
            
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
        return
    except Exception as e:
        print(f"Input error: {e}")
        print("Using default value...")
        taluk_input = "Bangalore-South"
    
    print(f"\nTesting with Taluk Name: '{taluk_input}'")
    
    # Test with user provided taluk name
    result = tester.test_api_with_taluk_name(taluk_input)
    
    # Ask if user wants to run sample tests
    print(f"\n{'='*60}")
    try:
        run_samples = input("Would you like to test multiple sample taluk names? (y/n): ").strip().lower()
        if run_samples in ['y', 'yes']:
            tester.test_sample_taluk_names()
    except KeyboardInterrupt:
        print("\nSkipping sample tests.")
    except:
        pass
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    if 'error' not in result and result.get('status_code') == 200:
        print(f"✅ Taluk Code API test successful!")
        print(f"   Taluk: '{result['taluk_name']}'")
        print(f"   Response Time: {result.get('response_time', 0):.3f} seconds")
        print("🎉 API is working correctly!")
    else:
        print(f"❌ Taluk Code API test failed")
        print(f"   Taluk: '{result.get('taluk_name', 'Unknown')}'")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        print("\n🔍 Troubleshooting suggestions:")
        print("1. Check if the taluk name is spelled correctly")
        print("2. Try using exact capitalization (e.g., 'Bangalore-South')")
        print("3. Check if the taluk exists in Karnataka state")
        print("4. Verify the API service is currently available")

if __name__ == "__main__":
    main()