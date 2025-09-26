
#!/usr/bin/env python3
"""
MCP Simple Learning Server
Core server for self-learning assistant operations with REST endpoints.
"""

import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data models
class LearnRequest(BaseModel):
    content: str
    source: str = "manual"
    metadata: Dict[str, Any] = {}

class InsightResponse(BaseModel):
    insights: List[str]
    confidence: float
    timestamp: str
    source: str

# Initialize FastAPI app
app = FastAPI(
    title="MCP Learning Server",
    description="Self-Learning Assistant Core Server",
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

# In-memory storage (replace with database in production)
learning_data = {
    "sessions": [],
    "insights": [],
    "metrics": {
        "total_sessions": 0,
        "total_insights": 0,
        "last_activity": None
    }
}

@app.get("/")
async def root():
    """Root endpoint with server info."""
    return {
        "name": "MCP Learning Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": ["/status", "/learn", "/insights", "/metrics"]
    }

@app.get("/status")
async def get_status():
    """Health check and server status."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running",
        "learning_sessions": len(learning_data["sessions"]),
        "total_insights": len(learning_data["insights"])
    }

@app.post("/learn", response_model=InsightResponse)
async def learn_from_content(request: LearnRequest):
    """Process content and generate insights."""
    try:
        # Simulate learning process (replace with actual ML/AI logic)
        insights = await generate_insights(request.content)
        
        # Store learning session
        session = {
            "id": len(learning_data["sessions"]) + 1,
            "content_preview": request.content[:100] + "..." if len(request.content) > 100 else request.content,
            "source": request.source,
            "insights": insights,
            "timestamp": datetime.now().isoformat(),
            "metadata": request.metadata
        }
        
        learning_data["sessions"].append(session)
        learning_data["insights"].extend(insights)
        learning_data["metrics"]["total_sessions"] += 1
        learning_data["metrics"]["total_insights"] += len(insights)
        learning_data["metrics"]["last_activity"] = datetime.now().isoformat()
        
        logger.info(f"Processed learning session {session['id']} with {len(insights)} insights")
        
        return InsightResponse(
            insights=insights,
            confidence=0.85,  # Simulated confidence score
            timestamp=session["timestamp"],
            source=request.source
        )
        
    except Exception as e:
        logger.error(f"Learning error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Learning failed: {str(e)}")

@app.get("/insights")
async def get_insights(limit: int = 10):
    """Retrieve recent insights."""
    recent_insights = learning_data["insights"][-limit:]
    return {
        "insights": recent_insights,
        "total_count": len(learning_data["insights"]),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics")
async def get_metrics():
    """Get learning metrics and statistics."""
    return {
        "metrics": learning_data["metrics"],
        "session_count": len(learning_data["sessions"]),
        "insight_count": len(learning_data["insights"]),
        "timestamp": datetime.now().isoformat()
    }

async def generate_insights(content: str) -> List[str]:
    """
    Generate insights from content (simplified version).
    In production, this would use advanced NLP/ML models.
    """
    # Simulate processing time
    await asyncio.sleep(0.1)
    
    # Simple insight generation based on content analysis
    insights = []
    
    # Length-based insight
    if len(content) > 500:
        insights.append("This is a substantial piece of content with rich information density.")
    else:
        insights.append("This is a concise piece of content suitable for quick processing.")
    
    # Keyword-based insights
    keywords = ["learn", "AI", "data", "process", "system", "model", "analysis"]
    found_keywords = [kw for kw in keywords if kw.lower() in content.lower()]
    if found_keywords:
        insights.append(f"Content focuses on technical concepts: {', '.join(found_keywords[:3])}")
    
    # Structure insight
    if "\n" in content:
        insights.append("Content has structured formatting with multiple sections.")
    else:
        insights.append("Content is presented as continuous text.")
    
    return insights[:3]  # Return top 3 insights

if __name__ == "__main__":
    print("🚀 Starting MCP Learning Server...")
    print("📊 Dashboard: http://localhost:8000")
    print("📋 Status: http://localhost:8000/status")
    print("🔍 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "mcp_simple_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
