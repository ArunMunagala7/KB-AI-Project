#!/usr/bin/env python3
"""Simple test for the update-portfolio endpoint"""

import requests
import json

def test_update_portfolio():
    url = "http://localhost:5001/update-portfolio"
    test_portfolio = {
        "portfolio": [
            {"ticker": "MA", "qty": 10, "avgPrice": 450.50},
            {"ticker": "TSLA", "qty": 5, "avgPrice": 250.00}
        ]
    }
    
    print(f"Testing POST to {url}")
    print(f"Payload: {json.dumps(test_portfolio, indent=2)}")
    
    try:
        response = requests.post(
            url,
            json=test_portfolio,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.ok:
            print("\n✅ SUCCESS! Portfolio saved.")
        else:
            print(f"\n❌ FAILED with status {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("\n⏱️ Request timed out after 5 seconds")
    except requests.exceptions.ConnectionError as e:
        print(f"\n🔌 Connection error: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_update_portfolio()
