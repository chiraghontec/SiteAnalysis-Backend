import requests
import urllib3
import time

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_hobli_code_api():
    """
    Test the KGIS Hobli Code API
    Service URL: https://kgis.ksrsac.in:9000/genericwebservices/ws/hoblicode
    Method: GET
    Parameters: hobliname
    """
    
    base_url = "https://kgis.ksrsac.in:9000/genericwebservices/ws/hoblicode"
    
    print("=== KGIS Hobli Code API Test ===")
    print(f"Service URL: {base_url}")
    print()
    
    # Get hobli name from user
    hobli_name = input("Enter Hobli Name (e.g., KULAGERI, UTTARAHALLI -4): ").strip()
    
    if not hobli_name:
        print("Error: Hobli name is required!")
        return
    
    # Prepare parameters
    params = {
        'hobliname': hobli_name
    }
    
    print(f"\nTesting with parameters:")
    print(f"  hobliname: {hobli_name}")
    print()
    
    try:
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
                print(json_response)
                print()
                
                # Parse and display the data
                if isinstance(json_response, list) and len(json_response) > 0:
                    data = json_response[0]
                    print("=== Parsed Hobli Information ===")
                    print(f"District Name: {data.get('districtName', 'N/A')}")
                    print(f"District Code: {data.get('districtCode', 'N/A')}")
                    print(f"Taluk Name: {data.get('talukName', 'N/A')}")
                    print(f"Taluk Code: {data.get('talukCode', 'N/A')}")
                    print(f"Hobli Name: {data.get('hobliName', 'N/A')}")
                    print(f"Hobli Code: {data.get('hobliCode', 'N/A')}")
                    print(f"Message: {data.get('message', 'N/A')}")
                    
                    if data.get('hobliCode'):
                        print("\n✓ Test Result: SUCCESS - Hobli code retrieved successfully!")
                    else:
                        print("\n⚠ Test Result: WARNING - No hobli code found in response!")
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

if __name__ == "__main__":
    test_hobli_code_api()
