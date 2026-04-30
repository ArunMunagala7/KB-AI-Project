#!/usr/bin/env python3
"""
Complete Portfolio Manager Test Script
This will test the entire flow: add stocks → save → verify file → check dashboard
"""

import requests
import json
import os
from pathlib import Path

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_1_backend_connection():
    """Test 1: Can we reach the Flask backend?"""
    print_section("TEST 1: Backend Connection")
    try:
        response = requests.get("http://localhost:5001/portfolio", timeout=5)
        if response.ok:
            print("✅ Flask backend is reachable on port 5001")
            data = response.json()
            portfolio = data.get('portfolio', [])
            print(f"   Current portfolio has {len(portfolio)} stocks")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot reach backend: {e}")
        return False

def test_2_save_portfolio():
    """Test 2: Can we save a custom portfolio?"""
    print_section("TEST 2: Save Custom Portfolio")
    
    test_portfolio = {
        "portfolio": [
            {"ticker": "MA", "qty": 10, "avgPrice": 450.50},
            {"ticker": "NVDA", "qty": 15, "avgPrice": 850.00},
            {"ticker": "TSLA", "qty": 5, "avgPrice": 250.00}
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/update-portfolio",
            json=test_portfolio,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.ok:
            print("✅ Portfolio saved successfully!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Save failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Save failed: {e}")
        return False

def test_3_verify_file():
    """Test 3: Does the portfolio file exist?"""
    print_section("TEST 3: Verify File Creation")
    
    file_path = Path(__file__).parent / "custom_portfolio.json"
    
    if file_path.exists():
        print(f"✅ File exists at: {file_path}")
        with open(file_path, 'r') as f:
            data = json.load(f)
        print(f"   Contains {len(data)} stocks:")
        for stock in data:
            print(f"   - {stock['ticker']}: {stock['qty']} shares @ ${stock['avgPrice']}")
        return True
    else:
        print(f"❌ File not found at: {file_path}")
        return False

def test_4_load_from_backend():
    """Test 4: Does the backend load our custom portfolio?"""
    print_section("TEST 4: Backend Loads Custom Portfolio")
    
    try:
        response = requests.get("http://localhost:5001/portfolio", timeout=5)
        if response.ok:
            data = response.json()
            portfolio = data.get('portfolio', [])
            tickers = [stock['ticker'] for stock in portfolio]
            
            # Check if our custom stocks are present
            if 'MA' in tickers and 'NVDA' in tickers:
                print("✅ Backend is serving our custom portfolio!")
                print(f"   Tickers: {', '.join(tickers)}")
                return True
            else:
                print("⚠️  Backend is serving portfolio, but not our custom one")
                print(f"   Tickers: {', '.join(tickers)}")
                return False
        else:
            print(f"❌ Failed to load portfolio: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error loading portfolio: {e}")
        return False

def main():
    print("\n" + "🧪" * 30)
    print("   PORTFOLIO MANAGER - COMPLETE TEST SUITE")
    print("🧪" * 30)
    
    results = []
    
    # Run all tests
    results.append(("Backend Connection", test_1_backend_connection()))
    results.append(("Save Portfolio", test_2_save_portfolio()))
    results.append(("File Creation", test_3_verify_file()))
    results.append(("Backend Load", test_4_load_from_backend()))
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*60}")
    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print(f"{'='*60}")
        print("\n📋 NEXT STEPS:")
        print("1. Open browser: http://localhost:5173")
        print("2. Click 'Manage Portfolio'")
        print("3. You should see MA, NVDA, TSLA already loaded")
        print("4. Add more stocks or modify quantities")
        print("5. Click 'Save Portfolio' 💾")
        print("6. Navigate to Dashboard")
        print("7. Your custom portfolio should appear!")
    else:
        print(f"⚠️  {passed}/{total} TESTS PASSED")
        print(f"{'='*60}")
        print("\nSome tests failed. Check the output above for details.")
    
    print()

if __name__ == "__main__":
    main()
