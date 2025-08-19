"""
Enhanced Site Analysis Backend Agent with comprehensive Bhuvan API tools.
This agent provides expert assistance for geospatial analysis using 7 integrated Bhuvan APIs.
"""

import datetime
import json
from google.adk.agents import Agent

# Import additional tools
try:
    # Try relative import first (when used as a package)
    from .bhuvan_tools import (
        validate_coordinates,
        calculate_distance, 
        generate_api_request_template,
        analyze_api_performance,
        get_error_troubleshooting_guide
    )
except ImportError:
    # Fallback to absolute import (when running directly)
    from bhuvan_tools import (
        validate_coordinates,
        calculate_distance, 
        generate_api_request_template,
        analyze_api_performance,
        get_error_troubleshooting_guide
    )

def get_api_overview():
    """Provides an overview of available Bhuvan APIs and their capabilities.

    Returns:
        dict: status and comprehensive overview of all 7 Bhuvan APIs
    """
    return {
        "status": "success",
        "overview": {
            "total_apis": 7,
            "performance": {
                "average_response_time": "0.546s",
                "success_rate": "100%",
                "total_api_calls_tested": 32
            },
            "available_apis": {
                "postal_hospital": {
                    "purpose": "Find postal codes and nearby hospitals",
                    "avg_response_time": "0.507s",
                    "input": "Latitude, longitude, buffer distance",
                    "output": "Postal codes, hospital locations, administrative info"
                },
                "village_geocoding": {
                    "purpose": "Convert village names to coordinates",
                    "avg_response_time": "0.509s", 
                    "input": "Village name, state",
                    "output": "Precise coordinates, administrative boundaries"
                },
                "village_reverse_geocoding": {
                    "purpose": "Get village information from coordinates",
                    "avg_response_time": "0.513s",
                    "input": "Latitude, longitude",
                    "output": "Village name, administrative hierarchy"
                },
                "lulc_aoi_statistics": {
                    "purpose": "Land use/land cover analysis for area of interest",
                    "avg_response_time": "0.582s",
                    "input": "Polygon coordinates, analysis parameters",
                    "output": "Detailed LULC statistics, area calculations"
                },
                "routing": {
                    "purpose": "Navigation and route planning",
                    "avg_response_time": "2.602s",
                    "input": "Origin and destination coordinates",
                    "output": "Turn-by-turn directions, distance, duration"
                },
                "thematic_statistics": {
                    "purpose": "District-wise LULC statistical data",
                    "avg_response_time": "0.773s",
                    "input": "District code, year",
                    "output": "Comprehensive land use statistics"
                },
                "geoid": {
                    "purpose": "Administrative boundary identification",
                    "avg_response_time": "0.254s",
                    "input": "Latitude, longitude",
                    "output": "State, district, block, village codes"
                }
            }
        }
    }

def analyze_location_context(latitude: float, longitude: float):
    """Analyzes the geographical context of given coordinates within India.

    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate

    Returns:
        dict: status and geographical context analysis
    """
    # Use the validation tool
    validation = validate_coordinates(latitude, longitude)
    
    if not validation["valid"]:
        return {
            "status": "error",
            "error": validation["error"],
            "type": validation["type"]
        }
    
    # Determine region and suggest appropriate APIs
    region_analysis = {
        "coordinates": {"lat": latitude, "lng": longitude},
        "validation": validation,
        "region": "India" if validation["within_india"] else "Outside India",
        "recommended_apis": []
    }
    
    if validation["within_india"]:
        # Add recommendations based on location
        region_analysis["recommended_apis"] = [
            {
                "api": "geoid",
                "reason": "Get administrative boundaries for any Indian location",
                "priority": "high"
            },
            {
                "api": "village_reverse_geocoding", 
                "reason": "Identify village and administrative hierarchy",
                "priority": "high"
            },
            {
                "api": "postal_hospital",
                "reason": "Find nearby healthcare facilities and postal services",
                "priority": "medium"
            }
        ]
        
        # Add climate zone estimation
        if latitude < 10:
            climate_zone = "Tropical"
        elif latitude < 23.5:
            climate_zone = "Tropical/Subtropical"
        elif latitude < 30:
            climate_zone = "Subtropical"
        else:
            climate_zone = "Temperate/Mountain"
            
        region_analysis["climate_zone"] = climate_zone
    else:
        region_analysis["warning"] = "Coordinates outside India. Bhuvan APIs may not provide data."
    
    return {
        "status": "success",
        "analysis": region_analysis
    }

def get_api_usage_guide(api_name: str):
    """Provides detailed usage guide for a specific Bhuvan API.

    Args:
        api_name (str): Name of the API (postal_hospital, routing, geoid, etc.)

    Returns:
        dict: status and detailed usage guide
    """
    api_guides = {
        "postal_hospital": {
            "endpoint": "/api/postal-hospital",
            "method": "POST",
            "description": "Find postal codes and nearby hospitals within a specified buffer distance",
            "input_format": {
                "lat": "float (latitude)",
                "lng": "float (longitude)",
                "buffer": "int (distance in meters, default: 3000)",
                "theme": "string ('hospital', 'postal', 'all')"
            },
            "example_request": {
                "lat": 19.0760,
                "lng": 72.8777,
                "buffer": 3000,
                "theme": "all"
            },
            "output_fields": ["postal_codes", "hospitals", "administrative_info"],
            "use_cases": [
                "Healthcare facility planning",
                "Postal service coverage analysis",
                "Emergency service proximity check"
            ]
        },
        "routing": {
            "endpoint": "/api/routing",
            "method": "POST", 
            "description": "Get optimal route between two points using Bhuvan's road network",
            "input_format": {
                "origin": {"lat": "float", "lng": "float"},
                "destination": {"lat": "float", "lng": "float"}
            },
            "example_request": {
                "origin": {"lat": 19.0760, "lng": 72.8777},
                "destination": {"lat": 18.5204, "lng": 73.8567}
            },
            "output_fields": ["route_geometry", "distance", "duration", "turn_by_turn_directions"],
            "limitations": "Both coordinates should be within the same state",
            "use_cases": [
                "Navigation planning",
                "Distance calculation",
                "Route optimization"
            ]
        },
        "geoid": {
            "endpoint": "/api/geoid",
            "method": "POST",
            "description": "Get administrative boundary codes for any location in India",
            "input_format": {
                "lat": "float (latitude)",
                "lng": "float (longitude)"
            },
            "example_request": {
                "lat": 28.6139,
                "lng": 77.2090
            },
            "output_fields": ["state_code", "district_code", "block_code", "village_code"],
            "use_cases": [
                "Administrative boundary identification",
                "Government data integration",
                "Census data mapping"
            ]
        },
        "village_geocoding": {
            "endpoint": "/api/village-geocoding", 
            "method": "POST",
            "description": "Convert village names to precise coordinates",
            "input_format": {
                "village": "string (village name)",
                "state": "string (state name)"
            },
            "example_request": {
                "village": "Andheri",
                "state": "Maharashtra"
            },
            "output_fields": ["coordinates", "administrative_boundaries", "accuracy_level"],
            "use_cases": [
                "Address standardization",
                "Rural area mapping",
                "Geocoding services"
            ]
        },
        "village_reverse_geocoding": {
            "endpoint": "/api/village-reverse-geocoding",
            "method": "POST", 
            "description": "Get village and administrative information from coordinates",
            "input_format": {
                "lat": "float (latitude)",
                "lng": "float (longitude)"
            },
            "example_request": {
                "lat": 19.0760,
                "lng": 72.8777
            },
            "output_fields": ["village_name", "administrative_hierarchy", "local_names"],
            "use_cases": [
                "Reverse geocoding",
                "Location identification",
                "Address generation"
            ]
        },
        "lulc_aoi_statistics": {
            "endpoint": "/api/lulc-aoi",
            "method": "POST",
            "description": "Analyze land use and land cover for a specific area of interest",
            "input_format": {
                "polygon": "array (polygon coordinates)",
                "year": "int (analysis year)"
            },
            "output_fields": ["land_use_categories", "area_statistics", "change_analysis"],
            "use_cases": [
                "Environmental monitoring",
                "Urban planning",
                "Agricultural assessment"
            ]
        },
        "thematic_statistics": {
            "endpoint": "/api/thematic-stats",
            "method": "POST",
            "description": "Get comprehensive district-wise land use statistics",
            "input_format": {
                "district": "string (district name)",
                "year": "int (data year)"
            },
            "example_request": {
                "district": "Mumbai",
                "year": 2022
            },
            "output_fields": ["district_stats", "land_cover_breakdown", "temporal_changes"],
            "use_cases": [
                "District-level planning",
                "Statistical analysis",
                "Policy development"
            ]
        }
    }
    
    if api_name.lower() in api_guides:
        return {
            "status": "success",
            "api_guide": api_guides[api_name.lower()]
        }
    else:
        available_apis = list(api_guides.keys())
        return {
            "status": "error",
            "error_message": f"API '{api_name}' not found. Available APIs: {', '.join(available_apis)}"
        }

def suggest_api_workflow(use_case: str):
    """Suggests the best API workflow for a specific use case.

    Args:
        use_case (str): Description of the use case or project requirement

    Returns:
        dict: status and suggested workflow with API sequence
    """
    use_case_lower = use_case.lower()
    
    workflows = {
        "site_analysis": {
            "description": "Comprehensive site analysis for development or research",
            "workflow": [
                {"step": 1, "api": "geoid", "purpose": "Get administrative boundaries"},
                {"step": 2, "api": "village_reverse_geocoding", "purpose": "Identify village and local area"},
                {"step": 3, "api": "postal_hospital", "purpose": "Check nearby facilities"},
                {"step": 4, "api": "lulc_aoi_statistics", "purpose": "Analyze land use patterns"}
            ],
            "estimated_time": "2-3 seconds total"
        },
        "navigation": {
            "description": "Route planning and navigation between locations", 
            "workflow": [
                {"step": 1, "api": "village_geocoding", "purpose": "Convert addresses to coordinates if needed"},
                {"step": 2, "api": "routing", "purpose": "Get optimal route"},
                {"step": 3, "api": "postal_hospital", "purpose": "Identify facilities along route"}
            ],
            "estimated_time": "3-4 seconds total"
        },
        "urban_planning": {
            "description": "Urban development and planning analysis",
            "workflow": [
                {"step": 1, "api": "geoid", "purpose": "Administrative boundary mapping"},
                {"step": 2, "api": "thematic_statistics", "purpose": "District-level land use data"},
                {"step": 3, "api": "lulc_aoi_statistics", "purpose": "Detailed area analysis"},
                {"step": 4, "api": "postal_hospital", "purpose": "Infrastructure assessment"}
            ],
            "estimated_time": "3-4 seconds total"
        },
        "emergency_response": {
            "description": "Emergency services and disaster response planning",
            "workflow": [
                {"step": 1, "api": "village_reverse_geocoding", "purpose": "Rapid location identification"},
                {"step": 2, "api": "postal_hospital", "purpose": "Find nearest hospitals"},
                {"step": 3, "api": "routing", "purpose": "Plan emergency routes"}
            ],
            "estimated_time": "2-3 seconds total"
        }
    }
    
    # Match use case to workflow
    matched_workflow = None
    for key, workflow in workflows.items():
        if key in use_case_lower or any(keyword in use_case_lower for keyword in 
                                      ["site", "analysis", "plan", "develop", "emergency", "navigation", "route"]):
            matched_workflow = workflow
            break
    
    if matched_workflow:
        return {
            "status": "success",
            "workflow": matched_workflow,
            "note": "This is a suggested workflow. Adapt based on your specific requirements."
        }
    else:
        return {
            "status": "success",
            "general_suggestion": {
                "description": "General purpose geospatial analysis",
                "workflow": [
                    {"step": 1, "api": "geoid", "purpose": "Start with administrative context"},
                    {"step": 2, "api": "village_reverse_geocoding", "purpose": "Get local area details"},
                    {"step": 3, "api": "Choose additional APIs based on specific needs"}
                ]
            },
            "available_workflows": list(workflows.keys()),
            "note": f"No specific workflow found for '{use_case}'. Consider the general approach or specify: site analysis, navigation, urban planning, or emergency response."
        }

def get_project_status():
    """Provides current status and capabilities of the Site Analysis Backend project.

    Returns:
        dict: status and comprehensive project information
    """
    return {
        "status": "success",
        "project_info": {
            "name": "Site Analysis Backend",
            "description": "Comprehensive backend service integrating 7 Bhuvan APIs for geospatial analysis",
            "current_status": "Production Ready",
            "key_features": [
                "Complete Bhuvan API Integration (7 APIs)",
                "Real-time Geospatial Data (No simulated data)",
                "Performance Benchmarking Suite",
                "Geographic Validation",
                "Robust Error Handling",
                "100% Success Rate"
            ],
            "technology_stack": {
                "backend": "Flask",
                "apis": "Bhuvan NRSC APIs",
                "data_format": "JSON/GeoJSON",
                "validation": "Geographic boundary checking"
            },
            "testing": {
                "comprehensive_benchmarks": "Yes",
                "performance_tracking": "Yes", 
                "geographic_coverage": "India-wide",
                "latest_test_results": "32 API calls, 100% success rate"
            },
            "deployment": {
                "status": "Production Ready",
                "monitoring": "Performance benchmarks established",
                "error_handling": "Comprehensive",
                "scalability": "Tested and validated"
            }
        }
    }

# Create enhanced agent with all tools
enhanced_agent = Agent(
    name="site_analysis_expert",
    model="gemini-2.0-flash",
    description=(
        "Expert AI Assistant for the Site Analysis Backend project with comprehensive knowledge "
        "of 7 Bhuvan APIs, advanced geospatial analysis capabilities, and specialized tools for "
        "coordinate validation, distance calculation, API template generation, performance analysis, "
        "and error troubleshooting. Optimized for Indian geographical data processing."
    ),
    instruction=(
        "You are an expert AI assistant for the Site Analysis Backend project with deep knowledge of "
        "7 Bhuvan APIs and advanced geospatial analysis capabilities. You can:\n\n"
        "1. Provide API overviews and usage guides\n"
        "2. Analyze geographical contexts and validate coordinates\n" 
        "3. Suggest optimal workflows for different use cases\n"
        "4. Generate ready-to-use API request templates\n"
        "5. Calculate distances and assess routing feasibility\n"
        "6. Analyze API performance and provide optimization tips\n"
        "7. Troubleshoot errors and provide debugging guidance\n\n"
        "Focus on practical applications for site analysis, urban planning, navigation, "
        "emergency response, and geospatial research in India. Always provide accurate, "
        "actionable information with specific examples and best practices. Use the specialized "
        "tools to validate coordinates, calculate distances, and generate templates when needed."
    ),
    tools=[
        get_api_overview,
        analyze_location_context, 
        get_api_usage_guide,
        suggest_api_workflow,
        get_project_status,
        validate_coordinates,
        calculate_distance,
        generate_api_request_template,
        analyze_api_performance,
        get_error_troubleshooting_guide
    ],
)

# Keep the original agent for backward compatibility
root_agent = enhanced_agent
