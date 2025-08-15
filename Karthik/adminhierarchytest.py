#!/usr/bin/env python3
"""
KGIS Admin Hierarchy API Test Script
Tests the API endpoint: https://kgis.ksrsac.in:9000/genericwebservices/ws/kgisadminhierarchy
"""

import requests
import json
import time
from typing import Dict, Any, List
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class KGISAdminHierarchyTester:
    def __init__(self):
        self.base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/kgisadminhierarchy"
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing
        
    def test_api_with_department_code(self, dept_code: str) -> Dict[str, Any]:
        """
        Test the API with a specific department code using GET request
        """
        print(f"\n{'='*50}")
        print(f"Testing API with department code: {dept_code}")
        print(f"{'='*50}")
        
        try:
            # Test with GET request (only supported method)
            print("Testing GET request...")
            get_start_time = time.time()
            get_response = self.session.get(
                self.base_url,
                params={'deptcode': dept_code},
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
                'department_code': dept_code,
                'status_code': get_response.status_code,
                'data': get_response.text,
                'response_time': get_response_time
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return {'error': str(e), 'department_code': dept_code}
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return {'error': str(e), 'department_code': dept_code}

    def test_api_with_all_parameters(self, dept_code: str, app_code: str, type_param: str, code: str) -> Dict[str, Any]:
        """
        Test the API with all required parameters: Department Code, Application Code, Type, Code
        """
        print(f"\n{'='*50}")
        print(f"Testing API with all parameters:")
        print(f"  Department Code: {dept_code}")
        print(f"  Application Code: {app_code}")
        print(f"  Type: {type_param}")
        print(f"  Code: {code}")
        print(f"{'='*50}")
        
        try:
            # Test with all parameters
            print("Testing GET request with all parameters...")
            get_start_time = time.time()
            get_response = self.session.get(
                self.base_url,
                params={
                    'deptcode': dept_code,
                    'applncode': app_code,
                    'type': type_param,
                    'code': code
                },
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
                'department_code': dept_code,
                'application_code': app_code,
                'type': type_param,
                'code': code,
                'status_code': get_response.status_code,
                'data': get_response.text,
                'response_time': get_response_time
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return {'error': str(e), 'parameters': {'dept': dept_code, 'app': app_code, 'type': type_param, 'code': code}}
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return {'error': str(e), 'parameters': {'dept': dept_code, 'app': app_code, 'type': type_param, 'code': code}}
    
    def test_without_parameters(self) -> Dict[str, Any]:
        """
        Test the API without any parameters to see the default response
        """
        print(f"\n{'='*50}")
        print("Testing API without parameters")
        print(f"{'='*50}")
        
        try:
            start_time = time.time()
            response = self.session.get(self.base_url, timeout=30)
            end_time = time.time()
            response_time = end_time - start_time
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Time: {response_time:.3f} seconds")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.text:
                try:
                    data = response.json()
                    print(f"Response JSON: {json.dumps(data, indent=2)}")
                except json.JSONDecodeError:
                    print(f"Response Text: {response.text}")
                    
            return {
                'status_code': response.status_code,
                'data': response.text
            }
            
        except Exception as e:
            print(f"Error: {e}")
            return {'error': str(e)}
    
    def test_different_parameter_names(self, dept_code: str) -> None:
        """
        Test different parameter names to find the correct one
        """
        print(f"\n{'='*50}")
        print("Testing different parameter names")
        print(f"{'='*50}")
        
        param_names = [
            'departmentcode',
            'department_code', 
            'deptcode',
            'dept_code',
            'department',
            'departmentCode',
            'deptCode',
            'code',
            'dept',
            'DEPARTMENTCODE',
            'DEPARTMENT_CODE'
        ]
        
        for param_name in param_names:
            print(f"\nTesting parameter: {param_name}")
            try:
                response = self.session.get(
                    self.base_url,
                    params={param_name: dept_code},
                    timeout=10
                )
                print(f"  Status: {response.status_code}")
                if response.text and len(response.text) < 200:
                    print(f"  Response: {response.text}")
                elif response.text:
                    print(f"  Response (truncated): {response.text[:200]}...")
                    
            except Exception as e:
                print(f"  Error: {e}")

    def test_different_parameter_combinations(self) -> None:
        """
        Test different parameter name combinations to find the correct API format
        """
        print(f"\n{'='*50}")
        print("Testing different parameter name combinations")
        print(f"{'='*50}")
        
        # Common parameter name variations with your specific values
        param_combinations = [
            # Most likely correct names with your specific values
            {'departmentcode': '1'},
            {'department_code': '1'},
            {'deptcode': '1'},
            {'DEPARTMENTCODE': '1'},
            
            # Test with all your parameters using different naming conventions
            {'departmentcode': '1', 'applicationcode': '102', 'type': 'lgd', 'code': '602'},
            {'department_code': '1', 'application_code': '102', 'type': 'lgd', 'code': '602'},
            {'deptcode': '1', 'appcode': '102', 'type': 'lgd', 'code': '602'},
            {'dept_code': '1', 'app_code': '102', 'type': 'lgd', 'code': '602'},
            {'departmentCode': '1', 'applicationCode': '102', 'type': 'lgd', 'code': '602'},
            {'Department': '1', 'Application': '102', 'Type': 'lgd', 'Code': '602'},
            
            # Alternative parameter names
            {'dept': '1', 'app': '102', 'type': 'lgd', 'code': '602'},
            {'department': '1', 'application': '102', 'type': 'lgd', 'code': '602'},
        ]
        
        for i, params in enumerate(param_combinations, 1):
            print(f"\nTesting combination {i}: {params}")
            try:
                response = self.session.get(
                    self.base_url,
                    params=params,
                    timeout=10
                )
                print(f"  Status: {response.status_code}")
                if response.text and len(response.text) < 200:
                    print(f"  Response: {response.text}")
                elif response.text:
                    print(f"  Response (truncated): {response.text[:200]}...")
                    
            except Exception as e:
                print(f"  Error: {e}")
    
    def performance_test(self, dept_code: str, num_requests: int = 5) -> Dict[str, Any]:
        """
        Test API performance with multiple requests
        """
        print(f"\n{'='*50}")
        print(f"Performance test with {num_requests} requests")
        print(f"{'='*50}")
        
        response_times = []
        successful_requests = 0
        
        for i in range(num_requests):
            start_time = time.time()
            try:
                response = self.session.get(
                    self.base_url,
                    params={'deptcode': dept_code},
                    timeout=30
                )
                end_time = time.time()
                response_time = end_time - start_time
                response_times.append(response_time)
                
                if response.status_code == 200:
                    successful_requests += 1
                    
                print(f"Request {i+1}: {response.status_code} - {response_time:.2f}s")
                
            except Exception as e:
                print(f"Request {i+1}: Error - {e}")
                
            time.sleep(0.5)  # Small delay between requests
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
            
            print(f"\nPerformance Summary:")
            print(f"  Successful requests: {successful_requests}/{num_requests}")
            print(f"  Average response time: {avg_time:.2f}s")
            print(f"  Minimum response time: {min_time:.2f}s")
            print(f"  Maximum response time: {max_time:.2f}s")
            
            return {
                'total_requests': num_requests,
                'successful_requests': successful_requests,
                'avg_response_time': avg_time,
                'min_response_time': min_time,
                'max_response_time': max_time
            }
        
        return {'error': 'No successful requests completed'}

def main():
    """
    Main function to run a single test case with user-provided parameters
    """
    print("KGIS Admin Hierarchy API Test Suite - Interactive Test")
    print("=" * 60)
    
    tester = KGISAdminHierarchyTester()
    
    # Get user input for parameters
    print("Please provide the following parameters:")
    print()
    
    dept_code = input("Enter Department Code (e.g., 1): ").strip()
    if not dept_code:
        dept_code = "1"
        print(f"Using default: {dept_code}")
    
    app_code = input("Enter Application Code (e.g., 102): ").strip()
    if not app_code:
        app_code = "102"
        print(f"Using default: {app_code}")
    
    type_param = input("Enter Type (e.g., lgd): ").strip()
    if not type_param:
        type_param = "lgd"
        print(f"Using default: {type_param}")
    
    code = input("Enter Code (e.g., 604199): ").strip()
    if not code:
        code = "604199"
        print(f"Using default: {code}")
    
    print()
    print("Testing with your provided parameter values...")
    
    # Your provided test values
    test_params = {
        'dept_code': dept_code,
        'app_code': app_code,
        'type_param': type_param,
        'code': code
    }
    
    result = tester.test_api_with_all_parameters(
        test_params['dept_code'],
        test_params['app_code'], 
        test_params['type_param'],
        test_params['code']
    )
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    if 'error' not in result and result.get('status_code') == 200:
        print("✓ API test successful!")
        print("🎉 API is working correctly!")
        print(f"Parameters used: dept={test_params['dept_code']}, app={test_params['app_code']}, type={test_params['type_param']}, code={test_params['code']}")
        print("\n💡 Check the response data above for the API results")
    else:
        print("❌ API test failed")
        print(f"Status Code: {result.get('status_code', 'Unknown')}")
        print(f"Parameters tested: dept={test_params['dept_code']}, app={test_params['app_code']}, type={test_params['type_param']}, code={test_params['code']}")
        print("\n🔍 The API may require different parameter names or values")

if __name__ == "__main__":
    main()