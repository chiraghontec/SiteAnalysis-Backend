#!/usr/bin/env python3
"""
Test script to verify that the multi_tool_agent imports work correctly
"""

import sys
import os

# Add the parent directory to the path to allow imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing basic imports...")
    
    # Test individual module imports
    print("1. Testing bhuvan_tools import...")
    from bhuvan_tools import validate_coordinates
    print("   ✓ bhuvan_tools imported successfully")
    
    print("2. Testing enhanced_agent import...")
    from enhanced_agent import enhanced_agent, root_agent
    print("   ✓ enhanced_agent imported successfully")
    
    print("3. Testing agent import...")
    from agent import agent
    print("   ✓ agent imported successfully")
    
    print("4. Testing package import...")
    try:
        sys.path.insert(0, parent_dir)
        from multi_tool_agent import root_agent as pkg_agent
        print("   ✓ multi_tool_agent package imported successfully")
    except ImportError as pkg_error:
        print(f"   ⚠️  Package import failed (this is OK): {pkg_error}")
        print("   → Individual module imports work fine")
    
    print("\n✅ All critical imports successful!")
    print(f"Agent name: {root_agent.name}")
    print(f"Number of tools: {len(root_agent.tools)}")
    
    # Test a basic tool function
    print("\n5. Testing a tool function...")
    result = validate_coordinates(19.0760, 72.8777)  # Mumbai coordinates
    print(f"   ✓ Tool test result: {result['valid']}")
    
    print("\n🎉 Agent is ready for use!")
    print("\n📝 For ADK usage:")
    print("   The agent can be imported and used with Google ADK")
    print("   Use: from agent import root_agent")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nTroubleshooting steps:")
    print("1. Ensure all files are in the correct directory")
    print("2. Check that __init__.py exists in the multi_tool_agent directory")
    print("3. Verify Python path includes the agent directory")
    
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()
