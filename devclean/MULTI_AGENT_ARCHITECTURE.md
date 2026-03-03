# 🤖 DevClean Multi-Agent Architecture

## Overview

DevClean now uses a **sophisticated multi-agent architecture** powered by OpenClaw principles to analyze disk usage, Docker resources, and package caches. Each agent specializes in a specific domain, working autonomously and coordinating through an Orchestrator agent.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│           OrchestratorAgent (Master Coordinator)       │
└────────────────┬────────────────────────────────────────┘
                 │
    ┌────────────┼────────────┬──────────────────┐
    ▼            ▼            ▼                  ▼
┌─────────┐ ┌─────────┐ ┌──────────┐    ┌────────────┐
│ Disk    │ │ Docker  │ │ Package  │    │ Optimization
│Analyzer │ │Analyzer │ │ Cache    │────│  Agent (AI)
│ Agent   │ │ Agent   │ │Analyzer  │    │
│         │ │         │ │ Agent    │    │
└────┬────┘ └────┬────┘ └────┬─────┘    └─────┬──────┘
     │           │           │               │
     └───────────┴───────────┴───────────────┘
              Combined Analysis
                  │
                  ▼
            AI Recommendations
         (with OpenRouter API)
```

## Agents

### 1. **DiskAnalyzerAgent**
- **Purpose**: Scans the filesystem and analyzes disk usage
- **Outputs**:
  - File types by size
  - Folder sizes (hierarchical)
  - Total disk usage
- **Endpoint**: `GET /disk-analysis`

```python
# Example output
{
  "agent": "disk_analyzer",
  "file_types": {
    ".py": 523456,
    ".json": 234567,
    ".log": 1234567
  },
  "folders": {...},
  "total_size": 45678901
}
```

### 2. **DockerAnalyzerAgent**
- **Purpose**: Analyzes Docker images, containers, and volumes
- **Outputs**:
  - Unused Docker images
  - Dangling volumes
  - Stopped containers
- **Endpoint**: `GET /docker-analysis`
- **Requirements**: Docker installed and running

```python
# Example output
{
  "agent": "docker_analyzer",
  "unused_images": [...],
  "dangling_volumes": [...],
  "stopped_containers": [...]
}
```

### 3. **PackageCacheAgent**
- **Purpose**: Identifies package manager caches
- **Outputs**:
  - npm cache location and size
  - pip cache location and size
  - git objects cache
  - docker cache info
- **Endpoint**: `GET /cache-analysis`

```python
# Example output
{
  "agent": "cache_analyzer",
  "npm_cache": {
    "path": "~/.npm",
    "size": 523456789
  },
  "pip_cache": {
    "path": "~/.cache/pip",
    "size": 234567890
  }
}
```

### 4. **OptimizationAgent**
- **Purpose**: Generates AI-powered recommendations based on all analysis
- **Uses**: OpenRouter API with GPT-4o-mini
- **Outputs**:
  - Specific cleanup recommendations
  - Prioritized by impact
  - Fallback recommendations if AI unavailable
- **Returns**: Formatted markdown with actionable steps

### 5. **OrchestratorAgent** (Master Coordinator)
- **Purpose**: Coordinates all specialized agents
- **Workflow**:
  1. Phase 1: Run all analysis agents (disk, docker, cache)
  2. Phase 2: Aggregate results
  3. Phase 3: Send to OptimizationAgent for AI analysis
  4. Return combined report
- **Endpoint**: `GET /analyze` (main entry point)

## API Endpoints

### Full Multi-Agent Analysis
```bash
GET /analyze
```
Returns complete analysis from all agents + AI recommendations

### Individual Agent Analysis
```bash
GET /disk-analysis      # Disk usage only
GET /docker-analysis    # Docker resources only
GET /cache-analysis     # Package caches only
GET /recommendations    # AI recommendations only
```

### Agent Management
```bash
GET /agents/status      # View all agents and their status
GET /health             # Service health check
```

## Workflow

### Standard Workflow: `/analyze`
```
1. OrchestratorAgent starts
2. ├─ DiskAnalyzerAgent: Scan filesystem
3. ├─ DockerAnalyzerAgent: Check Docker resources
4. └─ PackageCacheAgent: Find package caches
5. Combine all data
6. Send to OptimizationAgent for AI analysis
7. Return comprehensive report
```

### Example Response
```json
{
  "workflow": "multi_agent_analysis",
  "agents": [
    {
      "agent": "disk_analyzer",
      "file_types": {...},
      "folders": {...},
      "total_size": 45678901
    },
    {
      "agent": "docker_analyzer",
      "unused_images": [...],
      ...
    },
    {
      "agent": "cache_analyzer",
      "npm_cache": {...},
      ...
    }
  ],
  "recommendations": "🤖 **AI Analysis**\n..."
}
```

## Configuration

### Required Environment Variables
```bash
# For AI recommendations (OpenRouter)
OPENROUTER_API_KEY=your_key_here

# Optional: For future integrations
COMPOSIO_API_KEY=your_key_here
```

### Agent Capabilities
- All agents run independently and can be called individually
- Orchestrator manages sequencing and data aggregation
- Graceful degradation if optional services (Docker, AI) unavailable

## Agent Coordination Features

### 1. **Fault Tolerance**
- If Docker not installed → Docker agent returns error gracefully
- If API key missing → Optimization agent provides fallback recommendations
- Failed agents don't block other agents

### 2. **Performance**
- Agents run sequentially but can be parallelized in future versions
- Caching possible for repeated analyses
- Results can be streamed for large datasets

### 3. **Extensibility**
- Easy to add new agents (SSL certificate cleanup, git repo analysis, etc.)
- Plugin architecture ready for OpenClaw integration
- Clear interface for custom agents

## Future Enhancements with OpenClaw

### Potential Integrations
1. **Agent Communication Layer**: Use OpenClaw's plugin system for inter-agent messaging
2. **Parallel Execution**: Run agents concurrently using OpenClaw's task orchestration
3. **Dynamic Agent Loading**: Load custom cleanup agents from plugins
4. **Distributed Execution**: Deploy agents across multiple systems

### Remote Agent Mode
```python
from openclaw2 import OpenClaw

# Future: Remote orchestration
client = OpenClaw.remote(api_key="cmdop_live_xxx")
results = client.pipeline([
    "disk_analysis",
    "docker_analysis",
    "cache_analysis",
    "optimize"
])
```

## Usage Examples

### Quick Analysis
```bash
curl http://localhost:8000/analyze | jq .
```

### Disk Analysis Only
```bash
curl http://localhost:8000/disk-analysis | jq '.analysis.file_types'
```

### Get Recommendations
```bash
curl http://localhost:8000/recommendations | jq '.recommendations'
```

### Check Agent Status
```bash
curl http://localhost:8000/agents/status | jq '.agents'
```

## Performance Metrics

### Typical Response Times
- Disk Analysis: 2-5 seconds
- Docker Analysis: 3-10 seconds
- Cache Analysis: 1-3 seconds
- AI Recommendations: 5-15 seconds (API dependent)
- **Total**: 15-40 seconds for full analysis

### Scalability
- Current design handles up to ~1GB filesystem indexing easily
- Cache and Docker analysis limited by system resources
- AI analysis throttled by OpenRouter API rate limits

## Code Structure

```
devclean/
├── agents.py          # All agent implementations
├── backend.py         # FastAPI app with endpoints
├── requirements.txt   # Dependencies
└── .env               # Configuration
```

## Key Files

### [agents.py](agents.py)
Contains all agent classes:
- `DiskAnalyzerAgent`
- `DockerAnalyzerAgent`
- `PackageCacheAgent`
- `OptimizationAgent`
- `OrchestratorAgent`

### [backend.py](backend.py)
FastAPI endpoints exposing agents:
- `/analyze` - Main orchestrated analysis
- `/disk-analysis`, `/docker-analysis`, `/cache-analysis` - Individual agents
- `/agents/status` - Agent health
- `/health` - Service health

## Troubleshooting

### Docker Agent Returns Errors
- Ensure Docker is installed: `docker --version`
- Ensure Docker daemon running: `docker ps`

### AI Recommendations Not Working
- Verify API key: `echo $OPENROUTER_API_KEY`
- Check internet connection
- Verify credit balance at openrouter.ai

### Agent Status Shows "Degraded"
- Usually due to missing OPENROUTER_API_KEY
- Still returns fallback recommendations
- No service interruption

## Integration with OpenClaw

Currently using **OpenClaw principles** (modular, extensible) without requiring remote API.

To enable full OpenClaw remote orchestration:
1. Get CMDOP API key
2. `pip install openclaw`
3. Create `openclaw_orchestrator.py` with remote pipeline
4. Switch backend to use remote orchestration

---

**Built for the OpenClaw Hackathon 2026** 🎉  
Multi-Agent Disk Optimization System with AI-Powered Recommendations
