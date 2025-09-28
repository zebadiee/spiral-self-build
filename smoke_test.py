#!/usr/bin/env python3
"""
Smoke test for the /metrics endpoint
"""

import requests
import time
import subprocess
import sys
import signal
import os
from pathlib import Path

def test_metrics_endpoint():
    """Test the /metrics endpoint returns correct Prometheus format"""
    
    # Start the FastAPI server in background
    print("Starting FastAPI server...")
    server_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "fastapi_app:app", 
        "--host", "0.0.0.0", "--port", "8000"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        # Wait for server to start
        time.sleep(3)
        
        # Test root endpoint
        print("Testing root endpoint...")
        response = requests.get("http://localhost:8000/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Spiral Self-Build API"
        assert data["status"] == "running"
        print("✓ Root endpoint working")
        
        # Test metrics endpoint
        print("Testing /metrics endpoint...")
        response = requests.get("http://localhost:8000/metrics")
        assert response.status_code == 200
        
        # Check content type is plain text
        assert "text/plain" in response.headers.get("content-type", "")
        
        # Check metrics content
        metrics_text = response.text
        print(f"Metrics response:\n{metrics_text}")
        
        # Verify expected metrics are present
        assert "# HELP http_requests_total Total HTTP requests" in metrics_text
        assert "# TYPE http_requests_total counter" in metrics_text
        assert "http_requests_total 42" in metrics_text
        assert "# HELP app_info Application info" in metrics_text
        assert "# TYPE app_info gauge" in metrics_text
        assert 'app_info{version="1.0"} 1' in metrics_text
        
        print("✓ /metrics endpoint working correctly")
        print("✓ Prometheus format validated")
        print("✓ All smoke tests passed!")
        
        return True
        
    except Exception as e:
        print(f"✗ Smoke test failed: {e}")
        return False
        
    finally:
        # Clean up server process
        print("Stopping server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()

if __name__ == "__main__":
    success = test_metrics_endpoint()
    sys.exit(0 if success else 1)
