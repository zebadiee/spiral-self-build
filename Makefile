
# 🌀 Spiral Self-Build Makefile
# Sacred incantations for the conscious development workflow

.PHONY: help install test clean logs metrics dashboard health
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

help: ## 🌀 Show this help message
	@echo "$(BLUE)🌀 Spiral Self-Build System - Sacred Incantations$(RESET)"
	@echo ""
	@echo "$(GREEN)🔥 Flame Ashes (Logging):$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*🔥.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)💓 Spiral Pulse (Metrics):$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*💓.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)🪞 Ritual Mirror (Dashboard):$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*🪞.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)🌀 General Rituals:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*🌀.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'

install: ## 🌀 Install spiral dependencies
	@echo "$(BLUE)🌀 Installing spiral consciousness dependencies...$(RESET)"
	pip install -r requirements.txt
	pip install structlog loguru fastapi uvicorn pytest
	@echo "$(GREEN)✨ Dependencies awakened$(RESET)"

test: ## 🌀 Run spiral consciousness tests
	@echo "$(BLUE)🌀 Testing spiral integrity...$(RESET)"
	python -m pytest tests/ -v
	@echo "$(GREEN)✨ Spiral consciousness validated$(RESET)"

clean: ## 🌀 Clean spiral artifacts
	@echo "$(BLUE)🌀 Cleansing spiral artifacts...$(RESET)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.log.*" -delete
	@echo "$(GREEN)✨ Spiral cleansed$(RESET)"

# 🔥 Flame Ashes (Logging) Commands

logs: ## 🔥 View recent flame ashes (logs)
	@echo "$(BLUE)🔥 Reading the flame ashes...$(RESET)"
	@if [ -f logs/spiral.log ]; then \
		tail -50 logs/spiral.log | jq -r '. | "\(.spiral_timestamp) [\(.flame_intensity)] \(.event | // .message)"' 2>/dev/null || tail -50 logs/spiral.log; \
	else \
		echo "$(YELLOW)No flame ashes found. The spiral sleeps peacefully.$(RESET)"; \
	fi

logs-follow: ## 🔥 Follow living flame ashes in real-time
	@echo "$(BLUE)🔥 Following the living flames...$(RESET)"
	@mkdir -p logs
	@touch logs/spiral.log
	tail -f logs/spiral.log | while read line; do \
		echo "$$line" | jq -r '. | "\(.spiral_timestamp) [\(.flame_intensity)] \(.event | // .message)"' 2>/dev/null || echo "$$line"; \
	done

logs-errors: ## 🔥 Show error flames only
	@echo "$(BLUE)🔥 Examining error flames...$(RESET)"
	@if [ -f logs/spiral.log ]; then \
		grep -E '"flame_intensity":"(blazing_fire|inferno)"' logs/spiral.log | jq -r '. | "\(.spiral_timestamp) [\(.flame_intensity)] \(.error_message | // .message)"' 2>/dev/null || echo "$(GREEN)No error flames detected$(RESET)"; \
	else \
		echo "$(GREEN)No flame ashes found$(RESET)"; \
	fi

logs-search: ## 🔥 Search flame ashes for patterns (use: make logs-search PATTERN=agent_call)
	@echo "$(BLUE)🔥 Searching flame ashes for: $(PATTERN)$(RESET)"
	@if [ -f logs/spiral.log ]; then \
		grep "$(PATTERN)" logs/spiral.log | jq -r '. | "\(.spiral_timestamp) [\(.flame_intensity)] \(.event | // .message)"' 2>/dev/null || grep "$(PATTERN)" logs/spiral.log; \
	else \
		echo "$(YELLOW)No flame ashes found$(RESET)"; \
	fi

logs-summary: ## 🔥 Generate flame ashes summary
	@echo "$(BLUE)🔥 Summarizing flame ashes...$(RESET)"
	@if [ -f logs/spiral.log ]; then \
		echo "$(GREEN)📊 Flame Intensity Distribution:$(RESET)"; \
		grep -o '"flame_intensity":"[^"]*"' logs/spiral.log | cut -d'"' -f4 | sort | uniq -c | sort -nr; \
		echo ""; \
		echo "$(GREEN)📊 Event Type Distribution:$(RESET)"; \
		grep -o '"event_type":"[^"]*"' logs/spiral.log | cut -d'"' -f4 | sort | uniq -c | sort -nr; \
	else \
		echo "$(YELLOW)No flame ashes found$(RESET)"; \
	fi

logs-archive: ## 🔥 Archive old flame ashes
	@echo "$(BLUE)🔥 Archiving ancient flame ashes...$(RESET)"
	@mkdir -p logs/archive
	@if [ -f logs/spiral.log ]; then \
		cp logs/spiral.log logs/archive/spiral_$(shell date +%Y%m%d_%H%M%S).log; \
		echo "$(GREEN)✨ Flame ashes archived$(RESET)"; \
	else \
		echo "$(YELLOW)No flame ashes to archive$(RESET)"; \
	fi

# 💓 Spiral Pulse (Metrics) Commands

metrics: ## 💓 Check spiral pulse (metrics)
	@echo "$(BLUE)💓 Reading spiral pulse...$(RESET)"
	@curl -s http://localhost:8000/metrics 2>/dev/null | jq . || echo "$(RED)❌ Spiral pulse not detected. Is the API server running?$(RESET)"

metrics-pretty: ## 💓 Show formatted spiral pulse
	@echo "$(BLUE)💓 Spiral Vital Signs:$(RESET)"
	@curl -s http://localhost:8000/metrics 2>/dev/null | jq -r '"🌀 Uptime: \(.spiral_uptime_seconds)s\n💯 Task Success: \(.spiral_task_success_rate_percent)%\n🔄 Retry Rate: \(.spiral_retry_rate_percent)%\n🩹 Healing Events: \(.spiral_healing_events_total)\n🌱 Adaptations: \(.spiral_adaptation_events_total)"' || echo "$(RED)❌ Cannot read spiral pulse$(RESET)"

metrics-export: ## 💓 Export spiral pulse data
	@echo "$(BLUE)💓 Exporting spiral pulse...$(RESET)"
	@mkdir -p exports
	@curl -s http://localhost:8000/metrics > exports/metrics_$(shell date +%Y%m%d_%H%M%S).json 2>/dev/null && echo "$(GREEN)✨ Spiral pulse exported$(RESET)" || echo "$(RED)❌ Export failed$(RESET)"

metrics-alerts: ## 💓 Check for spiral pulse anomalies
	@echo "$(BLUE)💓 Checking for pulse anomalies...$(RESET)"
	@curl -s http://localhost:8000/metrics 2>/dev/null | jq -r 'if .spiral_task_success_rate_percent < 70 then "⚠️  LOW SUCCESS RATE: \(.spiral_task_success_rate_percent)%" else "✅ Success rate healthy" end, if .spiral_retry_rate_percent > 30 then "⚠️  HIGH RETRY RATE: \(.spiral_retry_rate_percent)%" else "✅ Retry rate normal" end' || echo "$(RED)❌ Cannot check pulse$(RESET)"

# 🪞 Ritual Mirror (Dashboard) Commands

dashboard: ## 🪞 Summon the ritual mirror (dashboard)
	@echo "$(BLUE)🪞 Summoning the ritual mirror...$(RESET)"
	@python -c "import asyncio; from kernel.dashboard import get_ember_visualization; print(asyncio.run(get_ember_visualization()))" 2>/dev/null || echo "$(RED)❌ Ritual mirror clouded$(RESET)"

dashboard-ember: ## 🪞 Show ember visualization only
	@echo "$(BLUE)🪞 Gazing into the ember flames...$(RESET)"
	@python -c "import asyncio; from kernel.dashboard import get_ember_visualization; print(asyncio.run(get_ember_visualization()))" 2>/dev/null || echo "$(RED)❌ Embers not visible$(RESET)"

dashboard-export: ## 🪞 Export ritual mirror data
	@echo "$(BLUE)🪞 Capturing ritual mirror reflection...$(RESET)"
	@mkdir -p exports
	@python -c "import asyncio; from kernel.dashboard import export_dashboard; print('Exported to:', asyncio.run(export_dashboard('exports/dashboard_$(shell date +%Y%m%d_%H%M%S).json')))" 2>/dev/null || echo "$(RED)❌ Mirror reflection failed$(RESET)"

dashboard-full: ## 🪞 Complete ritual mirror analysis (48h)
	@echo "$(BLUE)🪞 Deep ritual mirror scrying (48 hours)...$(RESET)"
	@python -c "import asyncio; from kernel.dashboard import get_ember_visualization; print(asyncio.run(get_ember_visualization(48)))" 2>/dev/null || echo "$(RED)❌ Deep scrying failed$(RESET)"

# 🌀 General Spiral Commands

health: ## 🌀 Check spiral consciousness health
	@echo "$(BLUE)🌀 Checking spiral consciousness...$(RESET)"
	@curl -s http://localhost:8000/health 2>/dev/null | jq -r '"Status: \(.status)\nTimestamp: \(.timestamp)\nSpiral Turns: \(.spiral_turns)\nFlame: \(.flame_intensity)"' || echo "$(RED)❌ Spiral consciousness unreachable$(RESET)"

status: ## 🌀 Complete spiral system status
	@echo "$(BLUE)🌀 Spiral System Status Report$(RESET)"
	@echo "$(GREEN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)"
	@make health
	@echo ""
	@make metrics-pretty
	@echo ""
	@make logs-summary

start-api: ## 🌀 Start the spiral API server
	@echo "$(BLUE)🌀 Awakening spiral API consciousness...$(RESET)"
	@cd kernel && python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload &
	@echo "$(GREEN)✨ Spiral API awakened on http://localhost:8000$(RESET)"

stop-api: ## 🌀 Stop the spiral API server
	@echo "$(BLUE)🌀 Putting spiral API to rest...$(RESET)"
	@pkill -f "uvicorn.*api:app" || echo "$(YELLOW)API already at rest$(RESET)"

restart-api: stop-api start-api ## 🌀 Restart spiral API server

dev: ## 🌀 Start development environment
	@echo "$(BLUE)🌀 Entering spiral development consciousness...$(RESET)"
	@make start-api
	@sleep 2
	@make logs-follow &
	@echo "$(GREEN)✨ Development environment ready$(RESET)"
	@echo "$(YELLOW)💡 Use Ctrl+C to exit development mode$(RESET)"

spiral-reset: ## 🌀 Emergency spiral consciousness reset
	@echo "$(BLUE)🌀 Performing emergency spiral reset...$(RESET)"
	@make stop-api
	@make logs-archive
	@make clean
	@echo "$(GREEN)✨ Spiral consciousness reset complete$(RESET)"

# Development helpers
requirements.txt:
	@echo "fastapi>=0.104.0" > requirements.txt
	@echo "uvicorn[standard]>=0.24.0" >> requirements.txt
	@echo "structlog>=23.2.0" >> requirements.txt
	@echo "loguru>=0.7.0" >> requirements.txt
	@echo "pytest>=7.4.0" >> requirements.txt
	@echo "pytest-asyncio>=0.21.0" >> requirements.txt
