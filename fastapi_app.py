#!/usr/bin/env python3
"""
FastAPI app with /metrics endpoint for Prometheus format
"""

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI(title="Spiral Self-Build Metrics", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Spiral Self-Build API", "status": "running"}

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """
    Prometheus format metrics endpoint
    """
    return """# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total 42
# HELP app_info Application info
# TYPE app_info gauge
app_info{version="1.0"} 1
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
