#!/usr/bin/env python3
"""
Quick Map Integration Test
"""

import sys
import os
from datetime import datetime

# Add the path to import database_manager
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from database_manager import DatabaseManager
    print("✅ Database manager imported successfully")
except ImportError as e:
    print(f"❌ Failed to import database manager: {e}")
    sys.exit(1)

def quick_test():
    """Quick test of map functionality"""
    try:
        print("🧪 Quick Map Integration Test...")
        
        # Initialize database manager
        db = DatabaseManager()
        
        # Test connection
        if not db.test_connection():
            print("❌ Database connection failed")
            return False
        
        # Create a test session
        session_id = f"quick_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"📝 Creating session: {session_id}")
        
        agent_created = db.create_agent_session(session_id=session_id, user_id=1)
        
        if agent_created:
            print("✅ Agent session created")
            
            # Now test map interaction
            success = db.save_map_interaction(
                session_id=session_id,
                latitude=28.6139,
                longitude=77.2090,
                location_data={"test": True},
                user_id=1,
                interaction_type="test_point"
            )
            
            if success:
                print("✅ Map interaction saved!")
                
                # Test retrieval
                data = db.get_session_map_data(session_id)
                print(f"✅ Retrieved {data['total_interactions']} interactions")
                
                return True
            else:
                print("❌ Failed to save map interaction")
                return False
        else:
            print("❌ Failed to create agent session")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n🎉 Quick test PASSED!")
    else:
        print("\n❌ Quick test FAILED!")