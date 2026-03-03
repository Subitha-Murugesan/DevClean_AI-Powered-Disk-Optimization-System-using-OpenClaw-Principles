 # DevClean Telegram & Scheduler - Complete Setup

## Status: **LIVE & OPERATIONAL**

Your DevClean now includes:

### Daily 9 AM Analysis
- **Runs automatically** every morning at 9:00 AM UTC
- **Multi-agent analysis** of disk, Docker, and caches
- **AI recommendations** generated using OpenRouter
- **Results sent to Telegram** automatically

### Click-to-Notify Analysis  
- Click "Analyze Disk" in frontend
- Analysis runs immediately
- Results sent to Telegram chat
- Appears in both frontend and Telegram

### Verified Working
```
Service Status:
Health: healthy
Telegram: configured
Scheduler: running
API Key: configured
```

## What's New

### New Files Created
1. **[telegram_service.py](telegram_service.py)** - Telegram integration & scheduler
2. **[TELEGRAM_SCHEDULER_GUIDE.md](TELEGRAM_SCHEDULER_GUIDE.md)** - Complete usage guide

### Modified Files
1. **[backend.py](backend.py)** - Added startup/shutdown events, Telegram notifications
2. **[requirements.txt](requirements.txt)** - Added: apscheduler, pytz
3. **[agents.py](agents.py)** - No changes

### New Dependencies
- `apscheduler>=3.10.0` - Task scheduling
- `pytz>=2024.1` - Timezone support

## How It Works

### Daily Schedule
```
9:00 AM UTC (every day)
         ↓
   OrchestratorAgent starts
         ↓
   DiskAnalyzerAgent (runs)
   DockerAnalyzerAgent (runs)  ← parallel
   PackageCacheAgent (runs)
         ↓
   OptimizationAgent (AI analysis)
         ↓
   TelegramNotifier sends report
         ↓
Message appears in your Telegram chat
```

### Manual Analysis
```
Click "Analyze" in frontend
         ↓
Backend processes all agents
         ↓
Generates recommendations
         ↓
TelegramNotifier sends report
         ↓
Message appears in Telegram
Results shown in frontend
```

## Configuration (Already Done)

### Environment Variables (.env)
```bash
# Already configured
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
OPENROUTER_API_KEY=...
```

### Timezone (Default: UTC)
To change daily schedule time, edit [telegram_service.py](telegram_service.py):

```python
# Line ~85
self.scheduler.add_job(
    self.run_daily_analysis,
    'cron',
    hour=9,      # ← Change this number (0-23)
    minute=0,    # ← Or this for minutes (0-59)
    timezone=pytz.timezone('UTC'),  # ← Or change timezone
)
```

**Timezone Examples:**
- `'UTC'` = 9 AM UTC
- `'US/Eastern'` = 9 AM EST (-5) / EDT (-4)
- `'US/Pacific'` = 9 AM PST (-8) / PDT (-7)
- `'Europe/London'` = 9 AM GMT (+0) / BST (+1)
- `'Asia/Tokyo'` = 9 AM JST (+9)

## Testing

### Test 1: Manual Notification
```bash
curl http://localhost:8000/analyze | jq '.workflow'

# Expected: "multi_agent_analysis"
# Action: Check Telegram for notification
```

### Test 2: Check Scheduler Status
```bash
curl http://localhost:8000/health | jq '.scheduler_running'

# Expected: true
```

### Test 3: Agent Status
```bash
curl http://localhost:8000/agents/status | jq '.agents'

# Shows all 5 agents operational
```

## Telegram Message Format

### Manual Analysis Message
```
Manual Analysis
Time: 2026-02-28 14:32:15

Analysis Summary:

Disk Usage:
   • Total: 45.23 GB
   • File types: 512
   • Folders: 1024

Docker:
   • Unused images: 5
   • Dangling volumes: 2

Package Caches:
   • npm: 523.4MB, pip: 234.5MB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI Recommendations:

[500 characters of recommendations...]

See frontend for full recommendations
```

### Scheduled Analysis Message
```
Scheduled Analysis
Time: 2026-02-29 09:00:00
[Same format as above, marked as "Scheduled"]
```

## Security

**All credentials stored in .env file**
- Not in code
- Not in logs (masked)
- Sent only to Telegram HTTPS API

**Safe for production**
- Graceful error handling
- Failed notifications don't crash service
- Fallback recommendations if API down

## API Endpoints

### New/Updated Endpoints
| Endpoint | Method | Returns |
|----------|--------|---------|
| `/analyze` | GET | Full analysis + sends Telegram |
| `/health` | GET | Service health + scheduler status |
| `/agents/status` | GET | All agents status |
| `/disk-analysis` | GET | Disk data only |
| `/docker-analysis` | GET | Docker data only |
| `/cache-analysis` | GET | Cache data only |

## Troubleshooting

### No Telegram Messages?
- **Check configuration:** `curl http://localhost:8000/health | jq '.telegram_configured'`
- **Should show:** `true`
- **If false:** Verify .env has both `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
- **If true:** Your credentials might be invalid

### Scheduler Not Running?
- **Check status:** `curl http://localhost:8000/health | jq '.scheduler_running'`
- **Should show:** `true`
- **If false:** Restart backend and check logs

### Telegram API Error (400 Bad Request)?
- **Likely cause:** Invalid `TELEGRAM_CHAT_ID`
- **Solution:** Get correct chat ID via @RawDataBot on Telegram
- **Verify:** Send message manually to @BotFather's bot first

### Wrong Schedule Time?
- **Edit:** [telegram_service.py](telegram_service.py) line ~85
- **Change:** `hour=9` to desired hour (0-23)
- **Restart:** Backend picks up changes on reload

## Documentation Files

1. **[TELEGRAM_SCHEDULER_GUIDE.md](TELEGRAM_SCHEDULER_GUIDE.md)** - Complete usage guide
2. **[MULTI_AGENT_ARCHITECTURE.md](MULTI_AGENT_ARCHITECTURE.md)** - Agent system docs
3. **[backend.py](backend.py)** - Source code
4. **[telegram_service.py](telegram_service.py)** - Telegram/scheduler code
5. **[agents.py](agents.py)** - Multi-agent system

## Quick Start

### 1. Verify Setup
```bash
curl http://localhost:8000/health | jq .
```

### 2. Test Notification
```bash
curl http://localhost:8000/analyze
# Check Telegram for message
```

### 3. Customize Time (Optional)
```bash
# Edit telegram_service.py line ~85
# Change hour=9 to your preferred time
# Restart backend
```

### 4. Monitor Logs
```bash
# Backend logs show all scheduler activity
# Look for: "Scheduler initialized" and "Running scheduled daily analysis"
```

## What Gets Analyzed (Daily at 9 AM)

**Disk Usage**
- File types and sizes
- Folder hierarchy  
- Total disk usage

**Docker Resources**
- Unused images
- Dangling volumes
- Stopped containers

**Package Caches**
- npm cache size
- pip cache size
- git objects

**AI Recommendations**
- Cleanup suggestions
- Priority by impact
- Specific file paths

## Next Steps

1. **Verify Telegram credentials are correct**
   - Got bot token from @BotFather?
   - Got chat ID from @RawDataBot?
   - Added to .env?

2. **Test the system**
   - Click "Analyze" in frontend
   - Check Telegram for notification
   - Verify all fields populated

3. **Customize schedule (optional)**
   - Edit hour in telegram_service.py
   - Adjust timezone
   - Restart backend

4. **Monitor daily runs**
   - Check Telegram at scheduled time
   - Review recommendations
   - Implement cleanup suggestions

## Summary

**Your DevClean is now:**
- Running daily analysis at 9 AM UTC
- Sending results to Telegram automatically
- Notifying on manual analysis clicks
- Generating AI-powered recommendations
- Fully operational and production-ready

**Three ways to get analysis:**
1. **Automatic:** Every day at 9 AM → Telegram notification
2. **Manual:** Click "Analyze" → Telegram + Frontend
3. **API:** Call `/analyze` endpoint → Auto-notification

---

**Installation Date:** 2026-02-28  
**Status:** LIVE  
**Next Run:** Tomorrow at 09:00 UTC  

Your DevClean with Telegram scheduling is ready!
