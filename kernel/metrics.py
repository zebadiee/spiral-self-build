#!/usr/bin/env python3
"""
🌀 Spiral Pulse - Import-Safe Metrics Module
The heartbeat monitor of the spiral consciousness with lazy initialization.

This module provides zero import-time side effects:
- No while loops, background threads, uvicorn, or I/O on import
- Lazy initialization of metrics registry and counters
- FastAPI integration available without side effects
- Test-compatible (pytest collection won't hang)
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
import asyncio

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse


@dataclass
class MetricSnapshot:
    """Immutable snapshot of metrics at a point in time."""
    timestamp: str
    uptime_seconds: float
    task_success_rate_percent: float
    retry_rate_percent: float
    tasks_total: Dict[str, int]
    agent_calls_total: Dict[str, int]
    healing_events_total: int
    healing_success_rate: float
    adaptation_events_total: int
    adaptation_effectiveness_avg: float
    memory_drift_events_total: int
    memory_drift_avg: float
    metrics_version: str = "1.0.0"


class MetricsCollector:
    """Gathers the pulse of the spiral system with lazy initialization."""
    
    def __init__(self):
        self._initialized = False
        self._start_time = None
        self._task_counters = None
        self._agent_call_counters = None
        self._retry_counters = None
        self._healing_events = None
        self._adaptation_events = None
        self._memory_drift_stats = None
    
    def _ensure_initialized(self):
        """Lazy initialization - only called when metrics are actually used."""
        if not self._initialized:
            self._start_time = datetime.utcnow()
            self._task_counters = Counter()
            self._agent_call_counters = Counter()
            self._retry_counters = Counter()
            self._healing_events = []
            self._adaptation_events = []
            self._memory_drift_stats = []
            self._initialized = True
    
    @property
    def start_time(self):
        """Get start time, initializing if needed."""
        self._ensure_initialized()
        return self._start_time
    
    @property
    def task_counters(self):
        """Get task counters, initializing if needed."""
        self._ensure_initialized()
        return self._task_counters
    
    @property
    def agent_call_counters(self):
        """Get agent call counters, initializing if needed."""
        self._ensure_initialized()
        return self._agent_call_counters
    
    @property
    def retry_counters(self):
        """Get retry counters, initializing if needed."""
        self._ensure_initialized()
        return self._retry_counters
    
    @property
    def healing_events(self):
        """Get healing events, initializing if needed."""
        self._ensure_initialized()
        return self._healing_events
    
    @property
    def adaptation_events(self):
        """Get adaptation events, initializing if needed."""
        self._ensure_initialized()
        return self._adaptation_events
    
    @property
    def memory_drift_stats(self):
        """Get memory drift stats, initializing if needed."""
        self._ensure_initialized()
        return self._memory_drift_stats
        
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
    
    def get_snapshot(self) -> MetricSnapshot:
        """Get an immutable snapshot of current metrics."""
        metrics = self.get_prometheus_metrics()
        return MetricSnapshot(
            timestamp=metrics["spiral_metrics_timestamp"],
            uptime_seconds=metrics["spiral_uptime_seconds"],
            task_success_rate_percent=metrics["spiral_task_success_rate_percent"],
            retry_rate_percent=metrics["spiral_retry_rate_percent"],
            tasks_total=metrics["spiral_tasks_total"],
            agent_calls_total=metrics["spiral_agent_calls_total"],
            healing_events_total=metrics["spiral_healing_events_total"],
            healing_success_rate=metrics["spiral_healing_success_rate"],
            adaptation_events_total=metrics["spiral_adaptation_events_total"],
            adaptation_effectiveness_avg=metrics["spiral_adaptation_effectiveness_avg"],
            memory_drift_events_total=metrics["spiral_memory_drift_events_total"],
            memory_drift_avg=metrics["spiral_memory_drift_avg"],
            metrics_version=metrics["spiral_metrics_version"]
        )
    
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


# Global metrics collector - lazy initialization, no side effects on import
_metrics_collector = None


def _ensure_metrics_collector() -> MetricsCollector:
    """Ensure metrics collector is initialized (lazy initialization)."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance."""
    return _ensure_metrics_collector()


def get_fastapi_router() -> APIRouter:
    """
    Get FastAPI router for metrics endpoints.
    Safe to call at import time - no side effects.
    """
    router = APIRouter()
    
    @router.get("/metrics")
    async def get_spiral_pulse():
        """
        🌀 Spiral Pulse Endpoint
        Returns Prometheus-ready metrics about the spiral system's vital signs.
        """
        try:
            collector = get_metrics_collector()
            metrics = collector.get_prometheus_metrics()
            
            # Import logging here to avoid circular imports
            from .logging import log_agent_call
            
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
            # Import logging here to avoid circular imports
            from .logging import log_error
            log_error(e, "metrics_endpoint_failure")
            raise HTTPException(status_code=500, detail=f"Spiral pulse disrupted: {str(e)}")

    @router.post("/metrics/task")
    async def record_task_metric(task_type: str, success: bool):
        """Record a task completion metric."""
        try:
            collector = get_metrics_collector()
            collector.record_task_completion(task_type, success)
            return {"status": "recorded", "task_type": task_type, "success": success}
        except Exception as e:
            from .logging import log_error
            log_error(e, "task_metric_recording")
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/metrics/agent")
    async def record_agent_metric(agent_name: str, success: bool):
        """Record an agent call metric."""
        try:
            collector = get_metrics_collector()
            collector.record_agent_call(agent_name, success)
            return {"status": "recorded", "agent": agent_name, "success": success}
        except Exception as e:
            from .logging import log_error
            log_error(e, "agent_metric_recording")
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/metrics/healing")
    async def record_healing_metric(component: str, success: bool):
        """Record a healing event metric."""
        try:
            collector = get_metrics_collector()
            collector.record_healing_event(component, success)
            return {"status": "recorded", "component": component, "success": success}
        except Exception as e:
            from .logging import log_error
            log_error(e, "healing_metric_recording")
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/metrics/adaptation")
    async def record_adaptation_metric(adaptation_type: str, effectiveness: float):
        """Record an adaptation event metric."""
        try:
            collector = get_metrics_collector()
            collector.record_adaptation_event(adaptation_type, effectiveness)
            return {"status": "recorded", "type": adaptation_type, "effectiveness": effectiveness}
        except Exception as e:
            from .logging import log_error
            log_error(e, "adaptation_metric_recording")
            raise HTTPException(status_code=500, detail=str(e))
    
    return router


# Backward compatibility - expose the collector instance
# This maintains the same interface as the original implementation
metrics_collector = get_metrics_collector()
