"""
Test Agent table functionality
"""

import uuid
from database_manager import DatabaseManager

def test_agent_functionality():
    """Test the Agent table CRUD operations"""
    print("🧪 Testing Agent Table Functionality")
    
    # Initialize database manager
    db = DatabaseManager()
    
    # Test connection first
    if not db.test_connection():
        print("❌ Database connection failed")
        return False
    
    # Generate unique session ID
    session_id = f"test-{uuid.uuid4()}"
    user_id = 12345  # Use integer for user_id since it's INTEGER type in DB
    
    print(f"📝 Testing with session_id: {session_id}")
    
    # Test 1: Create agent session
    print("\n1️⃣ Testing create_agent_session...")
    result = db.create_agent_session(session_id, user_id)
    if result:
        print("✅ Agent session created successfully")
    else:
        print("❌ Failed to create agent session")
        return False
    
    # Test 2: Get agent session
    print("\n2️⃣ Testing get_agent_session...")
    session_data = db.get_agent_session(session_id)
    if session_data:
        print("✅ Agent session retrieved successfully")
        print(f"   Session ID: {session_data.get('session_id')}")
        print(f"   User ID: {session_data.get('user_id')}")
        print(f"   API Count: {session_data.get('api_count', 0)}")
    else:
        print("❌ Failed to retrieve agent session")
        return False
    
    # Test 3: Update agent session with user query
    print("\n3️⃣ Testing update_agent_session (user query)...")
    result = db.update_agent_session(
        session_id=session_id,
        user_query="Test query: Where are hospitals in Bangalore?"
    )
    if result:
        print("✅ Agent session updated with user query")
    else:
        print("❌ Failed to update agent session with user query")
    
    # Test 4: Update agent session with coordinates
    print("\n4️⃣ Testing update_agent_session (coordinates)...")
    result = db.update_agent_session(
        session_id=session_id,
        coordinate={"lat": 12.9716, "lng": 77.5946}
    )
    if result:
        print("✅ Agent session updated with coordinates")
    else:
        print("❌ Failed to update agent session with coordinates")
    
    # Test 5: Update agent session with API call
    print("\n5️⃣ Testing update_agent_session (API call)...")
    result = db.update_agent_session(
        session_id=session_id,
        api_call={"api_name": "postal_hospital", "success": True}
    )
    if result:
        print("✅ Agent session updated with API call")
    else:
        print("❌ Failed to update agent session with API call")
    
    # Test 6: Update agent session with response length
    print("\n6️⃣ Testing update_agent_session (response length)...")
    result = db.update_agent_session(
        session_id=session_id,
        response_length=250
    )
    if result:
        print("✅ Agent session updated with response length")
    else:
        print("❌ Failed to update agent session with response length")
    
    # Test 7: Get updated session data
    print("\n7️⃣ Testing updated session data...")
    updated_data = db.get_agent_session(session_id)
    if updated_data:
        print("✅ Updated session data retrieved")
        print(f"   User Queries: {len(updated_data.get('user_queries', []))}")
        print(f"   Coordinates: {len(updated_data.get('coordinates', []))}")
        print(f"   API Calls: {updated_data.get('api_count', 0)}")
        print(f"   Response Length: {updated_data.get('response_length', 0)}")
    else:
        print("❌ Failed to retrieve updated session data")
    
    # Test 8: Get agent analytics
    print("\n8️⃣ Testing get_agent_analytics...")
    analytics = db.get_agent_analytics(days=1)
    if analytics and "error" not in analytics:
        print("✅ Agent analytics retrieved")
        totals = analytics.get("totals", {})
        print(f"   Total Sessions: {totals.get('total_sessions', 0)}")
        print(f"   Total API Calls: {totals.get('total_api_calls', 0)}")
        print(f"   API Distribution: {analytics.get('api_distribution', {})}")
    else:
        print("❌ Failed to retrieve agent analytics")
    
    print("\n🎉 All Agent table tests completed!")
    return True

if __name__ == "__main__":
    try:
        test_agent_functionality()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()