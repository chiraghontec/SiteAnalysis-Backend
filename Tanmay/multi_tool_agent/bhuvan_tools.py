"""
Additional tools for the Site Analysis Backend Agent.
These tools provide specific functionality for interacting with the Bhuvan APIs
and performing advanced geospatial analysis.
"""

import json
from typing import Optional

def validate_coordinates(latitude: float, longitude: float):
    """Validates if coordinates are within valid ranges and Indian boundaries.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        
    Returns:
        dict: Validation result with recommendations
    """
    # Basic coordinate validation
    if not (-90 <= latitude <= 90):
        return {
            "valid": False,
            "error": "Invalid latitude. Must be between -90 and 90 degrees.",
            "type": "coordinate_error"
        }
    
    if not (-180 <= longitude <= 180):
        return {
            "valid": False,
            "error": "Invalid longitude. Must be between -180 and 180 degrees.",
            "type": "coordinate_error"
        }
    
    # India boundary validation (approximate)
    india_bounds = {
        "lat_min": 6.0,   # Southernmost point
        "lat_max": 37.5,  # Northernmost point 
        "lng_min": 68.0,  # Westernmost point
        "lng_max": 97.5   # Easternmost point
    }
    
    within_india = (
        india_bounds["lat_min"] <= latitude <= india_bounds["lat_max"] and
        india_bounds["lng_min"] <= longitude <= india_bounds["lng_max"]
    )
    
    result = {
        "valid": True,
        "within_india": within_india,
        "coordinates": {"lat": latitude, "lng": longitude}
    }
    
    if within_india:
        result["recommendation"] = "Coordinates are within India. All Bhuvan APIs are applicable."
        result["suggested_apis"] = ["geoid", "village_reverse_geocoding", "postal_hospital"]
    else:
        result["recommendation"] = "Coordinates are outside India. Bhuvan APIs may not provide data."
        result["warning"] = "Bhuvan APIs are optimized for Indian geographical data only."
    
    return result

def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float):
    """Calculates the approximate distance between two coordinates using Haversine formula.
    
    Args:
        lat1 (float): Latitude of first coordinate
        lng1 (float): Longitude of first coordinate
        lat2 (float): Latitude of second coordinate
        lng2 (float): Longitude of second coordinate
        
    Returns:
        dict: Distance calculation results
    """
    import math
    
    lon1, lon2 = lng1, lng2
    
    # Validate coordinates
    validation1 = validate_coordinates(lat1, lng1)
    validation2 = validate_coordinates(lat2, lng2)
    
    if not validation1["valid"] or not validation2["valid"]:
        return {
            "error": "Invalid coordinates provided",
            "validation_errors": [validation1, validation2]
        }
    
    # Haversine formula
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lon/2) * math.sin(delta_lon/2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance_km = R * c
    
    # Check if routing API is likely to work
    same_region = distance_km < 500  # Approximate same-state distance
    
    return {
        "distance_km": round(distance_km, 2),
        "distance_miles": round(distance_km * 0.621371, 2),
        "coordinates": {
            "from": {"lat": lat1, "lng": lng1},
            "to": {"lat": lat2, "lng": lng2}
        },
        "routing_api_suitable": same_region,
        "note": "Routing API works best for coordinates within the same state" if not same_region else "Distance suitable for routing API"
    }

def generate_api_request_template(api_name: str, latitude: Optional[float] = None, longitude: Optional[float] = None):
    """Generates ready-to-use request templates for Bhuvan APIs.
    
    Args:
        api_name (str): Name of the API
        latitude (Optional[float]): Latitude to use in template (default: Mumbai)
        longitude (Optional[float]): Longitude to use in template (default: Mumbai)
        
    Returns:
        dict: Request template with examples
    """
    # Default coordinates (Mumbai) if none provided
    if latitude is None or longitude is None:
        default_coords = {"lat": 19.0760, "lng": 72.8777}
    else:
        default_coords = {"lat": latitude, "lng": longitude}
    
    templates = {
        "postal_hospital": {
            "endpoint": "POST /api/postal-hospital",
            "request_body": {
                "lat": default_coords["lat"],
                "lng": default_coords["lng"],
                "buffer": 3000,
                "theme": "all"
            },
            "curl_example": f"""curl -X POST http://localhost:5000/api/postal-hospital \\
  -H "Content-Type: application/json" \\
  -d '{{"lat": {default_coords["lat"]}, "lng": {default_coords["lng"]}, "buffer": 3000, "theme": "all"}}'""",
            "description": "Find postal codes and hospitals within 3km radius"
        },
        
        "routing": {
            "endpoint": "POST /api/routing", 
            "request_body": {
                "origin": {"lat": default_coords["lat"], "lng": default_coords["lng"]},
                "destination": {"lat": default_coords["lat"] + 0.1, "lng": default_coords["lng"] + 0.1}
            },
            "curl_example": f"""curl -X POST http://localhost:5000/api/routing \\
  -H "Content-Type: application/json" \\
  -d '{{"origin": {{"lat": {default_coords["lat"]}, "lng": {default_coords["lng"]}}}, "destination": {{"lat": {default_coords["lat"] + 0.1}, "lng": {default_coords["lng"] + 0.1}}}}}'""",
            "description": "Get route between two points",
            "note": "Ensure both coordinates are within the same state"
        },
        
        "geoid": {
            "endpoint": "POST /api/geoid",
            "request_body": {
                "coordinates": {"lat": default_coords["lat"], "lng": default_coords["lng"]}
            },
            "curl_example": f"""curl -X POST http://localhost:5000/api/geoid \\
  -H "Content-Type: application/json" \\
  -d '{{"coordinates": {{"lat": {default_coords["lat"]}, "lng": {default_coords["lng"]}}}}}'""",
            "description": "Get administrative boundary codes"
        },
        
        "village_geocoding": {
            "endpoint": "POST /api/village-geocoding",
            "request_body": {
                "village": "Andheri",
                "state": "Maharashtra"
            },
            "curl_example": """curl -X POST http://localhost:5000/api/village-geocoding \\
  -H "Content-Type: application/json" \\
  -d '{"village": "Andheri", "state": "Maharashtra"}'""",
            "description": "Convert village name to coordinates"
        },
        
        "village_reverse_geocoding": {
            "endpoint": "POST /api/village-reverse-geocoding",
            "request_body": {
                "lat": default_coords["lat"],
                "lng": default_coords["lng"]
            },
            "curl_example": f"""curl -X POST http://localhost:5000/api/village-reverse-geocoding \\
  -H "Content-Type: application/json" \\
  -d '{{"lat": {default_coords["lat"]}, "lng": {default_coords["lng"]}}}'""",
            "description": "Get village information from coordinates"
        },
        
        "lulc_aoi": {
            "endpoint": "POST /api/lulc-aoi",
            "request_body": {
                "polygon": [
                    [default_coords["lng"], default_coords["lat"]],
                    [default_coords["lng"] + 0.01, default_coords["lat"]],
                    [default_coords["lng"] + 0.01, default_coords["lat"] + 0.01],
                    [default_coords["lng"], default_coords["lat"] + 0.01],
                    [default_coords["lng"], default_coords["lat"]]
                ],
                "year": 2022
            },
            "curl_example": f"""curl -X POST http://localhost:5000/api/lulc-aoi \\
  -H "Content-Type: application/json" \\
  -d '{{"polygon": [[{default_coords["lng"]}, {default_coords["lat"]}], [{default_coords["lng"] + 0.01}, {default_coords["lat"]}], [{default_coords["lng"] + 0.01}, {default_coords["lat"] + 0.01}], [{default_coords["lng"]}, {default_coords["lat"] + 0.01}], [{default_coords["lng"]}, {default_coords["lat"]}]], "year": 2022}}'""",
            "description": "Analyze land use/land cover for a polygon area"
        },
        
        "thematic_statistics": {
            "endpoint": "POST /api/thematic-stats",
            "request_body": {
                "district": "Mumbai",
                "year": 2022
            },
            "curl_example": """curl -X POST http://localhost:5000/api/thematic-stats \\
  -H "Content-Type: application/json" \\
  -d '{"district": "Mumbai", "year": 2022}'""",
            "description": "Get district-wise land use statistics"
        }
    }
    
    if api_name.lower() in templates:
        return {
            "status": "success",
            "api": api_name,
            "template": templates[api_name.lower()]
        }
    else:
        available_apis = list(templates.keys())
        return {
            "status": "error",
            "error_message": f"Template not available for '{api_name}'. Available APIs: {', '.join(available_apis)}",
            "available_apis": available_apis
        }

def analyze_api_performance():
    """Provides detailed performance analysis of all Bhuvan APIs.
    
    Returns:
        dict: Comprehensive performance data and recommendations
    """
    performance_data = {
        "last_updated": "2024-08-15",
        "total_tests": 32,
        "overall_success_rate": "100%",
        "average_response_time": "0.546s",
        
        "api_performance": {
            "geoid": {
                "avg_response_time": "0.254s",
                "success_rate": "100%",
                "reliability": "Excellent",
                "best_for": "Quick administrative boundary lookup",
                "peak_usage_tip": "Use this API first for context setting"
            },
            "postal_hospital": {
                "avg_response_time": "0.507s",
                "success_rate": "100%", 
                "reliability": "Excellent",
                "best_for": "Finding nearby facilities",
                "peak_usage_tip": "Adjust buffer distance based on urban/rural areas"
            },
            "village_geocoding": {
                "avg_response_time": "0.509s",
                "success_rate": "100%",
                "reliability": "Excellent", 
                "best_for": "Converting addresses to coordinates",
                "peak_usage_tip": "Use exact village and state names for best results"
            },
            "village_reverse_geocoding": {
                "avg_response_time": "0.513s",
                "success_rate": "100%",
                "reliability": "Excellent",
                "best_for": "Location identification from coordinates",
                "peak_usage_tip": "Combine with geoid API for complete context"
            },
            "lulc_aoi_statistics": {
                "avg_response_time": "0.582s",
                "success_rate": "100%",
                "reliability": "Excellent",
                "best_for": "Environmental analysis of specific areas",
                "peak_usage_tip": "Use smaller polygons for faster response"
            },
            "thematic_statistics": {
                "avg_response_time": "0.773s",
                "success_rate": "100%",
                "reliability": "Excellent",
                "best_for": "District-level planning and analysis",
                "peak_usage_tip": "Cache results for frequently accessed districts"
            },
            "routing": {
                "avg_response_time": "2.602s",
                "success_rate": "100%",
                "reliability": "Excellent",
                "best_for": "Navigation and route planning",
                "peak_usage_tip": "Ensure coordinates are within same state",
                "note": "Slower due to complex route calculation"
            }
        },
        
        "optimization_recommendations": [
            "Use geoid API first for quick context establishment",
            "Cache thematic statistics for frequently accessed districts", 
            "Validate coordinates before routing API calls",
            "Use appropriate buffer distances for postal_hospital API",
            "Combine APIs for comprehensive analysis workflows"
        ],
        
        "performance_tiers": {
            "fastest": ["geoid"],
            "fast": ["postal_hospital", "village_geocoding", "village_reverse_geocoding"],
            "moderate": ["lulc_aoi_statistics", "thematic_statistics"],
            "slower_but_complex": ["routing"]
        }
    }
    
    return {
        "status": "success",
        "performance_analysis": performance_data
    }

def get_error_troubleshooting_guide():
    """Provides comprehensive error troubleshooting guide for Bhuvan APIs.
    
    Returns:
        dict: Common errors and solutions
    """
    troubleshooting_guide = {
        "common_errors": {
            "coordinate_validation": {
                "error": "Invalid coordinates",
                "causes": [
                    "Coordinates outside valid range (-90 to 90 for lat, -180 to 180 for lng)",
                    "Coordinates outside India boundaries",
                    "Swapped latitude and longitude values"
                ],
                "solutions": [
                    "Validate coordinates using validate_coordinates tool",
                    "Ensure lat/lng are not swapped",
                    "Check coordinates are within India (6-37.5°N, 68-97.5°E)"
                ]
            },
            
            "routing_api_issues": {
                "error": "Routing failed or no route found",
                "causes": [
                    "Coordinates in different states",
                    "Very long distances (>500km)",
                    "Coordinates in water bodies or restricted areas"
                ],
                "solutions": [
                    "Ensure both coordinates are within same state",
                    "Use calculate_distance tool to check feasibility",
                    "Verify coordinates are on road network"
                ]
            },
            
            "api_token_errors": {
                "error": "Authentication failed",
                "causes": [
                    "Missing or invalid API tokens",
                    "Expired tokens",
                    "Incorrect token configuration"
                ],
                "solutions": [
                    "Check .env file configuration",
                    "Validate tokens using validate_tokens.py",
                    "Contact NRSC for token renewal"
                ]
            },
            
            "data_format_errors": {
                "error": "Invalid request format",
                "causes": [
                    "Incorrect JSON structure",
                    "Missing required fields",
                    "Wrong data types"
                ],
                "solutions": [
                    "Use generate_api_request_template tool",
                    "Follow exact API documentation",
                    "Validate JSON before sending requests"
                ]
            },
            
            "timeout_errors": {
                "error": "Request timeout",
                "causes": [
                    "Network connectivity issues",
                    "Server overload",
                    "Large polygon areas for LULC analysis"
                ],
                "solutions": [
                    "Retry with exponential backoff",
                    "Reduce polygon size for LULC APIs",
                    "Check network connectivity"
                ]
            }
        },
        
        "debugging_steps": [
            "1. Validate coordinates using validation tools",
            "2. Check API token configuration",
            "3. Verify request format using templates",
            "4. Test with known working coordinates",
            "5. Check network connectivity",
            "6. Review API-specific limitations"
        ],
        
        "testing_coordinates": {
            "mumbai": {"lat": 19.0760, "lng": 72.8777},
            "delhi": {"lat": 28.6139, "lng": 77.2090},
            "bangalore": {"lat": 12.9716, "lng": 77.5946},
            "chennai": {"lat": 13.0827, "lng": 80.2707}
        },
        
        "api_specific_notes": {
            "routing": "Requires coordinates within same state",
            "village_geocoding": "Use exact village and state names",
            "lulc_aoi": "Smaller polygons process faster",
            "postal_hospital": "Adjust buffer based on area type (urban/rural)"
        }
    }
    
    return {
        "status": "success",
        "troubleshooting_guide": troubleshooting_guide
    }
