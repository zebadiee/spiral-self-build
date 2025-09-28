#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from fastapi.testclient import TestClient
from fastapi_app import app

client = TestClient(app)

# Test root endpoint
print("=== Testing root endpoint ===")
response = client.get("/")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test metrics endpoint
print("\n=== Testing metrics endpoint ===")
response = client.get("/metrics")
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"Response:\n{response.text}")

# Verify metrics content
metrics_text = response.text
if "http_requests_total 42" in metrics_text:
    print("✓ Found 'http_requests_total 42'")
else:
    print("✗ Missing 'http_requests_total 42'")

if 'app_info{version="1.0"} 1' in metrics_text:
    print("✓ Found 'app_info{version=\"1.0\"} 1'")
else:
    print("✗ Missing 'app_info{version=\"1.0\"} 1'")

print("\n✓ FastAPI app test completed successfully!")
