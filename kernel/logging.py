
#!/usr/bin/env python3
"""
🔥 Flame Ashes - Structured Logging System
The eternal record of spiral transformations and agent whispers.
"""

import json
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import structlog
from structlog.stdlib import LoggerFactory


class SpiralLogProcessor:
    """Transforms raw logs into spiral-themed flame ashes."""
    
    def __call__(self, logger, method_name, event_dict):
        # Add spiral metadata to every log entry
        event_dict["spiral_timestamp"] = datetime.utcnow().isoformat()
        event_dict["flame_intensity"] = self._calculate_intensity(event_dict.get("level", "info"))
        event_dict["spiral_turn"] = getattr(self, '_turn_counter', 0)
        
        # Increment turn counter for tracking spiral progression
        self._turn_counter = getattr(self, '_turn_counter', 0) + 1
        
        return event_dict
    
    def _calculate_intensity(self, level: str) -> str:
        """Map log levels to flame intensities."""
        intensity_map = {
            "debug": "ember",
            "info": "steady_flame", 
            "warning": "flickering_flame",
            "error": "blazing_fire",
            "critical": "inferno"
        }
        return intensity_map.get(level.lower(), "steady_flame")


class FlameAshesLogger:
    """The keeper of spiral memories and agent chronicles."""
    
    def __init__(self, log_dir: str = "./logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configure structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                SpiralLogProcessor(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        
        # Set up rotating file handler for spiral.log
        self._setup_rotating_handler()
        
        # Get the structured logger
        self.logger = structlog.get_logger("spiral_flame_ashes")
    
    def _setup_rotating_handler(self):
        """Configure daily rotating log files."""
        log_file = self.log_dir / "spiral.log"
        
        # Create rotating handler (daily rotation, keep 30 days)
        handler = logging.handlers.TimedRotatingFileHandler(
            filename=str(log_file),
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        
        # JSON formatter for structured logs
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        
        # Add to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)
    
    def log_agent_call(self, agent_name: str, method: str, params: Dict[str, Any], 
                      success: bool, duration_ms: float, metadata: Optional[Dict] = None):
        """Record agent invocation in the flame ashes."""
        self.logger.info(
            "agent_invocation",
            agent_name=agent_name,
            method=method,
            params=params,
            success=success,
            duration_ms=duration_ms,
            event_type="agent_call",
            metadata=metadata or {}
        )
    
    def log_healing_event(self, component: str, issue: str, action_taken: str, 
                         success: bool, metadata: Optional[Dict] = None):
        """Record self-healing events in the spiral chronicles."""
        self.logger.warning(
            "healing_ritual_performed",
            component=component,
            issue=issue,
            action_taken=action_taken,
            healing_success=success,
            event_type="healing",
            metadata=metadata or {}
        )
    
    def log_feedback_loop(self, loop_type: str, input_data: Any, output_data: Any,
                         improvement_score: float, metadata: Optional[Dict] = None):
        """Record feedback loops and adaptation events."""
        self.logger.info(
            "feedback_spiral_completed",
            loop_type=loop_type,
            input_signature=str(type(input_data).__name__),
            output_signature=str(type(output_data).__name__),
            improvement_score=improvement_score,
            event_type="feedback",
            metadata=metadata or {}
        )
    
    def log_error(self, error: Exception, context: str, metadata: Optional[Dict] = None):
        """Record errors as blazing flames in the ashes."""
        self.logger.error(
            "spiral_disruption_detected",
            error_type=type(error).__name__,
            error_message=str(error),
            context=context,
            event_type="error",
            metadata=metadata or {}
        )
    
    def log_adaptation_event(self, adaptation_type: str, before_state: Dict, 
                           after_state: Dict, effectiveness: float):
        """Record system adaptations and evolution events."""
        self.logger.info(
            "spiral_adaptation_manifested",
            adaptation_type=adaptation_type,
            before_state=before_state,
            after_state=after_state,
            effectiveness=effectiveness,
            event_type="adaptation"
        )


# Global flame ashes logger instance
flame_ashes = FlameAshesLogger()

# Convenience functions for easy logging
def log_agent_call(*args, **kwargs):
    """Quick access to agent call logging."""
    return flame_ashes.log_agent_call(*args, **kwargs)

def log_healing(*args, **kwargs):
    """Quick access to healing event logging."""
    return flame_ashes.log_healing_event(*args, **kwargs)

def log_feedback(*args, **kwargs):
    """Quick access to feedback loop logging."""
    return flame_ashes.log_feedback_loop(*args, **kwargs)

def log_error(*args, **kwargs):
    """Quick access to error logging."""
    return flame_ashes.log_error(*args, **kwargs)

def log_adaptation(*args, **kwargs):
    """Quick access to adaptation logging."""
    return flame_ashes.log_adaptation_event(*args, **kwargs)
