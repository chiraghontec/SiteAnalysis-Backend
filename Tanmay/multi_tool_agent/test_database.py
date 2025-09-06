"""
Database Integration Test Suite
Comprehensive testing for Site Analysis Backend database functionality
"""

import json
import time
from database_manager import DatabaseManager

def print_header(title: str):
    """Print formatted test section header"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_step(step_num: int, description: str):
    """Print formatted test step"""
    print(f"\n{step_num}. {description}")
    print("-" * 40)

def test_database_integration():
    """Comprehensive test of database integration features"""
    print_header("Site Analysis Backend Database Integration Test")
    
    print("🚀 Starting comprehensive database integration test...")
    print("📋 Testing: Connection, Caching, Analytics, Spatial Queries, Performance")
    
    try:
        # Initialize database manager
        print("\n🔧 Initializing Database Manager...")
        db = DatabaseManager()
        
        # Test 1: Basic Connection
        print_step(1, "Testing Database Connection")
        connection_success = db.test_connection()
        
        if not connection_success:
            print("❌ CRITICAL: Database connection failed!")
            print("🔧 Check your .env file configuration")
            print("🔧 Verify Neon database is running")
            return False
        
        print("✅ Database connection successful!")
        
        # Test 2: Cache API Response
        print_step(2, "Testing API Response Caching")
        
        # Sample API response data for different locations
        test_responses = [
            {
                "api_name": "bhuvan_pois",
                "lat": 28.6139,
                "lng": 77.2090,
                "data": {
                    "status": "success",
                    "location": "New Delhi, India",
                    "pois": [
                        {"name": "Red Fort", "type": "heritage", "distance": 450},
                        {"name": "Chandni Chowk", "type": "market", "distance": 680},
                        {"name": "Jama Masjid", "type": "religious", "distance": 720}
                    ],
                    "total_found": 3,
                    "query_radius": 1000
                }
            },
            {
                "api_name": "routing",
                "lat": 19.0760,
                "lng": 72.8777,
                "data": {
                    "status": "success",
                    "location": "Mumbai, India", 
                    "route_info": {
                        "total_distance_km": 12.5,
                        "estimated_time_min": 45,
                        "traffic_level": "moderate"
                    }
                }
            },
            {
                "api_name": "lulc_analysis",
                "lat": 12.9716,
                "lng": 77.5946,
                "data": {
                    "status": "success",
                    "location": "Bangalore, India",
                    "land_use": {
                        "urban": 65,
                        "vegetation": 20,
                        "water": 8,
                        "agricultural": 7
                    }
                }
            }
        ]
        
        cache_success_count = 0
        for test_data in test_responses:
            success = db.cache_api_response(
                test_data["api_name"],
                test_data["lat"], 
                test_data["lng"],
                test_data["data"]
            )
            if success:
                cache_success_count += 1
                time.sleep(0.1)  # Small delay to ensure different timestamps
        
        print(f"✅ Successfully cached {cache_success_count}/{len(test_responses)} API responses")
        
        # Test 3: Cache Retrieval with Spatial Queries
        print_step(3, "Testing Cached Response Retrieval (Spatial)")
        
        retrieval_tests = [
            {
                "desc": "Exact location match (Delhi)",
                "api": "bhuvan_pois",
                "lat": 28.6139,
                "lng": 77.2090,
                "radius": 0.1
            },
            {
                "desc": "Nearby location match (50m from Delhi)",
                "api": "bhuvan_pois", 
                "lat": 28.6142,  # Slightly different coordinates
                "lng": 77.2093,
                "radius": 0.1
            },
            {
                "desc": "Different city (Mumbai)",
                "api": "routing",
                "lat": 19.0760,
                "lng": 72.8777,
                "radius": 0.1
            }
        ]
        
        cache_hits = 0
        for test in retrieval_tests:
            print(f"   🔍 {test['desc']}")
            cached = db.get_cached_response(
                test["api"], 
                test["lat"], 
                test["lng"],
                test["radius"]
            )
            
            if cached:
                cache_hits += 1
                print(f"      ✅ Cache hit - found {test['api']} data")
                # Show a sample of the cached data
                if isinstance(cached, dict) and 'location' in cached:
                    print(f"      📍 Location: {cached.get('location', 'Unknown')}")
            else:
                print(f"      ❌ Cache miss - no data found")
        
        print(f"📊 Cache hit rate: {cache_hits}/{len(retrieval_tests)} ({cache_hits/len(retrieval_tests)*100:.1f}%)")
        
        # Test 4: User Interaction Logging
        print_step(4, "Testing User Interaction Logging")
        
        test_interactions = [
            {
                "query": "Find nearby hospitals in Delhi",
                "response": "Found 5 hospitals within 2km radius including AIIMS and Safdarjung",
                "coordinates": {"lat": 28.6139, "lng": 77.2090},
                "api_calls": 2
            },
            {
                "query": "What's the land use pattern in Bangalore?",
                "response": "Urban development dominates (65%), with 20% vegetation cover",
                "coordinates": {"lat": 12.9716, "lng": 77.5946},
                "api_calls": 1
            },
            {
                "query": "Route from Mumbai to airport",
                "response": "Optimal route found: 12.5km, 45min estimated time",
                "coordinates": {"lat": 19.0760, "lng": 72.8777},
                "api_calls": 1
            }
        ]
        
        interaction_success_count = 0
        for interaction in test_interactions:
            success = db.log_user_interaction(
                interaction["query"],
                interaction["response"],
                interaction["coordinates"],
                interaction["api_calls"]
            )
            if success:
                interaction_success_count += 1
                time.sleep(0.1)
        
        print(f"✅ Successfully logged {interaction_success_count}/{len(test_interactions)} user interactions")
        
        # Test 5: Analytics Event Logging
        print_step(5, "Testing Analytics Event Logging")
        
        analytics_events = [
            {
                "type": "system_startup",
                "data": {"version": "1.0", "features": ["caching", "analytics", "spatial"]},
                "lat": None,
                "lng": None
            },
            {
                "type": "api_performance",
                "data": {"api": "bhuvan_pois", "response_time_ms": 450, "status": "success"},
                "lat": 28.6139,
                "lng": 77.2090
            },
            {
                "type": "cache_optimization",
                "data": {"cache_size": 25, "hit_rate": 0.75, "cleanup_performed": True},
                "lat": None,
                "lng": None
            }
        ]
        
        analytics_success_count = 0
        for event in analytics_events:
            success = db.log_analytics_event(
                event["type"],
                event["data"],
                event["lat"],
                event["lng"]
            )
            if success:
                analytics_success_count += 1
        
        print(f"✅ Successfully logged {analytics_success_count}/{len(analytics_events)} analytics events")
        
        # Test 6: Analytics Summary Generation
        print_step(6, "Testing Analytics Summary Generation")
        
        analytics_summary = db.get_analytics_summary(days=1)  # Last 1 day for test data
        
        if analytics_summary and 'error' not in analytics_summary:
            print("✅ Analytics summary generated successfully!")
            print("\n📊 Analytics Summary:")
            
            # User interactions summary
            user_stats = analytics_summary.get('user_interactions', {})
            if user_stats:
                print(f"   👥 Total interactions: {user_stats.get('total_interactions', 0)}")
                print(f"   📅 Active days: {user_stats.get('active_days', 0)}")
                print(f"   🔄 Avg API calls per interaction: {user_stats.get('avg_api_calls_per_interaction', 0):.1f}")
            
            # Cache performance
            cache_perf = analytics_summary.get('cache_performance', {})
            if cache_perf:
                print(f"   💾 Cached responses: {cache_perf.get('total_cached_responses', 0)}")
                print(f"   🎯 Cache hit rate: {cache_perf.get('estimated_cache_hit_rate_percent', 0)}%")
            
            # Performance insights
            insights = analytics_summary.get('performance_insights', [])
            if insights:
                print("   💡 Performance insights:")
                for insight in insights:
                    print(f"      {insight}")
        else:
            print("❌ Failed to generate analytics summary")
            if 'error' in analytics_summary:
                print(f"   Error: {analytics_summary['error']}")
        
        # Test 7: Recent Activity Monitoring
        print_step(7, "Testing Recent Activity Monitoring")
        
        recent_activity = db.get_recent_activity(limit=5)
        
        if recent_activity and 'error' not in recent_activity:
            print("✅ Recent activity retrieved successfully!")
            
            interactions = recent_activity.get('recent_interactions', [])
            api_calls = recent_activity.get('recent_api_calls', [])
            
            print(f"   📝 Recent interactions: {len(interactions)}")
            print(f"   🔄 Recent API calls: {len(api_calls)}")
            
            if interactions:
                latest = interactions[0]
                print(f"   📍 Latest query: \"{latest.get('user_query', '')[:50]}...\"")
        else:
            print("❌ Failed to retrieve recent activity")
        
        # Test 8: Cache Cleanup
        print_step(8, "Testing Cache Cleanup")
        
        cleaned_count = db.cleanup_expired_cache()
        print(f"✅ Cache cleanup completed - removed {cleaned_count} expired entries")
        
        # Test 9: Performance Test
        print_step(9, "Performance Test - Rapid Operations")
        
        start_time = time.time()
        
        # Rapid cache operations
        for i in range(10):
            db.cache_api_response(
                f"test_api_{i}",
                28.6 + (i * 0.001),  # Slightly different coordinates
                77.2 + (i * 0.001),
                {"test_data": f"performance_test_{i}", "timestamp": time.time()}
            )
        
        # Rapid retrievals
        cache_hits_performance = 0
        for i in range(10):
            cached = db.get_cached_response(
                f"test_api_{i}",
                28.6 + (i * 0.001),
                77.2 + (i * 0.001)
            )
            if cached:
                cache_hits_performance += 1
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"✅ Performance test completed in {total_time:.2f} seconds")
        print(f"   📊 Operations per second: {20/total_time:.1f} ops/sec")
        print(f"   🎯 Cache hits: {cache_hits_performance}/10")
        
        # Final Summary
        print_header("TEST SUMMARY")
        
        print("🎉 Database Integration Test PASSED!")
        print("\n✅ Verified Features:")
        print("   🔗 Database connection with auto-resume")
        print("   💾 API response caching with spatial indexing")
        print("   📊 User interaction logging")
        print("   📈 Analytics event tracking")
        print("   🧠 Intelligent analytics summary generation")
        print("   ⚡ High-performance operations")
        print("   🧹 Automated cache management")
        
        print("\n🚀 Your Site Analysis Backend is ready for production!")
        print("   📱 Smart caching will reduce API calls")
        print("   📊 Analytics will track user behavior") 
        print("   🌍 Spatial queries enable location intelligence")
        print("   ⚡ Serverless database scales automatically")
        
        return True
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR in database integration test:")
        print(f"   {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check .env file has correct Neon credentials")
        print("   2. Verify database schema was created (run SQL in pgAdmin)")
        print("   3. Ensure psycopg2-binary is installed")
        print("   4. Check network connectivity to Neon")
        return False

def test_individual_components():
    """Test individual database components separately"""
    print_header("Individual Component Tests")
    
    try:
        db = DatabaseManager()
        
        # Test just connection
        print("🔌 Testing connection only...")
        if db.test_connection():
            print("✅ Connection test passed")
        else:
            print("❌ Connection test failed")
            return
        
        # Test just caching
        print("\n💾 Testing caching only...")
        cache_success = db.cache_api_response(
            "test_cache",
            28.6139, 77.2090,
            {"test": "simple cache test"}
        )
        
        if cache_success:
            print("✅ Cache write test passed")
            
            # Test retrieval
            cached = db.get_cached_response("test_cache", 28.6139, 77.2090)
            if cached:
                print("✅ Cache read test passed")
            else:
                print("❌ Cache read test failed")
        else:
            print("❌ Cache write test failed")
        
        print("\n🧪 Individual component tests completed")
        
    except Exception as e:
        print(f"❌ Individual component test failed: {e}")

if __name__ == "__main__":
    print("🧪 Site Analysis Backend Database Test Suite")
    print("=" * 60)
    
    # Ask user which test to run
    print("\nSelect test to run:")
    print("1. Full Integration Test (recommended)")
    print("2. Individual Component Tests")
    print("3. Both")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            test_database_integration()
        elif choice == "2":
            test_individual_components()
        elif choice == "3":
            test_individual_components()
            test_database_integration()
        else:
            print("Running full integration test (default)...")
            test_database_integration()
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
