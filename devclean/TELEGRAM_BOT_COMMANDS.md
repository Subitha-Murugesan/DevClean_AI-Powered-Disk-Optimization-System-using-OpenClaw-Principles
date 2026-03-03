 # DevClean Telegram Bot Commands

## New Feature: Control DevClean via Telegram

Your DevClean bot is now listening for commands in Telegram. You can run analysis and get results directly from chat.

## Available Commands

### `/analyze`
**Run disk analysis immediately and get results in Telegram**

```
User: /analyze
Bot: Analyzing...
     [waits 15-30 seconds]
     Analysis Complete
     
     Results:
     Disk Usage: 45.23 GB
     Docker: 5 unused images
     Caches: npm 523MB, pip 234MB
     
     Recommendations: [AI suggestions...]
```

### `/help` or `/start`
**Show available commands and features**

```
User: /help
Bot: DevClean Bot Commands
     
     /analyze - Run disk analysis now
     /status - Show system status
     /help - Show this help message
     
     Features:
     Disk usage analysis
     Docker resources check
     Package cache detection
     AI-powered recommendations
     
     Daily: Automatic analysis at 09:00 UTC
     Try /analyze to get started!
```

### `/status`
**Check system status**

```
User: /status
Bot: DevClean Status
     
     Service: Online
     Bot: Active
     Scheduler: Running
     Next daily: 09:00 UTC
     
     Use /analyze to start analysis
```

## How It Works

### Command Flow
```
You send: /analyze
           -> Bot receives and processes
           -> Starts all agents (Disk, Docker, Cache)
           -> Runs AI optimization
           -> Sends formatted results to Telegram
           -> You receive: Analysis + Recommendations
```

### Step-by-Step Example

**1. Send Command**
- Open Telegram
- Go to your bot
- Type `/analyze` and send

**2. Bot Responds**
- Shows "Analyzing..." message
- Starts analysis

**3. Get Results**
- Receives disk usage summary
- Docker information
- Package caches
- AI recommendations

## Three Ways to Analyze

### 1. Telegram Commands
```
Send: /analyze
Result: Gets analysis in Telegram instantly
```

### 2. Web Frontend (Existing)
```
Visit: http://localhost:5173
Click: "Analyze Disk" button
Result: Shows in web + sends to Telegram
```

### 3. API Endpoint (Existing)
```
curl http://localhost:8000/analyze
Result: Returns JSON + sends to Telegram
```

### 4. Daily Automatic (Existing)
```
Every day at 09:00 UTC
Result: Automatic analysis sent to Telegram
```

## Backend Requirements

The backend includes:

- **TelegramBot class** - Listens for commands
- **Bot polling** - Checks for messages continuously
- **Command handlers** - `/analyze`, `/help`, `/status`
- **Integration** - Runs orchestrator through command

## What Bot Sends

### Analysis Report Format
```
Analysis Complete
Time: 2026-02-28 16:45:30

Results:

Disk Usage:
   • Total: 45.23 GB
   • File types: 512
   • Folders: 1024

Docker:
   • Unused images: 5
   • Dangling volumes: 2

Package Caches:
   • npm: 523.4MB, pip: 234.5MB

━━━━━━━━━━━━━━━━━━━━━━━━

Recommendations:

[AI suggestions for cleanup...]
```

## Quick Start

### Step 1: Verify Bot is Running
```bash
curl http://localhost:8000/health | jq '.telegram_configured'
# Should return: true
```

### Step 2: Open Telegram
- Search for your DevClean bot
- Or open existing chat

### Step 3: Send Command
```
Type: /help
Send: Press send
Result: Bot responds with commands
```

### Step 4: Run Analysis
```
Type: /analyze
Send: Press send
Wait: 15-30 seconds
Result: Get full analysis report
```

## Bot Polling Details

The bot:
- Runs in background thread (non-blocking)
- Checks for messages every 1-30 seconds
- Processes commands instantly
- Sends formatted responses
- Handles errors gracefully

## Command Processing

Each command:
1. **Received** - Bot polling catches it
2. **Parsed** - Extracts command type
3. **Executed** - Runs appropriate handler
4. **Processed** - Orchestrator runs agents
5. **Formatted** - Prepares response
6. **Sent** - Message back to Telegram

## Stop Bot

The bot automatically stops when backend shuts down:
```bash
# Backend stops
pkill -f "uvicorn backend"

# Bot polling stops
# Telegram messages won't be processed until backend restarts
```

## Troubleshooting

### Bot not responding?
1. Check if backend is running: `curl http://localhost:8000/health`
2. Verify chat ID is correct in `.env`
3. Restart backend

### Command not recognized?
- Make sure to use `/` prefix
- Try `/help` to see available commands
- Commands are case-insensitive

### Takes too long to respond?
- Analysis takes 15-30 seconds
- Docker checks take 3-10 seconds
- AI analysis depends on API speed

## Available Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `/analyze` | Run analysis now | Send & wait for results |
| `/help` | Show commands | See all available options |
| `/start` | Start/help | Same as /help |
| `/status` | System status | Check if bot is working |

## Next Steps

1. **Test bot** - Send `/analyze` in Telegram
2. **Check results** - Verify message arrives
3. **Use regularly** - Run analysis via commands
4. **Schedule** - Still runs daily at 9 AM

---

**Telegram Bot Status:** Active  
**Commands Enabled:** /analyze, /help, /start, /status  
**Polling:** Active and listening for messages  

Try `/analyze` in Telegram now!
