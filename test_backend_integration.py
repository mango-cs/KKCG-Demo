#!/usr/bin/env python3
"""
KKCG Analytics Dashboard - Backend Integration Test
Test script to verify backend-only mode functionality
"""

import requests
import pandas as pd
import json
from datetime import datetime

# Backend configuration
BACKEND_URL = "https://kkcgbackend-production.up.railway.app"

def test_backend_connection():
    """Test basic backend connectivity"""
    print("🔍 Testing backend connection...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend connection successful!")
            print(f"   Status: {response.status_code}")
            print(f"   Database: {data.get('database', 'unknown')}")
            return True
        else:
            print(f"❌ Backend error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def test_authentication():
    """Test authentication with demo credentials"""
    print("\n🔐 Testing authentication...")
    
    try:
        payload = {"username": "demo", "password": "demo"}
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Authentication successful!")
            print(f"   Username: demo")
            print(f"   Token: {data['access_token'][:20]}...")
            return data['access_token']
        else:
            print(f"❌ Authentication failed: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Authentication error: {str(e)}")
        return None

def test_data_endpoints(token=None):
    """Test data retrieval endpoints"""
    print("\n📊 Testing data endpoints...")
    
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    endpoints = [
        ("/outlets", "Outlets"),
        ("/dishes", "Dishes"),
        ("/demand-data", "Demand Data")
    ]
    
    results = {}
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(
                f"{BACKEND_URL}{endpoint}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                results[name] = len(data) if isinstance(data, list) else "OK"
                print(f"   ✅ {name}: {results[name]} records")
            else:
                results[name] = f"Error {response.status_code}"
                print(f"   ❌ {name}: HTTP {response.status_code}")
        except Exception as e:
            results[name] = f"Error: {str(e)}"
            print(f"   ❌ {name}: {str(e)}")
    
    return results

def test_data_structure():
    """Test data structure compatibility"""
    print("\n🔬 Testing data structure...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/demand-data", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                df = pd.DataFrame(data)
                print("✅ Data structure analysis:")
                print(f"   Records: {len(df)}")
                print(f"   Columns: {list(df.columns)}")
                
                # Check required columns
                required_cols = ['dish', 'outlet', 'predicted_demand', 'date']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if not missing_cols:
                    print("   ✅ All required columns present")
                else:
                    print(f"   ⚠️ Missing columns: {missing_cols}")
                
                return len(df) > 0
            else:
                print("   ⚠️ Empty dataset returned")
                return False
        else:
            print(f"   ❌ Data fetch failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Data structure test failed: {str(e)}")
        return False

def test_database_seeding(token=None):
    """Test database seeding functionality"""
    print("\n🌱 Testing database seeding...")
    
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/seed-data",
            headers=headers,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Database seeding successful!")
            print(f"   Message: {data.get('message', 'Seeded successfully')}")
            return True
        else:
            print(f"❌ Seeding failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Seeding error: {str(e)}")
        return False

def main():
    """Run complete backend integration test"""
    print("🚀 KKCG Analytics Dashboard - Backend Integration Test")
    print("=" * 60)
    
    # Test 1: Basic connection
    connection_ok = test_backend_connection()
    
    if not connection_ok:
        print("\n❌ CRITICAL: Backend connection failed!")
        print("   Solution: Ensure Railway backend is running")
        return
    
    # Test 2: Authentication
    token = test_authentication()
    
    # Test 3: Data endpoints
    endpoint_results = test_data_endpoints(token)
    
    # Test 4: Data structure
    structure_ok = test_data_structure()
    
    # Test 5: Database seeding (if needed)
    if not structure_ok or any("0" in str(v) for v in endpoint_results.values()):
        print("\n💡 Low data detected, testing seeding...")
        seeding_ok = test_database_seeding(token)
        
        if seeding_ok:
            # Re-test data after seeding
            print("\n🔄 Re-testing data after seeding...")
            endpoint_results = test_data_endpoints(token)
            structure_ok = test_data_structure()
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 INTEGRATION TEST SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Backend Connection", connection_ok),
        ("Authentication", token is not None),
        ("Data Endpoints", all(not str(v).startswith("Error") for v in endpoint_results.values())),
        ("Data Structure", structure_ok)
    ]
    
    for test_name, passed in tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<20} {status}")
    
    all_passed = all(passed for _, passed in tests)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Backend integration is working correctly")
        print("✅ Frontend can now be deployed to Streamlit Cloud")
        print("\n🚀 Next steps:")
        print("   1. Push code to GitHub")
        print("   2. Deploy to Streamlit Cloud")
        print("   3. Test live deployment")
    else:
        print("\n⚠️ SOME TESTS FAILED!")
        print("❌ Please fix issues before deployment")
        print("\n🔧 Troubleshooting:")
        print("   1. Check Railway backend status")
        print("   2. Verify API endpoints in browser")
        print("   3. Check authentication credentials")

if __name__ == "__main__":
    main() 