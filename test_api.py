#!/usr/bin/env python3
"""Test script for National Rail API."""

import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "https://api1.raildata.org.uk/1010-live-departure-board-dep1_2/LDBWS/api/20220120/GetDepartureBoard"
USER_AGENT = "ParkRail/1.1"

async def test_api():
    """Test the National Rail API connection."""
    api_key = os.getenv("NATIONAL_RAIL_API_KEY")
    
    if not api_key:
        print("Error: NATIONAL_RAIL_API_KEY not found in .env file")
        return
    
    # Test with Waterloo station
    station_code = "WAT"
    url = f"{BASE_URL}/{station_code}"
    
    headers = {
        "x-apikey": api_key,
        "User-Agent": USER_AGENT,
    }
    
    params = {
        "numRows": 5,
        "timeWindow": 120,
        "timeOffset": 0,
    }
    
    print(f"Testing API connection to: {url}")
    print(f"Headers: {headers}")
    print(f"Params: {params}")
    print("-" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                print(f"Response status: {response.status}")
                print(f"Response headers: {dict(response.headers)}")
                
                if response.status == 200:
                    data = await response.json()
                    print("✅ API connection successful!")
                    print(f"Station: {data.get('locationName')}")
                    print(f"CRS: {data.get('crs')}")
                    print(f"Generated at: {data.get('generatedAt')}")
                    print(f"Number of trains: {len(data.get('trainServices', []))}")
                    
                    # Show first train details
                    trains = data.get('trainServices', [])
                    if trains:
                        first_train = trains[0]
                        print(f"\nFirst train:")
                        print(f"  Destination: {first_train.get('destination', [{}])[0].get('locationName', 'Unknown')}")
                        print(f"  Scheduled: {first_train.get('std')}")
                        print(f"  Expected: {first_train.get('etd')}")
                        print(f"  Platform: {first_train.get('platform')}")
                        print(f"  Operator: {first_train.get('operator')}")
                        print(f"  Cancelled: {first_train.get('isCancelled')}")
                    
                    # Save full response for inspection
                    with open("api_response.json", "w") as f:
                        json.dump(data, f, indent=2)
                    print(f"\nFull response saved to api_response.json")
                    
                else:
                    error_text = await response.text()
                    print(f"❌ API request failed: {error_text}")
                    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_api()) 