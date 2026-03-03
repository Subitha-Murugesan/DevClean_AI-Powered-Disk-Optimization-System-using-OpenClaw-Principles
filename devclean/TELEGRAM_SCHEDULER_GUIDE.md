 # DevClean Telegram & Scheduler Setup Guide

## What's Enabled

Your DevClean now has:
- Daily 9 AM Scheduled Analysis - Runs automatically every morning at 9:00 UTC
- Telegram Notifications - Results sent to your Telegram chat
- Manual Analysis + Notification - Clicking "Analyze" also sends results to Telegram

## Configuration

### Environment Variables (in `.env`)
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
OPENROUTER_API_KEY=your_openrouter_key_here
```

### Verify Setup
```bash
# Check health endpoint
curl http://localhost:8000/health | jq .

# Expected output:
{
  "status": "healthy",
  "telegram_configured": true,
  "scheduler_running": true
}
```

## Daily Scheduler

### What Runs Daily at 9 AM
1. DiskAnalyzerAgent - Scans filesystem
2. DockerAnalyzerAgent - Checks Docker images/volumes
3. PackageCacheAgent - Finds npm, pip caches
4. OptimizationAgent - Generates AI recommendations
5. Telegram Notifier - Sends report to your chat

### Customize Schedule
Edit `telegram_service.py` to change timing:

```python
# Change from 09:00 UTC to 08:00 UTC
self.scheduler.add_job(
    self.run_daily_analysis,
    'cron',
    hour=8,  # Change this
    minute=0,
    timezone=pytz.timezone('UTC'),
)
```

### Supported Timezone Formats
```python
# Common timezones
'UTC'
'US/Eastern'
'US/Pacific'
'Europe/London'
'Asia/Tokyo'

# Apply timezone
timezone=pytz.timezone('US/Eastern')
```

## Telegram Notifications

### Manual Analysis Notification
When you click "Analyze Disk" in the frontend:
- Report sent immediately to Telegram
- Shows disk usage, Docker info, caches
- Includes AI recommendations preview

### Scheduled Analysis Notification
At 9 AM daily:
- Automatic analysis runs
- Full report sent to Telegram
- Marked as "Scheduled Analysis"

### Message Format
```
Scheduled Analysis
Time: 2026-02-28 09:00:00

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

[AI suggestions preview...]

See frontend for full recommendations
```

## Test Notifications

### Test 1: Manual Analysis
```bash
# This will send a notification to Telegram
curl http://localhost:8000/analyze | jq '.workflow'
```

### Test 2: Test Status Message
Use the status endpoint (future):
```bash
curl http://localhost:8000/status/test
```

### Test 3: Check Scheduler Status
```bash
curl http://localhost:8000/health | jq '.scheduler_running'
```

## Endpoints

### Analysis & Scheduling
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/analyze` | GET | Run analysis + send to Telegram |
| `/health` | GET | Check service & scheduler health |
| `/agents/status` | GET | View all agents |

### Individual Agents
| Endpoint | Agent |
|----------|-------|
| `/disk-analysis` | Disk usage analysis |
| `/docker-analysis` | Docker resources |
| `/cache-analysis` | Package caches |
| `/recommendations` | AI suggestions only |

## Architecture

```
┌─────────────────────────────────────────────┐
│     Daily Schedule (9 AM UTC)               │
│            ↓                                │
│     OrchestratorAgent                       │
│     ├─ DiskAnalyzerAgent                   │
│     ├─ DockerAnalyzerAgent                  │
│     ├─ PackageCacheAgent                    │
│     └─ OptimizationAgent (AI)              │
│            ↓                                │
│     TelegramNotifier                        │
│     └─ Send to Chat                         │
└─────────────────────────────────────────────┘
```

## Security Notes

- Bot token stored in `.env` (not in code)
- Chat ID stored in `.env` (not in code)
- Messages sent via HTTPS to Telegram API
- No sensitive data logged

## Troubleshooting

### Telegram Not Sending?
```bash
# Check configuration
curl http://localhost:8000/health | jq '.telegram_configured'

# Should return: true

# If false, verify .env has:
# TELEGRAM_BOT_TOKEN=<token>
# TELEGRAM_CHAT_ID=<id>
```

### Scheduler Not Running?
```bash
# Check scheduler status
curl http://localhost:8000/health | jq '.scheduler_running'

# Restart backend:
# 1. Kill current process: ps aux | grep uvicorn | kill -9
# 2. Restart: python -m uvicorn backend:app --reload
```

### Messages Not Formatted?
- Ensure Telegram bot has HTML parse mode enabled
- Check bot token is valid at https://api.telegram.org/bot<TOKEN>/getMe

### Timezone Issues?
- Default is UTC (9 AM UTC)
- For US/Eastern, that's 4 AM EST / 5 AM EDT
- Adjust `hour` parameter in scheduler to match your timezone

## Example Workflow

Morning at 9 AM:
1. Scheduler triggers
2. OrchestratorAgent runs all analysis agents
3. Analysis results collected
4. AI recommendations generated
5. Telegram message formatted
6. Telegram API called
7. Message appears in your chat

When you click "Analyze":
1. Frontend calls `/analyze`
2. Backend runs full analysis
3. Telegram notification sent
4. Results displayed in frontend

## Next Steps

1. Verify Setup Works
```bash
curl http://localhost:8000/analyze
# Check Telegram for notification
```

2. Check Scheduled Job
```bash
curl http://localhost:8000/health
# Verify scheduler_running: true
```

3. Customize Schedule (optional)
- Edit hour/minute in telegram_service.py
- Restart backend

4. Monitor Logs
```bash
# Backend logs show all activity
grep "Telegram\|scheduler" backend.log
```

## Files Modified

- [backend.py](backend.py) - Added Telegram integration & scheduler startup
- [telegram_service.py](telegram_service.py) - New: Telegram and scheduler service
- [requirements.txt](requirements.txt) - Added: apscheduler
- [agents.py](agents.py) - No changes (works with new backend)

---

**Backend running on:** http://localhost:8000  
**Frontend running on:** http://localhost:5173  
**Telegram notifications:** Active

Try clicking "Analyze Disk" now to get your first Telegram notification!
