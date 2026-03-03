from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import requests
import json
from collections import defaultdict
from agents import OrchestratorAgent
from telegram_service import TelegramNotifier, TelegramBot, SchedulerService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="DevClean - OpenClaw Multi-Agent Edition")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hackathon API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # $10 free credits!
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")  # Optional: for agent tools
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize multi-agent orchestrator
orchestrator = OrchestratorAgent(api_key=OPENROUTER_API_KEY)

# Initialize Telegram notifier
telegram = TelegramNotifier()

# Initialize Telegram bot for commands
telegram_bot = TelegramBot(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, orchestrator)

# Initialize scheduler
scheduler = SchedulerService(orchestrator, telegram)

@app.on_event("startup")
async def startup_event():
    """Initialize scheduler and bot on app startup"""
    logger.info("🚀 DevClean starting up...")
    scheduler.initialize_scheduler()
    
    if telegram.enabled:
        logger.info("📱 Telegram notifications enabled")
    else:
        logger.info("📱 Telegram notifications disabled (add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to .env)")
    
    # Start Telegram bot polling
    if telegram_bot.enabled:
        telegram_bot.start_polling()
        logger.info("🤖 Telegram bot polling started - send /help for commands")
    else:
        logger.info("🤖 Telegram bot disabled (add TELEGRAM_BOT_TOKEN to .env)")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown scheduler and bot gracefully"""
    logger.info("🛑 DevClean shutting down...")
    telegram_bot.stop_polling()
    scheduler.shutdown()

@app.get("/analyze")
def analyze():
    """Main analysis endpoint using multi-agent architecture"""
    result = orchestrator.run_complete_analysis()
    
    # Send to Telegram if enabled
    if telegram.enabled:
        try:
            recommendations = result.get("recommendations", "No recommendations available")
            telegram.send_analysis_report(result, recommendations, scheduled=False)
            logger.info("✅ Analysis results sent to Telegram")
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
    
    return result

@app.get("/agents/status")
def agents_status():
    """Return status of all available agents"""
    return {
        "status": "operational",
        "agents": [
            {
                "name": "disk_analyzer",
                "description": "Scans filesystem and analyzes disk usage",
                "status": "ready"
            },
            {
                "name": "docker_analyzer",
                "description": "Analyzes Docker images and containers",
                "status": "ready"
            },
            {
                "name": "cache_analyzer",
                "description": "Identifies package manager caches",
                "status": "ready"
            },
            {
                "name": "optimization",
                "description": "Generates AI-powered recommendations",
                "status": "ready" if OPENROUTER_API_KEY else "degraded"
            },
            {
                "name": "orchestrator",
                "description": "Coordinates all agents",
                "status": "operational"
            }
        ]
    }

@app.get("/disk-analysis")
def disk_analysis_only():
    """Get disk analysis from the disk analyzer agent only"""
    disk_agent = orchestrator.disk_agent
    return {
        "agent": "disk_analyzer",
        "analysis": disk_agent.analyze()
    }

@app.get("/docker-analysis")
def docker_analysis_only():
    """Get Docker analysis from the Docker analyzer agent only"""
    docker_agent = orchestrator.docker_agent
    return {
        "agent": "docker_analyzer",
        "analysis": docker_agent.analyze()
    }

@app.get("/cache-analysis")
def cache_analysis_only():
    """Get cache analysis from the cache analyzer agent only"""
    cache_agent = orchestrator.cache_agent
    return {
        "agent": "cache_analyzer",
        "analysis": cache_agent.analyze()
    }

@app.get("/recommendations")
def get_recommendations():
    """Get AI-powered recommendations based on full analysis"""
    analysis_data = orchestrator.run_complete_analysis()
    return {
        "recommendations": analysis_data.get("recommendations"),
        "analysis_summary": {
            "total_agents_run": len(analysis_data.get("agents", [])),
            "agents": [agent.get("agent") for agent in analysis_data.get("agents", [])]
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DevClean - Multi-Agent Disk Optimizer",
        "version": "2.0-multiagent",
        "api_key_configured": bool(OPENROUTER_API_KEY),
        "telegram_configured": telegram.enabled,
        "scheduler_running": bool(scheduler.scheduler and scheduler.scheduler.running if scheduler.scheduler else False)
    }
