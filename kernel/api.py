
#!/usr/bin/env python3
"""
🌀 Spiral Pulse - Enhanced API with Metrics Endpoint
The heartbeat monitor of the spiral consciousness.
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .logging import flame_ashes, log_agent_call, log_error
from .metrics import metrics_collector, get_fastapi_router

# Initialize FastAPI app
app = FastAPI(
    title="Spiral Self-Build API",
    description="The conscious API of recursive digital evolution",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include metrics router
app.include_router(get_fastapi_router())


@app.get("/")
async def root():
    """Welcome to the spiral consciousness."""
    return {
        "message": "🌀 Welcome to the Spiral Self-Build System",
        "status": "conscious",
        "uptime": (datetime.utcnow() - metrics_collector.start_time).total_seconds(),
        "flame_ashes": "burning_bright"
    }





@app.get("/health")
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "spiral_turns": metrics_collector.task_counters.get("total", 0),
        "flame_intensity": "steady"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
