import os
import sys
import json
import time
import requests
from flask import Flask
from src.api.thematic_statistics import ThematicStatisticsAPI
from src.api.routing import RoutingAPI
from src.api.geoid import GeoidAPI
from src.utils.benchmark import benchmark_api_call, generate_benchmark_report, log_benchmark
from src.utils.data_analyzer import DataAnalyzer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_benchmark_tests():
    """
    Run benchmark tests on all APIs with various test cases
    """
    print("Starting API benchmark tests...")
    
    # Create test coordinates
    test_coordinates = [
        {"lat": 12.9716, "lng": 77.5946},  # Bangalore
        {"lat": 28.6139, "lng": 77.2090},  # Delhi
        {"lat": 19.0760, "lng": 72.8777},  # Mumbai
        {"lat": 13.0827, "lng": 80.2707},  # Chennai
        {"lat": 17.3850, "lng": 78.4867}   # Hyderabad
    ]
    
    # Ensure directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/benchmarks", exist_ok=True)
    os.makedirs("data/reports", exist_ok=True)
    
    # Test Thematic Statistics API
    print("\nBenchmarking Thematic Statistics API...")
    thematic_api = ThematicStatisticsAPI()
    
    for i, coords in enumerate(test_coordinates):
        print(f"Test case {i+1}: {coords}")
        
        try:
            # Test with default parameters
            result, query_time = benchmark_api_call(thematic_api.get_statistics, coords)
            print(f"  Default parameters: {query_time} ms")
            
            # Log data fields for analysis
            if result:
                print(f"  Data fields: {list(result.keys())}")
            
            # Test with additional parameters
            result, query_time = benchmark_api_call(
                thematic_api.get_statistics, 
                coords, 
                {"detail_level": "high"}
            )
            print(f"  With detail_level=high: {query_time} ms")
            
            # Log data fields for analysis with detail_level=high
            if result:
                print(f"  Detail level data fields: {list(result.keys())}")
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            # Create a fallback mock response for visualization/testing
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            fallback_data = {
                "error": str(e),
                "coordinates": coords,
                "timestamp": timestamp,
                "fallback": True,
                # Sample data structure
                "elevation": 920,
                "landuse": "urban",
                "population_density": 12000,
                "rainfall_annual": 800
            }
            
            filename = f"data/thematic_stats_fallback_{coords['lat']}_{coords['lng']}_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(fallback_data, f, indent=2)
                
            # Log the error as a benchmark result
            log_benchmark(
                "thematic_api.get_statistics_failed", 
                [coords], 
                {"error": str(e)}, 
                0
            )
    
    # Test Geoid API
    print("\nBenchmarking Geoid API...")
    geoid_api = GeoidAPI()
    
    for i, coords in enumerate(test_coordinates):
        print(f"Test case {i+1}: {coords}")
        
        try:
            # Test with default parameters
            result, query_time = benchmark_api_call(geoid_api.get_geoid_data, coords)
            print(f"  Default parameters: {query_time} ms")
            
            # Log data fields for analysis
            if result:
                print(f"  Data fields: {list(result.keys())}")
            
            # Test with additional parameters
            result, query_time = benchmark_api_call(
                geoid_api.get_geoid_data, 
                coords, 
                {"format": "detailed"}
            )
            print(f"  With format=detailed: {query_time} ms")
            
            # Log data fields for analysis with format=detailed
            if result:
                print(f"  Detailed format data fields: {list(result.keys())}")
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            # Create a fallback mock response for visualization/testing
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            fallback_data = {
                "error": str(e),
                "coordinates": coords,
                "timestamp": timestamp,
                "fallback": True,
                # Sample data structure for visualization
                "geoid_height": 45.6,
                "undulation": 12.3,
                "reference_ellipsoid": "WGS84",
                "accuracy": "high"
            }
            
            filename = f"data/geoid_fallback_{coords['lat']}_{coords['lng']}_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(fallback_data, f, indent=2)
                
            # Log the error as a benchmark result
            log_benchmark(
                "geoid_api.get_geoid_data_failed", 
                [coords], 
                {"error": str(e)}, 
                0
            )
    
    # Test Routing API
    print("\nBenchmarking Routing API...")
    
    # Create test routes (origin to destination)
    test_routes = [
        (test_coordinates[0], test_coordinates[1]),  # Bangalore to Delhi
        (test_coordinates[1], test_coordinates[2]),  # Delhi to Mumbai
        (test_coordinates[2], test_coordinates[3]),  # Mumbai to Chennai
        (test_coordinates[3], test_coordinates[4]),  # Chennai to Hyderabad
        (test_coordinates[4], test_coordinates[0])   # Hyderabad to Bangalore
    ]
    
    routing_api = RoutingAPI()
    
    for i, (origin, destination) in enumerate(test_routes):
        print(f"Test case {i+1}: {origin} to {destination}")
        
        try:
            # Test with default parameters
            result, query_time = benchmark_api_call(routing_api.get_route, origin, destination)
            print(f"  Default parameters: {query_time} ms")
            
            # Log data fields for analysis
            if result:
                print(f"  Data fields: {list(result.keys())}")
            
            # Test with additional parameters
            result, query_time = benchmark_api_call(
                routing_api.get_route, 
                origin, 
                destination, 
                {"mode": "driving", "avoid": "tolls"}
            )
            print(f"  With mode=driving, avoid=tolls: {query_time} ms")
            
            # Log data fields for analysis with additional parameters
            if result:
                print(f"  With params data fields: {list(result.keys())}")
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            # No fallback to simulated data - we want to see real errors
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            # Log the failure for analysis
            log_benchmark("routing_api", {
                "status": "error",
                "error_type": str(type(e).__name__),
                "error_message": str(e),
                "origin": origin,
                "destination": destination,
                "timestamp": timestamp,
                "fallback": False
            })
            
            filename = f"data/route_fallback_{origin['lat']}_{origin['lng']}_to_{destination['lat']}_{destination['lng']}_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(fallback_data, f, indent=2)
                
            # Log the error as a benchmark result
            log_benchmark(
                "routing_api.get_route_failed", 
                [origin, destination], 
                {"error": str(e)}, 
                0
            )
    
    # Generate benchmark reports
    print("\nGenerating benchmark reports...")
    
    try:
        # Generate benchmark performance report
        generate_benchmark_report()
        print("Benchmark performance report generated")
        
        # Generate API comparison report
        analyzer = DataAnalyzer()
        result = analyzer.generate_comparison_report()
        print(f"API comparison report generation: {result['status']}")
        
        # List all saved files
        print("\nSaved data files:")
        
        for root, _, files in os.walk("data"):
            for file in files:
                if file.endswith(".json") and not file.startswith("."):
                    print(f"  - {os.path.join(root, file)}")
        
    except Exception as e:
        print(f"Error generating reports: {str(e)}")
    
    print("\nBenchmark tests completed!")

if __name__ == "__main__":
    # Check if we need to run tests
    if len(sys.argv) > 1 and sys.argv[1] == "benchmark":
        run_benchmark_tests()
    else:
        print("Usage: python benchmark_tests.py benchmark")
        print("This script will run benchmark tests on all APIs")
