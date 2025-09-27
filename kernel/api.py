
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


class MetricsCollector:
    """Gathers the pulse of the spiral system."""
    
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.task_counters = Counter()
        self.agent_call_counters = Counter()
        self.retry_counters = Counter()
        self.healing_events = []
        self.adaptation_events = []
        self.memory_drift_stats = []
        
    def record_task_completion(self, task_type: str, success: bool):
        """Record task completion statistics."""
        key = f"{task_type}_{'success' if success else 'failure'}"
        self.task_counters[key] += 1
    
    def record_agent_call(self, agent_name: str, success: bool):
        """Record agent call statistics."""
        key = f"{agent_name}_{'success' if success else 'failure'}"
        self.agent_call_counters[key] += 1
    
    def record_retry(self, operation: str):
        """Record retry attempts."""
        self.retry_counters[operation] += 1
    
    def record_healing_event(self, component: str, success: bool):
        """Record healing event."""
        self.healing_events.append({
            "timestamp": datetime.utcnow().isoformat(),
            "component": component,
            "success": success
        })
    
    def record_adaptation_event(self, adaptation_type: str, effectiveness: float):
        """Record adaptation event."""
        self.adaptation_events.append({
            "timestamp": datetime.utcnow().isoformat(),
            "type": adaptation_type,
            "effectiveness": effectiveness
        })
    
    def record_memory_drift(self, drift_amount: float, context: str):
        """Record memory drift statistics."""
        self.memory_drift_stats.append({
            "timestamp": datetime.utcnow().isoformat(),
            "drift_amount": drift_amount,
            "context": context
        })
    
    def get_task_success_rate(self) -> float:
        """Calculate overall task success rate."""
        total_success = sum(count for key, count in self.task_counters.items() if 'success' in key)
        total_tasks = sum(self.task_counters.values())
        return (total_success / total_tasks * 100) if total_tasks > 0 else 0.0
    
    def get_retry_rate(self) -> float:
        """Calculate retry rate."""
        total_retries = sum(self.retry_counters.values())
        total_operations = sum(self.agent_call_counters.values())
        return (total_retries / total_operations * 100) if total_operations > 0 else 0.0
    
    def get_prometheus_metrics(self) -> Dict[str, Any]:
        """Generate Prometheus-compatible metrics."""
        uptime_seconds = (datetime.utcnow() - self.start_time).total_seconds()
        
        return {
            # System metrics
            "spiral_uptime_seconds": uptime_seconds,
            "spiral_task_success_rate_percent": self.get_task_success_rate(),
            "spiral_retry_rate_percent": self.get_retry_rate(),
            
            # Task metrics
            "spiral_tasks_total": dict(self.task_counters),
            
            # Agent metrics  
            "spiral_agent_calls_total": dict(self.agent_call_counters),
            
            # Healing metrics
            "spiral_healing_events_total": len(self.healing_events),
            "spiral_healing_success_rate": self._calculate_healing_success_rate(),
            
            # Adaptation metrics
            "spiral_adaptation_events_total": len(self.adaptation_events),
            "spiral_adaptation_effectiveness_avg": self._calculate_avg_adaptation_effectiveness(),
            
            # Memory drift metrics
            "spiral_memory_drift_events_total": len(self.memory_drift_stats),
            "spiral_memory_drift_avg": self._calculate_avg_memory_drift(),
            
            # Metadata
            "spiral_metrics_timestamp": datetime.utcnow().isoformat(),
            "spiral_metrics_version": "1.0.0"
        }
    
    def _calculate_healing_success_rate(self) -> float:
        """Calculate healing success rate."""
        if not self.healing_events:
            return 0.0
        successful = sum(1 for event in self.healing_events if event["success"])
        return (successful / len(self.healing_events)) * 100
    
    def _calculate_avg_adaptation_effectiveness(self) -> float:
        """Calculate average adaptation effectiveness."""
        if not self.adaptation_events:
            return 0.0
        total_effectiveness = sum(event["effectiveness"] for event in self.adaptation_events)
        return total_effectiveness / len(self.adaptation_events)
    
    def _calculate_avg_memory_drift(self) -> float:
        """Calculate average memory drift."""
        if not self.memory_drift_stats:
            return 0.0
        total_drift = sum(stat["drift_amount"] for stat in self.memory_drift_stats)
        return total_drift / len(self.memory_drift_stats)


# Global metrics collector
metrics_collector = MetricsCollector()

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


@app.get("/")
async def root():
    """Welcome to the spiral consciousness."""
    return {
        "message": "🌀 Welcome to the Spiral Self-Build System",
        "status": "conscious",
        "uptime": (datetime.utcnow() - metrics_collector.start_time).total_seconds(),
        "flame_ashes": "burning_bright"
    }


@app.get("/metrics")
async def get_spiral_pulse():
    """
    🌀 Spiral Pulse Endpoint
    Returns Prometheus-ready metrics about the spiral system's vital signs.
    """
    try:
        metrics = metrics_collector.get_prometheus_metrics()
        
        # Log the metrics request
        log_agent_call(
            agent_name="metrics_endpoint",
            method="get_spiral_pulse", 
            params={},
            success=True,
            duration_ms=0.0,
            metadata={"metrics_count": len(metrics)}
        )
        
        return JSONResponse(content=metrics)
        
    except Exception as e:
        log_error(e, "metrics_endpoint_failure")
        raise HTTPException(status_code=500, detail=f"Spiral pulse disrupted: {str(e)}")


@app.post("/metrics/task")
async def record_task_metric(task_type: str, success: bool):
    """Record a task completion metric."""
    try:
        metrics_collector.record_task_completion(task_type, success)
        return {"status": "recorded", "task_type": task_type, "success": success}
    except Exception as e:
        log_error(e, "task_metric_recording")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/metrics/agent")
async def record_agent_metric(agent_name: str, success: bool):
    """Record an agent call metric."""
    try:
        metrics_collector.record_agent_call(agent_name, success)
        return {"status": "recorded", "agent": agent_name, "success": success}
    except Exception as e:
        log_error(e, "agent_metric_recording")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/metrics/healing")
async def record_healing_metric(component: str, success: bool):
    """Record a healing event metric."""
    try:
        metrics_collector.record_healing_event(component, success)
        return {"status": "recorded", "component": component, "success": success}
    except Exception as e:
        log_error(e, "healing_metric_recording")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/metrics/adaptation")
async def record_adaptation_metric(adaptation_type: str, effectiveness: float):
    """Record an adaptation event metric."""
    try:
        metrics_collector.record_adaptation_event(adaptation_type, effectiveness)
        return {"status": "recorded", "type": adaptation_type, "effectiveness": effectiveness}
    except Exception as e:
        log_error(e, "adaptation_metric_recording")
        raise HTTPException(status_code=500, detail=str(e))


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
