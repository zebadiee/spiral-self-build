
# Spiral Self-Learning Assistant (SLSA) Skeleton

A production-ready, domain-agnostic blueprint for building self-learning AI applications. This skeleton provides the essential components to create AI assistants that continuously improve through interaction and feedback.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env with your configuration

# 3. Start the MCP Learning Server
python assistant/mcp_simple_server.py

# 4. Launch the Dashboard (in another terminal)
python tk_simple_dashboard.py

# 5. Test knowledge ingestion
python assistant/knowledge_simple.py sample.pdf
```

## 📁 Project Structure

```
spiral-self-build/
├── assistant/
│   ├── mcp_simple_server.py    # Core MCP Learning Server
│   └── knowledge_simple.py     # Knowledge Ingestion Engine
├── tk_simple_dashboard.py      # Metrics Dashboard
├── n8n_workflow.json          # Automation Workflow
├── docker-compose.yml         # Production Deployment
├── CHECKPOINT_GUIDE.md        # Step-by-step Implementation
└── SUMMARY_REPORT.md          # Progress Tracking Template
```

## 🎯 Core Features

- **MCP Learning Server**: REST API for learning operations with /status, /learn, /insights endpoints
- **Knowledge Ingestion**: PDF processing that extracts 3 key insights automatically
- **Real-time Dashboard**: Tkinter-based metrics visualization
- **Checkpoint System**: 5 guided steps with visible wins (<20min each)
- **Docker Ready**: Production deployment with docker-compose
- **n8n Integration**: Ready-to-import workflow for automation

## 🔧 Architecture

This skeleton follows a modular architecture:
- **Learning Core**: MCP server handles all learning operations
- **Knowledge Layer**: Processes and extracts insights from documents
- **Interface Layer**: Dashboard provides real-time feedback
- **Automation Layer**: n8n workflow orchestrates learning cycles

## 📋 Checkpoints

Follow the [CHECKPOINT_GUIDE.md](CHECKPOINT_GUIDE.md) for a structured 5-step implementation:
1. **Setup & Validation** (5min) - Verify all components work
2. **First Learning Cycle** (10min) - Process your first document
3. **Dashboard Integration** (15min) - See real-time metrics
4. **Automation Setup** (20min) - Configure n8n workflow
5. **Production Deploy** (15min) - Launch with Docker

## 🐳 Production Deployment

```bash
# Quick production start
docker-compose up -d

# Check status
curl http://localhost:8001/status
```

## 🤝 Contributing

This is a reusable blueprint. Fork it, customize it, and build your domain-specific self-learning assistant!

## 📄 License

MIT License - Build amazing things!
