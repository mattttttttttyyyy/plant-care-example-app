#!/usr/bin/env python3
"""
Simple test script for the Plant Care API
"""

import requests
import json

BASE_URL = "http://localhost:5001"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_plants_api():
    """Test the plants API endpoints"""
    try:
        # Test GET /api/plants
        response = requests.get(f"{BASE_URL}/api/plants")
        print(f"✅ GET /api/plants: {response.status_code}")
        plants = response.json()
        print(f"   Found {len(plants)} plants")
        
        # Test POST /api/plants
        new_plant = {
            "nickname": "Test Plant",
            "latin_name": "Testus Plantus"
        }
        response = requests.post(f"{BASE_URL}/api/plants", json=new_plant)
        print(f"✅ POST /api/plants: {response.status_code}")
        
        if response.status_code == 201:
            created_plant = response.json()
            plant_id = created_plant['id']
            print(f"   Created plant with ID: {plant_id}")
            
            # Test GET /api/plants/{id}
            response = requests.get(f"{BASE_URL}/api/plants/{plant_id}")
            print(f"✅ GET /api/plants/{plant_id}: {response.status_code}")
            
            # Test DELETE /api/plants/{id}
            response = requests.delete(f"{BASE_URL}/api/plants/{plant_id}")
            print(f"✅ DELETE /api/plants/{plant_id}: {response.status_code}")
            
            return True
        else:
            print(f"❌ Failed to create plant: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Plants API test failed: {e}")
        return False

def test_chat_api():
    """Test the chat API endpoints"""
    try:
        # First create a test plant
        new_plant = {
            "nickname": "Chat Test Plant",
            "latin_name": "Chatus Testus"
        }
        response = requests.post(f"{BASE_URL}/api/plants", json=new_plant)
        
        if response.status_code == 201:
            plant_id = response.json()['id']
            print(f"✅ Created test plant with ID: {plant_id}")
            
            # Test GET /api/chat/history/{plant_id}
            response = requests.get(f"{BASE_URL}/api/chat/history/{plant_id}")
            print(f"✅ GET /api/chat/history/{plant_id}: {response.status_code}")
            
            # Test POST /api/chat/message/{plant_id}
            message_data = {
                "message": "Hello, this is a test message!"
            }
            response = requests.post(f"{BASE_URL}/api/chat/message/{plant_id}", json=message_data)
            print(f"✅ POST /api/chat/message/{plant_id}: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   AI Response: {result.get('response', 'No response')[:100]}...")
            
            # Clean up
            requests.delete(f"{BASE_URL}/api/plants/{plant_id}")
            return True
        else:
            print(f"❌ Failed to create test plant for chat: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Plant Care API...")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health():
        print("❌ Health check failed, stopping tests")
        return
    
    print()
    
    # Test plants API
    if test_plants_api():
        print("✅ Plants API tests passed")
    else:
        print("❌ Plants API tests failed")
    
    print()
    
    # Test chat API
    if test_chat_api():
        print("✅ Chat API tests passed")
    else:
        print("❌ Chat API tests failed")
    
    print()
    print("🎉 API testing completed!")

if __name__ == "__main__":
    main() 