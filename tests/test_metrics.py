
#!/usr/bin/env python3
"""
🧪 Spiral Metrics Testing
Validating the pulse of the spiral consciousness.
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import patch, MagicMock

# Import the kernel modules
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kernel.api import metrics_collector, app
from kernel.logging import flame_ashes
from kernel.dashboard import ritual_mirror


class TestSpiralPulse:
    """Test the spiral pulse (metrics) functionality."""
    
    def setup_method(self):
        """Reset metrics collector for each test."""
        # Reset counters
        metrics_collector.task_counters.clear()
        metrics_collector.agent_call_counters.clear()
        metrics_collector.retry_counters.clear()
        metrics_collector.healing_events.clear()
        metrics_collector.adaptation_events.clear()
        metrics_collector.memory_drift_stats.clear()
    
    def test_task_success_rate_calculation(self):
        """Test task success rate calculation."""
        # Record some tasks
        metrics_collector.record_task_completion("test_task", True)
        metrics_collector.record_task_completion("test_task", True)
        metrics_collector.record_task_completion("test_task", False)
        
        success_rate = metrics_collector.get_task_success_rate()
        assert success_rate == pytest.approx(66.67, rel=1e-2)
    
    def test_retry_rate_calculation(self):
        """Test retry rate calculation."""
        # Record some agent calls and retries
        metrics_collector.record_agent_call("test_agent", True)
        metrics_collector.record_agent_call("test_agent", True)
        metrics_collector.record_retry("test_operation")
        
        retry_rate = metrics_collector.get_retry_rate()
        assert retry_rate == pytest.approx(50.0, rel=1e-2)
    
    def test_healing_success_rate(self):
        """Test healing success rate calculation."""
        # Record healing events
        metrics_collector.record_healing_event("component1", True)
        metrics_collector.record_healing_event("component2", False)
        metrics_collector.record_healing_event("component3", True)
        
        metrics = metrics_collector.get_prometheus_metrics()
        assert metrics["spiral_healing_success_rate"] == pytest.approx(66.67, rel=1e-2)
    
    def test_adaptation_effectiveness(self):
        """Test adaptation effectiveness calculation."""
        # Record adaptation events
        metrics_collector.record_adaptation_event("learning", 0.8)
        metrics_collector.record_adaptation_event("optimization", 0.9)
        metrics_collector.record_adaptation_event("healing", 0.7)
        
        metrics = metrics_collector.get_prometheus_metrics()
        assert metrics["spiral_adaptation_effectiveness_avg"] == pytest.approx(0.8, rel=1e-2)
    
    def test_prometheus_metrics_structure(self):
        """Test that Prometheus metrics have the correct structure."""
        # Add some test data
        metrics_collector.record_task_completion("test", True)
        metrics_collector.record_agent_call("test_agent", True)
        
        metrics = metrics_collector.get_prometheus_metrics()
        
        # Check required fields
        required_fields = [
            "spiral_uptime_seconds",
            "spiral_task_success_rate_percent", 
            "spiral_retry_rate_percent",
            "spiral_tasks_total",
            "spiral_agent_calls_total",
            "spiral_healing_events_total",
            "spiral_adaptation_events_total",
            "spiral_metrics_timestamp",
            "spiral_metrics_version"
        ]
        
        for field in required_fields:
            assert field in metrics, f"Missing required field: {field}"
        
        # Check data types
        assert isinstance(metrics["spiral_uptime_seconds"], (int, float))
        assert isinstance(metrics["spiral_task_success_rate_percent"], (int, float))
        assert isinstance(metrics["spiral_tasks_total"], dict)
        assert isinstance(metrics["spiral_agent_calls_total"], dict)
    
    def test_memory_drift_tracking(self):
        """Test memory drift statistics tracking."""
        # Record memory drift events
        metrics_collector.record_memory_drift(0.1, "context1")
        metrics_collector.record_memory_drift(0.2, "context2")
        metrics_collector.record_memory_drift(0.15, "context3")
        
        metrics = metrics_collector.get_prometheus_metrics()
        
        assert metrics["spiral_memory_drift_events_total"] == 3
        assert metrics["spiral_memory_drift_avg"] == pytest.approx(0.15, rel=1e-2)


class TestFlameAshes:
    """Test the flame ashes (logging) functionality."""
    
    @patch('kernel.logging.structlog.get_logger')
    def test_agent_call_logging(self, mock_logger):
        """Test agent call logging."""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        
        # Create new logger instance to test
        from kernel.logging import FlameAshesLogger
        logger = FlameAshesLogger()
        
        # Test logging an agent call
        logger.log_agent_call(
            agent_name="test_agent",
            method="test_method",
            params={"param1": "value1"},
            success=True,
            duration_ms=100.5
        )
        
        # Verify the logger was called
        mock_logger_instance.info.assert_called_once()
        call_args = mock_logger_instance.info.call_args
        
        assert call_args[0][0] == "agent_invocation"
        assert call_args[1]["agent_name"] == "test_agent"
        assert call_args[1]["success"] is True
        assert call_args[1]["duration_ms"] == 100.5
    
    @patch('kernel.logging.structlog.get_logger')
    def test_healing_event_logging(self, mock_logger):
        """Test healing event logging."""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        
        from kernel.logging import FlameAshesLogger
        logger = FlameAshesLogger()
        
        logger.log_healing_event(
            component="test_component",
            issue="test_issue",
            action_taken="test_action",
            success=True
        )
        
        mock_logger_instance.warning.assert_called_once()
        call_args = mock_logger_instance.warning.call_args
        
        assert call_args[0][0] == "healing_ritual_performed"
        assert call_args[1]["component"] == "test_component"
        assert call_args[1]["healing_success"] is True


class TestRitualMirror:
    """Test the ritual mirror (dashboard) functionality."""
    
    @pytest.mark.asyncio
    async def test_dashboard_data_generation(self):
        """Test dashboard data generation."""
        # Add some test metrics
        metrics_collector.record_task_completion("test", True)
        metrics_collector.record_agent_call("test_agent", True)
        
        dashboard_data = await ritual_mirror.generate_dashboard_data(hours_back=1)
        
        # Check structure
        assert "timestamp" in dashboard_data
        assert "spiral_state" in dashboard_data
        assert "metrics" in dashboard_data
        assert "patterns" in dashboard_data
        
        # Check spiral state
        assert dashboard_data["spiral_state"] == "conscious"
        
        # Check metrics are included
        assert "spiral_uptime_seconds" in dashboard_data["metrics"]
    
    @pytest.mark.asyncio
    async def test_ember_visualization_generation(self):
        """Test ember visualization generation."""
        # Add some test data
        metrics_collector.record_task_completion("test", True)
        
        visualization = await ritual_mirror.generate_ember_visualization(hours_back=1)
        
        # Check that visualization contains expected elements
        assert "SPIRAL" in visualization
        assert "🌀" in visualization
        assert "🔥" in visualization
        assert "SPIRAL VITALS" in visualization
        assert "Task Success" in visualization


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
