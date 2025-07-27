#!/usr/bin/env python3
"""
Test script for the new plant API endpoints
"""

import requests
import json
import os

# API base URL
BASE_URL = "http://localhost:5001/api/plants"

def test_create_plant_without_image():
    """Test creating a plant without image (JSON)"""
    print("Testing: Create plant without image")
    
    data = {
        "nickname": "Test Plant",
        "latin_name": "Testus Plantus",
        "english_name": "Test Plant",
        "description": "A test plant for API testing",
        "care_instructions": "Water weekly, bright indirect light"
    }
    
    response = requests.post(BASE_URL, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_create_plant_with_image():
    """Test creating a plant with image upload"""
    print("Testing: Create plant with image upload")
    
    # This would require an actual image file
    # For testing, we'll just show the structure
    print("To test with image, use:")
    print("curl -X POST http://localhost:5001/api/plants \\")
    print("  -F 'nickname=My Plant' \\")
    print("  -F 'image=@/path/to/plant/image.jpg'")
    print("-" * 50)

def test_get_all_plants():
    """Test getting all plants"""
    print("Testing: Get all plants")
    
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_get_plant(plant_id):
    """Test getting a specific plant"""
    print(f"Testing: Get plant {plant_id}")
    
    response = requests.get(f"{BASE_URL}/{plant_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_analyze_plant_image(plant_id):
    """Test analyzing an image for an existing plant"""
    print(f"Testing: Analyze image for plant {plant_id}")
    
    # This would require an actual image file
    print("To test image analysis, use:")
    print(f"curl -X POST http://localhost:5001/api/plants/{plant_id}/analyze-image \\")
    print("  -F 'image=@/path/to/plant/image.jpg'")
    print("-" * 50)

def test_update_plant(plant_id):
    """Test updating a plant"""
    print(f"Testing: Update plant {plant_id}")
    
    data = {
        "nickname": "Updated Test Plant",
        "description": "Updated description",
        "care_instructions": "Updated care instructions"
    }
    
    response = requests.put(f"{BASE_URL}/{plant_id}", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def main():
    """Run all tests"""
    print("Plant Care API Test Suite")
    print("=" * 50)
    
    # Test creating a plant without image
    test_create_plant_without_image()
    
    # Test getting all plants
    test_get_all_plants()
    
    # Test getting a specific plant (assuming plant with ID 1 exists)
    test_get_plant(1)
    
    # Test updating a plant
    test_update_plant(1)
    
    # Test image analysis (shows curl command)
    test_analyze_plant_image(1)
    
    # Test creating plant with image (shows curl command)
    test_create_plant_with_image()
    
    print("Test suite completed!")
    print("\nTo test with actual images:")
    print("1. Start the Flask server: python run.py")
    print("2. Use the curl commands shown above with real image files")

if __name__ == "__main__":
    main() 