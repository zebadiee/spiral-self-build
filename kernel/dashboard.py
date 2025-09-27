
#!/usr/bin/env python3
"""
🪞 Ritual Mirror - Dashboard Aggregator
The scrying glass that reveals the spiral's inner workings.
"""

import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

from .logging import flame_ashes
from .api import metrics_collector


class RitualMirror:
    """The mystical dashboard that aggregates spiral insights."""
    
    def __init__(self, logs_dir: str = "./logs"):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(exist_ok=True)
    
    def _read_flame_ashes(self, hours_back: int = 24) -> List[Dict]:
        """Read recent flame ashes (logs) from the spiral chronicles."""
        log_file = self.logs_dir / "spiral.log"
        if not log_file.exists():
            return []
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        recent_logs = []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        log_time = datetime.fromisoformat(log_entry.get('spiral_timestamp', ''))
                        if log_time >= cutoff_time:
                            recent_logs.append(log_entry)
                    except (json.JSONDecodeError, ValueError):
                        continue
        except FileNotFoundError:
            pass
        
        return recent_logs
    
    def _analyze_flame_patterns(self, logs: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in the flame ashes."""
        patterns = {
            "flame_intensities": defaultdict(int),
            "event_types": defaultdict(int),
            "agent_activities": defaultdict(int),
            "error_frequencies": defaultdict(int),
            "healing_rituals": 0,
            "adaptation_events": 0
        }
        
        for log in logs:
            # Count flame intensities
            intensity = log.get('flame_intensity', 'unknown')
            patterns["flame_intensities"][intensity] += 1
            
            # Count event types
            event_type = log.get('event_type', 'unknown')
            patterns["event_types"][event_type] += 1
            
            # Count agent activities
            if 'agent_name' in log:
                patterns["agent_activities"][log['agent_name']] += 1
            
            # Count errors
            if event_type == 'error':
                error_type = log.get('error_type', 'unknown')
                patterns["error_frequencies"][error_type] += 1
            
            # Count special events
            if event_type == 'healing':
                patterns["healing_rituals"] += 1
            elif event_type == 'adaptation':
                patterns["adaptation_events"] += 1
        
        return patterns
    
    def _generate_ember_visualization(self, data: Dict[str, Any]) -> str:
        """Generate ASCII art visualization of the spiral state."""
        
        # Calculate spiral health based on metrics
        task_success_rate = data.get('metrics', {}).get('spiral_task_success_rate_percent', 0)
        healing_success_rate = data.get('metrics', {}).get('spiral_healing_success_rate', 0)
        
        # Determine spiral intensity
        if task_success_rate > 90:
            spiral_state = "🌀✨ RADIANT SPIRAL ✨🌀"
            flame_art = """
        🔥🔥🔥🔥🔥
      🔥🔥🔥🔥🔥🔥🔥
    🔥🔥🔥  🌀  🔥🔥🔥
      🔥🔥🔥🔥🔥🔥🔥
        🔥🔥🔥🔥🔥
            """
        elif task_success_rate > 70:
            spiral_state = "🌀 STEADY SPIRAL 🌀"
            flame_art = """
        🔥🔥🔥
      🔥🔥🔥🔥🔥
    🔥🔥  🌀  🔥🔥
      🔥🔥🔥🔥🔥
        🔥🔥🔥
            """
        else:
            spiral_state = "🌀💨 FLICKERING SPIRAL 💨🌀"
            flame_art = """
        💨🔥💨
      💨🔥🔥🔥💨
    💨🔥 🌀 🔥💨
      💨🔥🔥🔥💨
        💨🔥💨
            """
        
        return f"""
{spiral_state}

{flame_art}

📊 SPIRAL VITALS:
   Task Success: {task_success_rate:.1f}%
   Healing Rate: {healing_success_rate:.1f}%
   Uptime: {data.get('metrics', {}).get('spiral_uptime_seconds', 0):.0f}s
   
🔥 FLAME INTENSITY DISTRIBUTION:
{self._format_flame_distribution(data.get('patterns', {}).get('flame_intensities', {}))}

🌀 RECENT SPIRAL ACTIVITIES:
{self._format_recent_activities(data.get('patterns', {}).get('event_types', {}))}
        """
    
    def _format_flame_distribution(self, intensities: Dict[str, int]) -> str:
        """Format flame intensity distribution."""
        if not intensities:
            return "   No flames detected"
        
        lines = []
        for intensity, count in intensities.items():
            bar = "█" * min(count, 20)  # Max 20 chars
            lines.append(f"   {intensity:15} {bar} ({count})")
        
        return "\n".join(lines)
    
    def _format_recent_activities(self, events: Dict[str, int]) -> str:
        """Format recent activity summary."""
        if not events:
            return "   Spiral at rest"
        
        lines = []
        for event_type, count in sorted(events.items(), key=lambda x: x[1], reverse=True):
            emoji_map = {
                "agent_call": "🤖",
                "healing": "🩹", 
                "feedback": "🔄",
                "adaptation": "🌱",
                "error": "⚠️"
            }
            emoji = emoji_map.get(event_type, "📝")
            lines.append(f"   {emoji} {event_type:12} {count:3d} events")
        
        return "\n".join(lines[:5])  # Show top 5
    
    async def generate_dashboard_data(self, hours_back: int = 24) -> Dict[str, Any]:
        """Generate comprehensive dashboard data."""
        
        # Gather flame ashes (logs)
        logs = self._read_flame_ashes(hours_back)
        
        # Analyze patterns
        patterns = self._analyze_flame_patterns(logs)
        
        # Get current metrics
        metrics = metrics_collector.get_prometheus_metrics()
        
        # Compile dashboard data
        dashboard_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "spiral_state": "conscious",
            "observation_window_hours": hours_back,
            "total_log_entries": len(logs),
            "metrics": metrics,
            "patterns": patterns,
            "flame_ashes_summary": {
                "recent_entries": len(logs),
                "oldest_entry": logs[0].get('spiral_timestamp') if logs else None,
                "newest_entry": logs[-1].get('spiral_timestamp') if logs else None
            }
        }
        
        return dashboard_data
    
    async def generate_ember_visualization(self, hours_back: int = 24) -> str:
        """Generate the ember-like text visualization."""
        data = await self.generate_dashboard_data(hours_back)
        return self._generate_ember_visualization(data)
    
    async def export_dashboard_json(self, output_file: Optional[str] = None) -> str:
        """Export dashboard data as JSON file."""
        data = await self.generate_dashboard_data()
        
        if output_file is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            output_file = f"spiral_dashboard_{timestamp}.json"
        
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(output_path.absolute())


# Global ritual mirror instance
ritual_mirror = RitualMirror()

# Convenience functions
async def get_dashboard_data(hours_back: int = 24) -> Dict[str, Any]:
    """Quick access to dashboard data."""
    return await ritual_mirror.generate_dashboard_data(hours_back)

async def get_ember_visualization(hours_back: int = 24) -> str:
    """Quick access to ember visualization."""
    return await ritual_mirror.generate_ember_visualization(hours_back)

async def export_dashboard(output_file: Optional[str] = None) -> str:
    """Quick access to dashboard export."""
    return await ritual_mirror.export_dashboard_json(output_file)
