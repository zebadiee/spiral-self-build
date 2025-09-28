#!/usr/bin/env python3
"""
Simple smoke test for FastAPI endpoints using direct ASGI testing
Addresses issues with port conflicts, multiprocessing, and missing dependencies
"""

import sys
import traceback
import asyncio
import json
from typing import Optional, Dict, Any

def test_imports() -> bool:
    """Test that all required imports are available"""
    print("🔍 Checking imports...")
    
    try:
        import fastapi
        print("✅ FastAPI available")
    except ImportError as e:
        print(f"🚫 FastAPI not available: {e}")
        print("💡 Install with: pip install fastapi")
        return False
    
    try:
        import sys
        import os
        # Add parent directory to path to find fastapi_app
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        import fastapi_app
        print("✅ FastAPI app module available")
    except ImportError as e:
        print(f"🚫 FastAPI app module not available: {e}")
        print("💡 Make sure fastapi_app.py is in the project root directory")
        return False
    
    return True

async def call_asgi_app(app, method: str, path: str) -> Dict[str, Any]:
    """Call ASGI app directly without TestClient"""
    
    # Create ASGI scope
    scope = {
        "type": "http",
        "method": method,
        "path": path,
        "query_string": b"",
        "headers": [
            [b"host", b"testserver"],
            [b"user-agent", b"test-client"],
        ],
        "server": ("testserver", 80),
        "scheme": "http",
    }
    
    # Storage for response
    response_data = {
        "status": None,
        "headers": [],
        "body": b"",
    }
    
    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}
    
    async def send(message):
        if message["type"] == "http.response.start":
            response_data["status"] = message["status"]
            response_data["headers"] = message.get("headers", [])
        elif message["type"] == "http.response.body":
            response_data["body"] += message.get("body", b"")
    
    # Call the ASGI app
    await app(scope, receive, send)
    
    return response_data

def test_endpoints() -> bool:
    """Test all FastAPI endpoints using direct ASGI calls"""
    print("\n🚀 Starting endpoint tests...")
    
    try:
        import sys
        import os
        # Add parent directory to path to find fastapi_app
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        import fastapi_app
        
        print("✅ Using direct ASGI testing (no port conflicts)")
        
        # Test 1: Root endpoint
        print("🔍 Testing root endpoint (/)...")
        response = asyncio.run(call_asgi_app(fastapi_app.app, "GET", "/"))
        
        if response["status"] != 200:
            print(f"❌ Root endpoint failed with status {response['status']}")
            return False
        
        # Parse JSON response
        try:
            data = json.loads(response["body"].decode())
        except json.JSONDecodeError as e:
            print(f"❌ Root endpoint returned invalid JSON: {e}")
            return False
        
        if data.get("message") != "Hello from Spiral Codex":
            print(f"❌ Root endpoint returned unexpected message: {data.get('message')}")
            return False
        
        print("✅ Root endpoint working correctly")
        
        # Test 2: Docs endpoint
        print("🔍 Testing docs endpoint (/docs)...")
        response = asyncio.run(call_asgi_app(fastapi_app.app, "GET", "/docs"))
        
        if response["status"] != 200:
            print(f"❌ Docs endpoint failed with status {response['status']}")
            return False
        
        print("✅ Docs endpoint accessible")
        
        # Test 3: Metrics endpoint
        print("🔍 Testing metrics endpoint (/metrics)...")
        response = asyncio.run(call_asgi_app(fastapi_app.app, "GET", "/metrics"))
        
        if response["status"] != 200:
            print(f"❌ Metrics endpoint failed with status {response['status']}")
            return False
        
        # Check content type
        content_type = ""
        for header_name, header_value in response["headers"]:
            if header_name.lower() == b"content-type":
                content_type = header_value.decode()
                break
        
        if "text/plain" not in content_type:
            print(f"❌ Metrics endpoint has wrong content-type: {content_type}")
            return False
        
        # Check metrics content
        metrics_text = response["body"].decode()
        
        # Verify expected metrics are present
        expected_metrics = [
            "# HELP http_requests_total Total HTTP requests",
            "# TYPE http_requests_total counter", 
            "http_requests_total 42",
            "# HELP app_info Application info",
            "# TYPE app_info gauge",
            'app_info{version="1.0"} 1'
        ]
        
        for expected in expected_metrics:
            if expected not in metrics_text:
                print(f"❌ Missing expected metric: {expected}")
                return False
        
        print("✅ Metrics endpoint working correctly")
        print("✅ Prometheus format validated")
        
        return True
        
    except Exception as e:
        print(f"❌ Endpoint test failed with exception: {e}")
        print(f"🔍 Traceback: {traceback.format_exc()}")
        return False

def main() -> int:
    """Main test runner"""
    print("🧪 Simple Smoke Test for Spiral Self-Build FastAPI")
    print("=" * 50)
    
    # Test imports first
    if not test_imports():
        print("\n💥 Import tests failed!")
        return 1
    
    # Test endpoints
    if not test_endpoints():
        print("\n💥 Endpoint tests failed!")
        return 1
    
    print("\n🎉 All smoke tests passed!")
    print("✨ FastAPI app is working correctly")
    print("🚀 No port conflicts, no multiprocessing issues!")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
