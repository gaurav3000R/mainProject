#!/usr/bin/env python3
"""
Fetch all Redmine API metadata and store in JSON file.

This script calls all Redmine API endpoints from api_details.json
and stores the responses in a comprehensive metadata JSON file.
"""

import json
import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.redmine_client import redmine_client, _redmine_config
from src.utils.logger import app_logger


async def fetch_all_metadata():
    """Fetch metadata from all Redmine API endpoints."""
    
    print("="*70)
    print("REDMINE API METADATA FETCHER")
    print("="*70)
    
    metadata = {
        "fetched_at": datetime.now().isoformat(),
        "base_url": _redmine_config.redmin_api_base_url,
        "endpoints": {}
    }
    
    # Read API details
    api_details_path = Path("redminDocs/api_details.json")
    with open(api_details_path, 'r') as f:
        api_details = json.load(f)
    
    external_apis = api_details['external_apis']['endpoints']
    
    print(f"\n📡 Found {len(external_apis)} endpoints to call\n")
    
    # Fetch each endpoint
    for i, api in enumerate(external_apis, 1):
        method_name = api['method_name']
        endpoint = api['endpoint']
        description = api['description']
        
        print(f"{i}. Fetching {method_name}...")
        print(f"   Endpoint: {endpoint}")
        print(f"   Description: {description}")
        
        try:
            # Call the appropriate method
            if method_name == "validateConnection":
                data = await redmine_client.validate_connection()
            elif method_name == "getProjects":
                data = await redmine_client.get_projects(limit=100)
            elif method_name == "getIssues":
                data = await redmine_client.get_issues(limit=100)
            elif method_name == "getTimeEntries":
                data = await redmine_client.get_time_entries(limit=100)
            elif method_name == "getIssueStatuses":
                data = await redmine_client.get_issue_statuses()
            elif method_name == "getPriorities":
                data = await redmine_client.get_priorities()
            elif method_name == "getTrackers":
                data = await redmine_client.get_trackers()
            else:
                print(f"   ⚠️  Unknown method: {method_name}")
                data = None
            
            # Store the response
            metadata["endpoints"][method_name] = {
                "url": f"{_redmine_config.redmin_api_base_url}{endpoint}",
                "method": api['http_method'],
                "description": description,
                "status": "success",
                "data": data,
                "fetched_at": datetime.now().isoformat()
            }
            
            # Print summary
            if isinstance(data, dict):
                if 'user' in data:
                    print(f"   ✅ Success: User {data['user'].get('login', 'N/A')}")
                elif len(data) == 1:
                    key = list(data.keys())[0]
                    count = len(data[key]) if isinstance(data[key], list) else 1
                    print(f"   ✅ Success: {count} items")
                else:
                    print(f"   ✅ Success: {len(data)} keys")
            elif isinstance(data, list):
                print(f"   ✅ Success: {len(data)} items")
            else:
                print(f"   ✅ Success")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            metadata["endpoints"][method_name] = {
                "url": f"{_redmine_config.redmin_api_base_url}{endpoint}",
                "method": api['http_method'],
                "description": description,
                "status": "error",
                "error": str(e),
                "fetched_at": datetime.now().isoformat()
            }
        
        print()
    
    # Save to file
    output_path = Path("redminDocs/redmine_metadata.json")
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2, default=str)
    
    print("="*70)
    print(f"✅ Metadata saved to: {output_path}")
    print("="*70)
    
    # Print summary
    total = len(metadata["endpoints"])
    success = sum(1 for ep in metadata["endpoints"].values() if ep["status"] == "success")
    failed = total - success
    
    print(f"\n📊 Summary:")
    print(f"   Total endpoints: {total}")
    print(f"   Successful: {success}")
    print(f"   Failed: {failed}")
    
    # Print what was fetched
    print(f"\n📦 Data Collected:")
    for name, data in metadata["endpoints"].items():
        if data["status"] == "success":
            if isinstance(data.get("data"), dict):
                if "user" in data["data"]:
                    print(f"   ✓ {name}: Current user info")
                else:
                    keys = list(data["data"].keys())
                    print(f"   ✓ {name}: {keys}")
            elif isinstance(data.get("data"), list):
                print(f"   ✓ {name}: {len(data['data'])} items")
            else:
                print(f"   ✓ {name}: Data retrieved")
        else:
            print(f"   ✗ {name}: {data.get('error', 'Failed')}")
    
    print(f"\n💾 Full response data saved to: {output_path}")
    print(f"📝 File size: {output_path.stat().st_size / 1024:.2f} KB")
    
    return metadata


async def main():
    """Main entry point."""
    try:
        metadata = await fetch_all_metadata()
        print("\n✨ Done!")
        return metadata
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(main())
