#!/usr/bin/env python3
"""
Comprehensive API Benchmark Suite
Tests all Bhuvan API endpoints for performance, reliability, and accuracy.
"""

import sys
import os
import time
import json
import statistics
from datetime import datetime
from typing import Dict, List, Any, Tuple
import requests

# Add src to path
sys.path.insert(0, 'src')

from src.api.postal_hospital import PostalHospitalAPI
from src.api.village_geocoding import VillageGeocodingAPI
from src.api.village_reverse_geocoding import VillageReverseGeocodingAPI
from src.api.lulc_aoi_wise import LULCAOIWiseAPI
from src.api.routing import RoutingAPI
from src.api.thematic_statistics import ThematicStatisticsAPI
from src.api.geoid import GeoidAPI

class APIBenchmark:
    """Comprehensive API benchmarking suite for all Bhuvan APIs."""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'total_apis': 7,
            'apis': {}
        }
        
        # Test coordinates for different states/regions
        self.test_coordinates = [
            {'lat': 12.9716, 'lng': 77.5946, 'location': 'Bangalore, Karnataka'},
            {'lat': 28.6139, 'lng': 77.2090, 'location': 'Delhi'},
            {'lat': 19.0760, 'lng': 72.8777, 'location': 'Mumbai, Maharashtra'},
            {'lat': 22.5726, 'lng': 88.3639, 'location': 'Kolkata, West Bengal'},
            {'lat': 13.0827, 'lng': 80.2707, 'location': 'Chennai, Tamil Nadu'}
        ]
        
        # Test district codes for LULC
        self.test_district_codes = ['2001', '1028', '2902', '3302', '1917']
        
        # Test routes for routing API (same state pairs)
        self.test_routes = [
            {
                'start': {'lat': 12.9716, 'lng': 77.5946},
                'end': {'lat': 12.2958, 'lng': 76.6394},
                'description': 'Bangalore to Mysore (Karnataka)'
            },
            {
                'start': {'lat': 28.6139, 'lng': 77.2090},
                'end': {'lat': 28.7041, 'lng': 77.1025},
                'description': 'Delhi Central to Delhi North'
            }
        ]
    
    def measure_performance(self, func, *args, **kwargs) -> Tuple[float, Any]:
        """Measure execution time and return result."""
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            return end_time - start_time, result
        except Exception as e:
            end_time = time.time()
            return end_time - start_time, {'error': str(e)}
    
    def analyze_response(self, result: Any) -> Dict[str, Any]:
        """Analyze API response for quality metrics."""
        analysis = {
            'success': False,
            'has_data': False,
            'data_points': 0,
            'error_message': None
        }
        
        if isinstance(result, dict):
            if 'error' in result:
                analysis['error_message'] = result['error']
            else:
                analysis['success'] = True
                # Count data points in nested structures
                data_count = 0
                for key, value in result.items():
                    if isinstance(value, (dict, list)):
                        if isinstance(value, dict):
                            data_count += len(value)
                        else:
                            data_count += len(value)
                    else:
                        data_count += 1
                
                analysis['data_points'] = data_count
                analysis['has_data'] = data_count > 0
        
        return analysis
    
    def benchmark_postal_hospital_api(self) -> Dict[str, Any]:
        """Benchmark Postal & Hospital API."""
        print("🏥 Benchmarking Postal & Hospital API...")
        api = PostalHospitalAPI()
        
        times = []
        successes = 0
        total_tests = 0
        results_data = []
        
        for coord in self.test_coordinates:
            total_tests += 1
            print(f"  Testing {coord['location']}...")
            
            exec_time, result = self.measure_performance(
                api.get_proximity_data,
                coord,
                'all',
                5000
            )
            
            times.append(exec_time)
            analysis = self.analyze_response(result)
            
            if analysis['success']:
                successes += 1
            
            results_data.append({
                'location': coord['location'],
                'execution_time': exec_time,
                'analysis': analysis
            })
            
            print(f"    Time: {exec_time:.2f}s, Success: {analysis['success']}, Data points: {analysis['data_points']}")
        
        return {
            'api_name': 'Postal & Hospital API',
            'total_tests': total_tests,
            'successes': successes,
            'success_rate': (successes / total_tests) * 100,
            'avg_response_time': statistics.mean(times),
            'min_response_time': min(times),
            'max_response_time': max(times),
            'median_response_time': statistics.median(times),
            'results': results_data
        }
    
    def benchmark_village_geocoding_api(self) -> Dict[str, Any]:
        """Benchmark Village Geocoding API."""
        print("🏘️ Benchmarking Village Geocoding API...")
        api = VillageGeocodingAPI()
        
        times = []
        successes = 0
        total_tests = 0
        results_data = []
        
        # Test with different village names
        test_villages = [
            'Bangalore',
            'Mumbai', 
            'Delhi',
            'Chennai',
            'Kolkata'
        ]
        
        for village in test_villages:
            total_tests += 1
            print(f"  Testing village: {village}...")
            
            exec_time, result = self.measure_performance(
                api.get_village_data,
                village
            )
            
            times.append(exec_time)
            analysis = self.analyze_response(result)
            
            if analysis['success']:
                successes += 1
            
            results_data.append({
                'village': village,
                'execution_time': exec_time,
                'analysis': analysis
            })
            
            print(f"    Time: {exec_time:.2f}s, Success: {analysis['success']}, Data points: {analysis['data_points']}")
        
        return {
            'api_name': 'Village Geocoding API',
            'total_tests': total_tests,
            'successes': successes,
            'success_rate': (successes / total_tests) * 100,
            'avg_response_time': statistics.mean(times),
            'min_response_time': min(times),
            'max_response_time': max(times),
            'median_response_time': statistics.median(times),
            'results': results_data
        }
    
    def benchmark_village_reverse_geocoding_api(self) -> Dict[str, Any]:
        """Benchmark Village Reverse Geocoding API."""
        print("🔄 Benchmarking Village Reverse Geocoding API...")
        api = VillageReverseGeocodingAPI()
        
        times = []
        successes = 0
        total_tests = 0
        results_data = []
        
        for coord in self.test_coordinates:
            total_tests += 1
            print(f"  Testing {coord['location']}...")
            
            exec_time, result = self.measure_performance(
                api.get_village_at_location,
                coord
            )
            
            times.append(exec_time)
            analysis = self.analyze_response(result)
            
            if analysis['success']:
                successes += 1
            
            results_data.append({
                'location': coord['location'],
                'execution_time': exec_time,
                'analysis': analysis
            })
            
            print(f"    Time: {exec_time:.2f}s, Success: {analysis['success']}, Data points: {analysis['data_points']}")
        
        return {
            'api_name': 'Village Reverse Geocoding API',
            'total_tests': total_tests,
            'successes': successes,
            'success_rate': (successes / total_tests) * 100,
            'avg_response_time': statistics.mean(times),
            'min_response_time': min(times),
            'max_response_time': max(times),
            'median_response_time': statistics.median(times),
            'results': results_data
        }
    
    def benchmark_lulc_aoi_wise_api(self) -> Dict[str, Any]:
        """Benchmark LULC AOI Wise API."""
        print("🗺️ Benchmarking LULC AOI Wise API...")
        api = LULCAOIWiseAPI()
        
        times = []
        successes = 0
        total_tests = 0
        results_data = []
        
        for coord in self.test_coordinates:
            total_tests += 1
            print(f"  Testing {coord['location']}...")
            
            # Create AOI polygon around the coordinate
            aoi_coordinates = [
                [coord['lng'] - 0.01, coord['lat'] - 0.01],
                [coord['lng'] + 0.01, coord['lat'] - 0.01],
                [coord['lng'] + 0.01, coord['lat'] + 0.01],
                [coord['lng'] - 0.01, coord['lat'] + 0.01],
                [coord['lng'] - 0.01, coord['lat'] - 0.01]
            ]
            
            exec_time, result = self.measure_performance(
                api.get_polygon_statistics,
                aoi_coordinates
            )
            
            times.append(exec_time)
            analysis = self.analyze_response(result)
            
            if analysis['success']:
                successes += 1
            
            results_data.append({
                'location': coord['location'],
                'execution_time': exec_time,
                'analysis': analysis
            })
            
            print(f"    Time: {exec_time:.2f}s, Success: {analysis['success']}, Data points: {analysis['data_points']}")
        
        return {
            'api_name': 'LULC AOI Wise API',
            'total_tests': total_tests,
            'successes': successes,
            'success_rate': (successes / total_tests) * 100,
            'avg_response_time': statistics.mean(times),
            'min_response_time': min(times),
            'max_response_time': max(times),
            'median_response_time': statistics.median(times),
            'results': results_data
        }
    
    def benchmark_routing_api(self) -> Dict[str, Any]:
        """Benchmark Routing API."""
        print("🛣️ Benchmarking Routing API...")
        api = RoutingAPI()
        
        times = []
        successes = 0
        total_tests = 0
        results_data = []
        
        for route in self.test_routes:
            total_tests += 1
            print(f"  Testing route: {route['description']}...")
            
            exec_time, result = self.measure_performance(
                api.get_route,
                route['start'],
                route['end']
            )
            
            times.append(exec_time)
            analysis = self.analyze_response(result)
            
            if analysis['success']:
                successes += 1
            
            results_data.append({
                'route': route['description'],
                'execution_time': exec_time,
                'analysis': analysis
            })
            
            print(f"    Time: {exec_time:.2f}s, Success: {analysis['success']}, Data points: {analysis['data_points']}")
        
        return {
            'api_name': 'Routing API',
            'total_tests': total_tests,
            'successes': successes,
            'success_rate': (successes / total_tests) * 100,
            'avg_response_time': statistics.mean(times) if times else 0,
            'min_response_time': min(times) if times else 0,
            'max_response_time': max(times) if times else 0,
            'median_response_time': statistics.median(times) if times else 0,
            'results': results_data
        }
    
    def benchmark_thematic_statistics_api(self) -> Dict[str, Any]:
        """Benchmark Thematic Statistics API (LULC)."""
        print("📊 Benchmarking Thematic Statistics API (LULC)...")
        api = ThematicStatisticsAPI()
        
        times = []
        successes = 0
        total_tests = 0
        results_data = []
        
        for distcode in self.test_district_codes:
            total_tests += 1
            print(f"  Testing district code: {distcode}...")
            
            exec_time, result = self.measure_performance(
                api.get_statistics,
                {'lat': 12.9716, 'lng': 77.5946},
                {'distcode': distcode, 'year': '1112'}
            )
            
            times.append(exec_time)
            analysis = self.analyze_response(result)
            
            if analysis['success']:
                successes += 1
            
            results_data.append({
                'district_code': distcode,
                'execution_time': exec_time,
                'analysis': analysis
            })
            
            print(f"    Time: {exec_time:.2f}s, Success: {analysis['success']}, Data points: {analysis['data_points']}")
        
        return {
            'api_name': 'Thematic Statistics API (LULC)',
            'total_tests': total_tests,
            'successes': successes,
            'success_rate': (successes / total_tests) * 100,
            'avg_response_time': statistics.mean(times),
            'min_response_time': min(times),
            'max_response_time': max(times),
            'median_response_time': statistics.median(times),
            'results': results_data
        }
    
    def benchmark_geoid_api(self) -> Dict[str, Any]:
        """Benchmark Geoid API."""
        print("🌍 Benchmarking Geoid API...")
        api = GeoidAPI()
        
        times = []
        successes = 0
        total_tests = 0
        results_data = []
        
        for coord in self.test_coordinates:
            total_tests += 1
            print(f"  Testing {coord['location']}...")
            
            exec_time, result = self.measure_performance(
                api.get_data,
                coord
            )
            
            times.append(exec_time)
            analysis = self.analyze_response(result)
            
            if analysis['success']:
                successes += 1
            
            results_data.append({
                'location': coord['location'],
                'execution_time': exec_time,
                'analysis': analysis
            })
            
            print(f"    Time: {exec_time:.2f}s, Success: {analysis['success']}, Data points: {analysis['data_points']}")
        
        return {
            'api_name': 'Geoid API',
            'total_tests': total_tests,
            'successes': successes,
            'success_rate': (successes / total_tests) * 100,
            'avg_response_time': statistics.mean(times),
            'min_response_time': min(times),
            'max_response_time': max(times),
            'median_response_time': statistics.median(times),
            'results': results_data
        }
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """Run comprehensive benchmarks for all APIs."""
        print("🚀 Starting Comprehensive API Benchmark Suite...")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run individual API benchmarks
        benchmarks = [
            self.benchmark_postal_hospital_api,
            self.benchmark_village_geocoding_api,
            self.benchmark_village_reverse_geocoding_api,
            self.benchmark_lulc_aoi_wise_api,
            self.benchmark_routing_api,
            self.benchmark_thematic_statistics_api,
            self.benchmark_geoid_api
        ]
        
        for benchmark_func in benchmarks:
            try:
                result = benchmark_func()
                self.results['apis'][result['api_name']] = result
                print(f"✅ {result['api_name']}: {result['success_rate']:.1f}% success rate")
            except Exception as e:
                print(f"❌ Error in {benchmark_func.__name__}: {e}")
                self.results['apis'][benchmark_func.__name__] = {
                    'error': str(e),
                    'success_rate': 0
                }
            print("-" * 40)
        
        total_time = time.time() - start_time
        self.results['total_execution_time'] = total_time
        
        # Calculate overall statistics
        self.calculate_overall_stats()
        
        return self.results
    
    def calculate_overall_stats(self):
        """Calculate overall benchmark statistics."""
        total_tests = 0
        total_successes = 0
        all_response_times = []
        api_success_rates = []
        
        for api_name, data in self.results['apis'].items():
            if 'error' not in data:
                total_tests += data['total_tests']
                total_successes += data['successes']
                api_success_rates.append(data['success_rate'])
                
                # Collect all response times
                for result in data.get('results', []):
                    all_response_times.append(result['execution_time'])
        
        self.results['overall'] = {
            'total_tests': total_tests,
            'total_successes': total_successes,
            'overall_success_rate': (total_successes / total_tests * 100) if total_tests > 0 else 0,
            'avg_api_success_rate': statistics.mean(api_success_rates) if api_success_rates else 0,
            'total_response_times': len(all_response_times),
            'avg_response_time': statistics.mean(all_response_times) if all_response_times else 0,
            'min_response_time': min(all_response_times) if all_response_times else 0,
            'max_response_time': max(all_response_times) if all_response_times else 0,
            'median_response_time': statistics.median(all_response_times) if all_response_times else 0
        }
    
    def print_summary_report(self):
        """Print a comprehensive summary report."""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE API BENCHMARK RESULTS")
        print("=" * 80)
        
        overall = self.results.get('overall', {})
        
        print(f"🕒 Total Execution Time: {self.results.get('total_execution_time', 0):.2f} seconds")
        print(f"🎯 Overall Success Rate: {overall.get('overall_success_rate', 0):.1f}%")
        print(f"⚡ Average Response Time: {overall.get('avg_response_time', 0):.3f} seconds")
        print(f"📈 Total API Calls: {overall.get('total_tests', 0)}")
        print(f"✅ Successful Calls: {overall.get('total_successes', 0)}")
        
        print("\n📋 Individual API Performance:")
        print("-" * 80)
        
        for api_name, data in self.results['apis'].items():
            if 'error' not in data:
                print(f"🔹 {api_name}")
                print(f"   Success Rate: {data['success_rate']:.1f}%")
                print(f"   Avg Response: {data['avg_response_time']:.3f}s")
                print(f"   Min Response: {data['min_response_time']:.3f}s")
                print(f"   Max Response: {data['max_response_time']:.3f}s")
                print(f"   Tests: {data['successes']}/{data['total_tests']}")
            else:
                print(f"❌ {api_name}: {data['error']}")
            print()
    
    def save_results(self, filename: str = None):
        """Save benchmark results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📄 Results saved to: {filename}")

def main():
    """Main benchmark execution."""
    benchmark = APIBenchmark()
    
    try:
        # Run all benchmarks
        results = benchmark.run_all_benchmarks()
        
        # Print summary
        benchmark.print_summary_report()
        
        # Save results
        benchmark.save_results()
        
        print("\n🎉 Benchmark suite completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Benchmark interrupted by user")
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
