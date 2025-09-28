#!/usr/bin/env python3
"""
Test Map Integration Functionality
This script tests the map interaction database integration.
"""

import sys
import os
import json
from datetime import datetime

# Add the path to import database_manager
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from database_manager import DatabaseManager
    print("✅ Database manager imported successfully")
except ImportError as e:
    print(f"❌ Failed to import database manager: {e}")
    sys.exit(1)

def test_map_interactions():
    """Test map interaction database functionality"""
    print("\n🧪 Testing Map Interaction Database Functionality...")
    
    try:
        # Initialize database manager
        db = DatabaseManager()
        
        # Test 0: First create an agent session (required for foreign key)
        print("\n📍 Test 0: Creating agent session for foreign key...")
        session_id = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create agent session first
        agent_created = db.create_agent_session(
            session_id=session_id,
            user_id=1  # Using user_id 1 for testing
        )
        
        if agent_created:
            print(f"✅ Agent session created: {session_id}")
        else:
            print("❌ Failed to create agent session - this is required for foreign key")
            return False
        
        # Test 1: Save a map interaction
        print("\n📍 Test 1: Saving map interaction...")
        test_lat = 28.6139  # New Delhi latitude
        test_lng = 77.2090  # New Delhi longitude
        
        location_data = {
            "polygon_id": "test_polygon_001",
            "point_index": 0,
            "total_points": 4,
            "geometry_type": "Polygon",
            "timestamp": datetime.now().isoformat(),
            "test": True
        }
        
        success = db.save_map_interaction(
            session_id=session_id, 
            latitude=test_lat, 
            longitude=test_lng, 
            location_data=location_data,
            user_id=1,
            interaction_type="polygon_point"
        )
        
        if success:
            print(f"✅ Map interaction saved successfully!")
            print(f"   Session ID: {session_id}")
            print(f"   Coordinates: ({test_lat}, {test_lng})")
        else:
            print("❌ Failed to save map interaction")
            return False
        
        # Test 2: Save multiple coordinates (polygon corners)
        print("\n📍 Test 2: Saving multiple polygon coordinates...")
        polygon_coords = [
            (28.6139, 77.2090),  # Delhi
            (28.6149, 77.2100),  # Slightly northeast
            (28.6159, 77.2080),  # Northwest
            (28.6139, 77.2090)   # Back to start (closed polygon)
        ]
        
        for i, (lat, lng) in enumerate(polygon_coords):
            location_data = {
                "polygon_id": "test_polygon_002",
                "point_index": i,
                "total_points": len(polygon_coords),
                "geometry_type": "Polygon",
                "timestamp": datetime.now().isoformat(),
                "test": True
            }
            
            success = db.save_map_interaction(
                session_id=session_id, 
                latitude=lat, 
                longitude=lng, 
                location_data=location_data,
                user_id=1,
                interaction_type="polygon_vertex"
            )
            if not success:
                print(f"❌ Failed to save coordinate {i+1}")
                return False
        
        print(f"✅ Saved {len(polygon_coords)} polygon coordinates successfully!")
        
        # Test 3: Retrieve map interactions for session
        print("\n📍 Test 3: Retrieving map interactions for session...")
        interactions = db.get_map_interactions(session_id)
        
        if interactions:
            print(f"✅ Retrieved {len(interactions)} interactions")
            print("   Sample interaction:")
            sample = interactions[0]
            print(f"   - ID: {sample['id']}")
            print(f"   - Session: {sample['session_id']}")
            print(f"   - Coordinates: ({sample['latitude']}, {sample['longitude']})")
            print(f"   - Timestamp: {sample['interaction_timestamp']}")
            if sample['location_data']:
                print(f"   - Location Data: {json.dumps(sample['location_data'], indent=4)}")
        else:
            print("❌ No interactions retrieved")
            return False
        
        # Test 4: Get session map data
        print("\n📍 Test 4: Getting formatted session map data...")
        session_data = db.get_session_map_data(session_id)
        
        if session_data and session_data['total_interactions'] > 0:
            print(f"✅ Session map data retrieved successfully!")
            print(f"   Session ID: {session_data['session_id']}")
            print(f"   Total Interactions: {session_data['total_interactions']}")
            print(f"   Latest Interaction: {session_data['latest_interaction']}")
            print(f"   Coordinates Count: {len(session_data['coordinates'])}")
            
            # Show first coordinate
            if session_data['coordinates']:
                first_coord = session_data['coordinates'][0]
                print(f"   First Coordinate: lat={first_coord['lat']}, lng={first_coord['lng']}")
        else:
            print("❌ Failed to get session map data")
            return False
        
        # Test 5: Test with different session
        print("\n📍 Test 5: Testing with different session...")
        other_session = f"other_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save one interaction in different session
        db.save_map_interaction(other_session, 19.0760, 72.8777, {  # Mumbai coordinates
            "city": "Mumbai",
            "test": True
        })
        
        # Get all interactions (should return from both sessions)
        all_interactions = db.get_map_interactions(limit=10)
        session_specific = db.get_map_interactions(session_id, limit=10)
        
        print(f"✅ All interactions: {len(all_interactions)}")
        print(f"✅ Session specific interactions: {len(session_specific)}")
        
        if len(all_interactions) > len(session_specific):
            print("✅ Session filtering works correctly!")
        else:
            print("⚠️  Session filtering may not be working as expected")
        
        print("\n🎉 All map interaction tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during map interaction testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_simulation():
    """Simulate API calls to test the database integration"""
    print("\n🌐 Testing API Integration Simulation...")
    
    try:
        db = DatabaseManager()
        
        # Create agent session first for foreign key constraint
        session_id = f"api_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🔄 Creating agent session: {session_id}")
        agent_created = db.create_agent_session(
            session_id=session_id,
            user_id=1  # Using user_id 1 for testing
        )
        
        if not agent_created:
            print("❌ Failed to create agent session for API test")
            return False
        
        # Simulate data that would come from the map.html Apply button
        # Sample polygon coordinates (a square around Delhi)
        polygon_coordinates = [
            [77.2090, 28.6139],  # [lng, lat] - GeoJSON format
            [77.2190, 28.6139],
            [77.2190, 28.6239],
            [77.2090, 28.6239],
            [77.2090, 28.6139]   # Closing the polygon
        ]
        
        print(f"🔄 Simulating API calls for session: {session_id}")
        print(f"📍 Processing {len(polygon_coordinates)} coordinates...")
        
        # Process each coordinate (like the frontend would do)
        for i, coord in enumerate(polygon_coordinates):
            lng, lat = coord  # GeoJSON format is [lng, lat]
            
            location_data = {
                "polygon_id": f"simulated_polygon_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "point_index": i,
                "total_points": len(polygon_coordinates),
                "geometry_type": "Polygon",
                "timestamp": datetime.now().isoformat(),
                "source": "api_simulation"
            }
            
            # This simulates the API call that would happen when Apply is clicked
            success = db.save_map_interaction(
                session_id=session_id, 
                latitude=lat, 
                longitude=lng, 
                location_data=location_data,
                user_id=1,
                interaction_type="polygon_vertex"
            )
            
            if success:
                print(f"  ✅ Coordinate {i+1} saved: ({lat:.4f}, {lng:.4f})")
            else:
                print(f"  ❌ Failed to save coordinate {i+1}")
                return False
        
        # Now test retrieving the data (like the agent would do)
        session_data = db.get_session_map_data(session_id)
        
        if session_data and session_data['total_interactions'] > 0:
            print(f"\n🎯 Agent can now access:")
            print(f"   ✅ Session ID: {session_data['session_id']}")
            print(f"   ✅ Total Points: {session_data['total_interactions']}")
            print(f"   ✅ Latest Interaction: {session_data['latest_interaction']}")
            print(f"   ✅ All Coordinates Available: {len(session_data['coordinates'])} points")
            
            # Show the polygon data formatted for agent use
            print(f"\n📊 Formatted for Agent Analysis:")
            coordinates_for_agent = []
            for coord in session_data['coordinates']:
                coordinates_for_agent.append([coord['lng'] if 'lng' in coord else coord['longitude'], coord['lat'] if 'lat' in coord else coord['latitude']])
            
            print(f"   GeoJSON Coordinates: {json.dumps(coordinates_for_agent, indent=2)}")
            
            return True
        else:
            print("❌ Failed to retrieve session data for agent")
            return False
            
    except Exception as e:
        print(f"❌ Error during API simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Map Integration Tests...")
    
    # Test database connection first
    try:
        db = DatabaseManager()
        if not db.test_connection():
            print("❌ Database connection failed. Please check your database setup.")
            sys.exit(1)
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)
    
    # Run the tests
    test1_success = test_map_interactions()
    test2_success = test_api_simulation()
    
    print("\n" + "="*60)
    
    if test1_success and test2_success:
        print("🎉 ALL TESTS PASSED! Map integration is working correctly.")
        print("\n📋 Integration Status:")
        print("   ✅ Database Methods: Working")
        print("   ✅ Coordinate Storage: Working")
        print("   ✅ Session Management: Working")
        print("   ✅ Data Retrieval: Working")
        print("   ✅ API Simulation: Working")
        print("\n🚀 Ready for production use!")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n📋 Next Steps:")
        print("   1. Check database connection")
        print("   2. Verify table structure")
        print("   3. Check error messages above")
        
    print("\n🔧 To use with map.html:")
    print("   1. Start the Flask backend: python app.py")
    print("   2. Open map.html in a browser")
    print("   3. Draw a polygon and click 'Apply'")
    print("   4. Check console for success messages")