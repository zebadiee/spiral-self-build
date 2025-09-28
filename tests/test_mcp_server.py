#!/usr/bin/env python3
"""
Simple tests for MCP server functionality.
"""
import requests
import time
import subprocess
import sys
import os

def test_server_health():
    """Test server health endpoint."""
    try:
        response = requests.get("http://localhost:8000/status", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        print("✅ Server health check passed")
        return True
    except Exception as e:
        print(f"❌ Server health check failed: {e}")
        return False

def test_learning_endpoint():
    """Test learning endpoint."""
    try:
        test_data = {
            "content": "This is a test document for the self-learning system with AI and machine learning concepts.",
            "source": "test_suite",
            "metadata": {"test": True}
        }
        response = requests.post("http://localhost:8000/learn", json=test_data, timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "insights" in data
        assert len(data["insights"]) > 0
        print(f"✅ Learning endpoint passed - generated {len(data['insights'])} insights")
        return True
    except Exception as e:
        print(f"❌ Learning endpoint failed: {e}")
        return False

def test_insights_endpoint():
    """Test insights retrieval endpoint."""
    try:
        response = requests.get("http://localhost:8000/insights", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "insights" in data
        print(f"✅ Insights endpoint passed - found {len(data['insights'])} insights")
        return True
    except Exception as e:
        print(f"❌ Insights endpoint failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running MCP Server Tests...")
    print("=" * 40)
    
    tests = [test_server_health, test_learning_endpoint, test_insights_endpoint]
    passed = 0
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Brief pause between tests
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{len(tests)} passed")
    
    if passed == len(tests):
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed")
        sys.exit(1)
