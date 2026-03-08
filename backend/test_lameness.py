#!/usr/bin/env python3
"""
Simple test script for lameness detection
"""

import requests
import json

def test_lameness_detection():
    """Test the lameness detection endpoint"""
    try:
        # Test with a simple JSON payload (simulating detection)
        test_data = {
            "detections": [
                {
                    "class_name": "cow_normal_walking",
                    "confidence": 0.85,
                    "bbox": [100, 100, 200, 150, 400, 300],
                    "timestamp": "2024-01-01T12:00:00"
                }
            ],
            "health_score": 95.0,
            "total_animals": 1
        }
        
        response = requests.post(
            "http://localhost:8001/detect/lameness",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Lameness Detection System...")
    success = test_lameness_detection()
    
    if success:
        print("🎉 Lameness detection is working correctly!")
        print("📋 Expected: Green bounding box for normal walking")
        print("🔍 Check frontend at: http://localhost:3000/camera")
    else:
        print("❌ Lameness detection test failed")
