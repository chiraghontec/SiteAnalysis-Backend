#!/usr/bin/env python3
"""
Token validation script for Bhuvan API
Run this script to check which API tokens are available and properly configured
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

try:
    from config.bhuvan_tokens import token_manager
except ImportError:
    print("Error: Could not import token_manager. Make sure you're running from the project root.")
    sys.exit(1)

def main():
    print("Bhuvan API Token Validation Report")
    print("=" * 50)
    
    # Validate tokens
    validation = token_manager.validate_tokens()
    
    print(f"Total tokens configured: {validation['total_tokens']}")
    print(f"Essential services validation: {'✅ PASSED' if validation['valid'] else '❌ FAILED'}")
    print()
    
    if validation['available_services']:
        print("Available services:")
        for service in validation['available_services']:
            print(f"  ✅ {service}")
        print()
    
    if validation['missing_essential']:
        print("Missing essential tokens:")
        for service in validation['missing_essential']:
            print(f"  ❌ {service}")
        print()
    
    # Show all token status
    print("All Service Token Status:")
    print("-" * 30)
    
    services = [
        'lulc_statistics',
        'lulc_aoi_wise', 
        'postal_hospital',
        'village_geocoding',
        'village_reverse_geocoding',
        'routing',
        'geoid',
        'legacy'
    ]
    
    for service in services:
        token = token_manager.get_token(service)
        status = "✅ SET" if token else "❌ NOT SET"
        token_preview = f"({token[:10]}...)" if token and len(token) > 10 else f"({token})" if token else ""
        print(f"  {service:<25} {status} {token_preview}")
    
    print()
    print("Environment Variables to Set:")
    print("-" * 30)
    print("BHUVAN_LULC_STATISTICS_TOKEN=your_token_here")
    print("BHUVAN_LULC_AOI_WISE_TOKEN=your_token_here")
    print("BHUVAN_POSTAL_HOSPITAL_TOKEN=your_token_here")
    print("BHUVAN_VILLAGE_GEOCODING_TOKEN=your_token_here")
    print("BHUVAN_VILLAGE_REVERSE_GEOCODING_TOKEN=your_token_here")
    print("BHUVAN_ROUTING_TOKEN=your_token_here")
    print("BHUVAN_GEOID_TOKEN=your_token_here")

if __name__ == "__main__":
    main()
