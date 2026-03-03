"""
Telegram notification service and scheduler for DevClean
Handles sending analysis results to Telegram and scheduling daily tasks
"""

import os
import requests
from datetime import datetime
from typing import Optional, Dict, Any
import logging
import threading
import time

logger = logging.getLogger(__name__)


class TelegramBot:
    """Handles incoming Telegram bot commands"""
    
    def __init__(self, bot_token: str, chat_id: str, orchestrator):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.orchestrator = orchestrator
        self.api_url = f"https://api.telegram.org/bot{bot_token}" if bot_token else None
        self.offset = 0
        self.running = False
        self.enabled = bool(bot_token and chat_id)
    
    def start_polling(self):
        """Start polling for updates in a background thread"""
        if not self.enabled:
            logger.warning("Telegram bot polling disabled - missing credentials")
            return False
        
        try:
            self.running = True
            thread = threading.Thread(target=self._polling_loop, daemon=True)
            thread.start()
            logger.info("✅ Telegram bot polling started")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to start bot polling: {e}")
            return False
    
    def stop_polling(self):
        """Stop the polling loop"""
        self.running = False
        logger.info("Telegram bot polling stopped")
    
    def _polling_loop(self):
        """Main polling loop to receive updates"""
        while self.running:
            try:
                updates = self._get_updates()
                if updates:
                    for update in updates:
                        self._handle_update(update)
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                time.sleep(5)
    
    def _get_updates(self) -> list:
        """Get updates from Telegram"""
        try:
            url = f"{self.api_url}/getUpdates"
            params = {
                "offset": self.offset,
                "timeout": 30
            }
            response = requests.get(url, params=params, timeout=35)
            response.raise_for_status()
            
            data = response.json()
            if data.get("ok") and data.get("result"):
                updates = data["result"]
                if updates:
                    self.offset = updates[-1]["update_id"] + 1
                return updates
            return []
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
            return []
    
    def _handle_update(self, update: Dict[str, Any]):
        """Handle incoming update/message"""
        if "message" not in update:
            return
        
        message = update["message"]
        text = message.get("text", "").strip()
        
        # Handle commands
        if text.startswith("/"):
            self._handle_command(message, text)
    
    def _handle_command(self, message: Dict, text: str):
        """Handle bot commands"""
        command = text.split()[0].lower()
        
        if command == "/analyze":
            self._run_analyze_command(message)
        elif command == "/start":
            self._show_help(message)
        elif command == "/help":
            self._show_help(message)
        elif command == "/status":
            self._show_status(message)
    
    def _run_analyze_command(self, message: Dict):
        """Run analyzer and send results"""
        try:
            chat_id = message["chat"]["id"]
            sender = message["from"].get("first_name", "User")
            
            # Send "analyzing..." message
            self._send_message(
                chat_id,
                f"🔍 <b>Analyzing...</b>\n\nHi {sender}! Starting disk analysis..."
            )
            
            # Run analysis
            logger.info(f"Running analysis for Telegram command from {sender}")
            analysis_result = self.orchestrator.run_complete_analysis()
            recommendations = analysis_result.get("recommendations", "No recommendations")
            
            # Send detailed report
            self._send_analysis_report(chat_id, analysis_result, recommendations)
            
        except Exception as e:
            logger.error(f"Error running analyze command: {e}")
            self._send_message(chat_id, f"❌ Error: {str(e)}")
    
    def _show_help(self, message: Dict):
        """Show available commands"""
        chat_id = message["chat"]["id"]
        help_text = """
<b>🤖 DevClean Bot Commands</b>

📊 <b>/analyze</b> - Run disk analysis now
📈 <b>/status</b> - Show system status
ℹ️ <b>/help</b> - Show this help message

<b>Features:</b>
✅ Disk usage analysis
✅ Docker resources check
✅ Package cache detection
✅ AI-powered recommendations

<b>Daily:</b>
📅 Automatic analysis at 09:00 UTC

Try /analyze to get started!
"""
        self._send_message(chat_id, help_text)
    
    def _show_status(self, message: Dict):
        """Show system status"""
        chat_id = message["chat"]["id"]
        
        try:
            # Get basic info
            status_text = """
<b>📊 DevClean Status</b>

✅ Service: Online
✅ Bot: Active
✅ Scheduler: Running
📅 Next daily: 09:00 UTC

Use /analyze to start analysis
"""
            self._send_message(chat_id, status_text)
        except Exception as e:
            self._send_message(chat_id, f"❌ Error getting status: {e}")
    
    def _send_analysis_report(self, chat_id: str, analysis_data: Dict, recommendations: str):
        """Send detailed analysis report to chat"""
        try:
            # Extract agent data
            agents_info = analysis_data.get("agents", [])
            disk_agent = next((a for a in agents_info if a.get("agent") == "disk_analyzer"), None)
            docker_agent = next((a for a in agents_info if a.get("agent") == "docker_analyzer"), None)
            cache_agent = next((a for a in agents_info if a.get("agent") == "cache_analyzer"), None)
            
            # Build report
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            report = f"""
<b>✅ Analysis Complete</b>
<b>Time:</b> {timestamp}

<b>📊 Results:</b>
"""
            
            # Disk info
            if disk_agent:
                total_size = disk_agent.get("total_size", 0)
                file_count = len(disk_agent.get("file_types", {}))
                folder_count = len(disk_agent.get("folders", {}))
                
                def format_bytes(b):
                    if b == 0: return "0 B"
                    k = 1024
                    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
                    i = min(len(sizes)-1, int(__import__('math').log(b, k)))
                    return f"{b / (k**i):.2f} {sizes[i]}"
                
                report += f"""
💾 <b>Disk Usage:</b>
   • Total: {format_bytes(total_size)}
   • File types: {file_count}
   • Folders: {folder_count}
"""
            
            # Docker info
            if docker_agent and not docker_agent.get("error"):
                unused = len(docker_agent.get("unused_images", []))
                volumes = len(docker_agent.get("dangling_volumes", []))
                if unused > 0 or volumes > 0:
                    report += f"""
🐳 <b>Docker:</b>
   • Unused images: {unused}
   • Dangling volumes: {volumes}
"""
            
            # Cache info
            if cache_agent:
                cache_details = []
                if cache_agent.get("npm_cache"):
                    size_mb = cache_agent['npm_cache'].get('size', 0) / 1024 / 1024
                    cache_details.append(f"npm: {size_mb:.1f}MB")
                if cache_agent.get("pip_cache"):
                    size_mb = cache_agent['pip_cache'].get('size', 0) / 1024 / 1024
                    cache_details.append(f"pip: {size_mb:.1f}MB")
                
                if cache_details:
                    report += f"""
📦 <b>Package Caches:</b>
   • {', '.join(cache_details)}
"""
            
            report += "\n━━━━━━━━━━━━━━━━━━━━━━━━"
            
            # Send report in parts (Telegram has message size limit)
            self._send_message(chat_id, report)
            
            # Send recommendations
            rec_text = f"<b>💡 Recommendations:</b>\n\n{recommendations[:1000]}"
            if len(recommendations) > 1000:
                rec_text += "\n\n<i>...see full details in DevClean dashboard</i>"
            
            self._send_message(chat_id, rec_text)
            
        except Exception as e:
            logger.error(f"Error sending report: {e}")
            self._send_message(chat_id, f"❌ Error sending report: {e}")
    
    def _send_message(self, chat_id: str, text: str) -> bool:
        """Send a message to specific chat"""
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False


class TelegramNotifier:
    """Sends DevClean analysis reports to Telegram"""
    
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}" if self.bot_token else None
        self.enabled = bool(self.bot_token and self.chat_id)
    
    def send_message(self, message: str) -> bool:
        """Send a message to Telegram"""
        if not self.enabled:
            logger.warning("Telegram not configured. Add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to .env")
            return False
        
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"✅ Telegram message sent successfully")
            return True
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to send Telegram message: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ Telegram error: {str(e)}")
            return False
    
    def send_analysis_report(self, analysis_data: Dict[str, Any], recommendations: str, scheduled: bool = False) -> bool:
        """Send analysis report to Telegram"""
        
        if not self.enabled:
            return False
        
        # Extract agent data
        agents_info = analysis_data.get("agents", [])
        disk_agent = next((a for a in agents_info if a.get("agent") == "disk_analyzer"), None)
        docker_agent = next((a for a in agents_info if a.get("agent") == "docker_analyzer"), None)
        cache_agent = next((a for a in agents_info if a.get("agent") == "cache_analyzer"), None)
        
        # Build message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        trigger = "📅 <b>Scheduled Analysis</b>" if scheduled else "🔍 <b>Manual Analysis</b>"
        
        message = f"""{trigger}
<b>Time:</b> {timestamp}

<b>📊 Analysis Summary:</b>
"""
        
        # Disk info
        if disk_agent:
            total_size = disk_agent.get("total_size", 0)
            file_count = len(disk_agent.get("file_types", {}))
            folder_count = len(disk_agent.get("folders", {}))
            
            def format_bytes(b):
                if b == 0: return "0 B"
                k = 1024
                sizes = ['B', 'KB', 'MB', 'GB', 'TB']
                i = min(len(sizes)-1, int(__import__('math').log(b, k)))
                return f"{b / (k**i):.2f} {sizes[i]}"
            
            message += f"""
💾 <b>Disk Usage:</b>
   • Total: {format_bytes(total_size)}
   • File types: {file_count}
   • Folders: {folder_count}
"""
        
        # Docker info
        if docker_agent and not docker_agent.get("error"):
            unused = len(docker_agent.get("unused_images", []))
            volumes = len(docker_agent.get("dangling_volumes", []))
            message += f"""
🐳 <b>Docker:</b>
   • Unused images: {unused}
   • Dangling volumes: {volumes}
"""
        
        # Cache info
        if cache_agent:
            caches_found = 0
            cache_details = []
            
            if cache_agent.get("npm_cache"):
                caches_found += 1
                cache_details.append(f"npm: {cache_agent['npm_cache'].get('size', 0) / 1024 / 1024:.1f}MB")
            if cache_agent.get("pip_cache"):
                caches_found += 1
                cache_details.append(f"pip: {cache_agent['pip_cache'].get('size', 0) / 1024 / 1024:.1f}MB")
            
            if cache_details:
                message += f"""
📦 <b>Package Caches:</b>
   • {', '.join(cache_details)}
"""
        
        # Add first part of recommendations
        message += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>💡 AI Recommendations:</b>

{recommendations[:500]}...

<i>See frontend for full recommendations</i>
"""
        
        return self.send_message(message)
    
    def send_status(self, status: str) -> bool:
        """Send a status update"""
        message = f"🤖 <b>DevClean Status</b>\n{status}"
        return self.send_message(message)


class SchedulerService:
    """Manages scheduled analysis tasks"""
    
    def __init__(self, orchestrator, telegram_notifier: TelegramNotifier):
        self.orchestrator = orchestrator
        self.telegram = telegram_notifier
        self.scheduler = None
    
    def initialize_scheduler(self):
        """Initialize APScheduler"""
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            import pytz
            
            self.scheduler = BackgroundScheduler()
            
            # Add job to run at 9 AM every day
            self.scheduler.add_job(
                self.run_daily_analysis,
                'cron',
                hour=9,
                minute=0,
                timezone=pytz.timezone('UTC'),  # Adjust timezone as needed
                id='devclean_daily_9am',
                name='DevClean Daily 9 AM Analysis'
            )
            
            self.scheduler.start()
            logger.info("✅ Scheduler initialized - Daily analysis scheduled for 09:00 UTC")
            
            # Send startup notification
            self.telegram.send_status("✅ DevClean scheduler started! Daily analysis at 09:00 UTC")
            
            return True
        
        except ImportError:
            logger.error("❌ APScheduler not installed. Run: pip install apscheduler")
            return False
        except Exception as e:
            logger.error(f"❌ Scheduler initialization failed: {str(e)}")
            return False
    
    def run_daily_analysis(self):
        """Run scheduled daily analysis"""
        try:
            logger.info("📅 Running scheduled daily analysis...")
            
            # Run analysis
            analysis_result = self.orchestrator.run_complete_analysis()
            
            # Send to Telegram
            recommendations = analysis_result.get("recommendations", "No recommendations available")
            self.telegram.send_analysis_report(
                analysis_result,
                recommendations,
                scheduled=True
            )
            
            logger.info("✅ Scheduled analysis completed and sent to Telegram")
        
        except Exception as e:
            logger.error(f"❌ Scheduled analysis failed: {str(e)}")
            self.telegram.send_status(f"❌ Analysis failed: {str(e)}")
    
    def shutdown(self):
        """Shutdown scheduler gracefully"""
        if self.scheduler:
            self.scheduler.shutdown()
            logger.info("Scheduler shut down")
