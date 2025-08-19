"""
Multi Tool Agent package for Site Analysis Backend
"""

# Import the enhanced agent which includes all tools
try:
    from .enhanced_agent import enhanced_agent, root_agent
    from .agent import agent
    
    # Export the main agents
    __all__ = ['root_agent', 'enhanced_agent', 'agent']
    
except ImportError as e:
    # Fallback if there are import issues
    print(f"Warning: Could not import enhanced_agent: {e}")
    from .agent import agent
    root_agent = agent
    enhanced_agent = agent
    __all__ = ['root_agent', 'enhanced_agent', 'agent']
