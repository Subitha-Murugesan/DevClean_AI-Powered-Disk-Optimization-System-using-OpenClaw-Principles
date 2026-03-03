# 🧹 DevClean - OpenClaw Hackathon Edition

**AI-Powered Disk Space Optimizer** built for the OpenClaw Hackathon using sponsor tools!

## 🎯 Hackathon Resources Used

### ✅ OpenRouter ($10 Free Credits)
- **What**: Unified API for 300+ LLMs (Claude, GPT-4, Gemini, etc.)
- **Use in Project**: Powers AI disk analysis recommendations
- **Setup**: 
  1. Create account at [openrouter.ai](https://openrouter.ai)
  2. Redeem code at [openrouter.ai/redeem](https://openrouter.ai/redeem) (expires March 1, 2026!)
  3. Add `OPENROUTER_API_KEY` to `.env`

### 🛠️ Optional Integrations

**Composio** - Connect agents to 1000+ apps
- Give your AI agent real tools (filesystem operations, Docker cleanup, etc.)
- Prize: $25K credits + feature interview for top team using Composio

**CopilotKit** - Add AI copilots to React UI
- Embed AI assistance directly in the frontend
- Enable users to ask questions about their disk usage inline

## 🚀 Quick Start (5 Minutes)

### 1. Backend Setup
```bash
cd devclean

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY

# Start server (http://localhost:8000)
uvicorn backend:app --reload
```

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start dev server (http://localhost:5173)
npm run dev
```

### 3. Use It!
1. Open `http://localhost:5173`
2. Click **"Analyze Disk"**
3. Get AI-powered cleanup recommendations!

## 📊 Features

- **📁 File Type Analysis**: See which file types consume the most space
- **💾 Largest Folders**: Identify space-hogging directories
- **🤖 AI Recommendations**: Get actionable cleanup suggestions via OpenRouter
- **📱 Responsive UI**: Works on desktop, tablet, and mobile
- **⚡ Fast Analysis**: Real-time disk scanning and analysis

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  ← Modern TypeScript UI
│  (localhost:5173)│
└────────┬────────┘
         │ REST API
         ↓
┌─────────────────┐
│ FastAPI Backend │  ← Python disk analyzer
│ (localhost:8000)│
└────────┬────────┘
         │ OpenRouter API
         ↓
┌─────────────────┐
│   GPT-4o-mini   │  ← AI analysis ($10 credits)
│   (via OpenRouter)│
└─────────────────┘
```

## 📡 API Endpoints

### `GET /analyze`
Analyzes current directory and returns AI suggestions

**Response:**
```json
{
  "analysis": {
    "file_types": {
      ".log": 1024000,
      ".tmp": 512000
    },
    "folders": {
      "/tmp": 2048000,
      "/var/cache": 1024000
    }
  },
  "ai_suggestions": "🤖 AI Analysis via OpenRouter..."
}
```

## 🎨 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenRouter** - Unified LLM API (hackathon sponsor)
- **Python 3.9+** - Core language

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Lightning-fast dev server
- **CSS3** - Modern styling with gradients

## 💡 Extending for the Hackathon

### Add Composio Integration
Give your AI agent real tools to execute cleanup:

```bash
pip install composio-core composio-openai
```

```python
from composio import Composio

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))

# Give agent access to shell commands
tools = composio.get_tools(actions=["SHELL_EXEC_COMMAND"])
```

### Add CopilotKit to Frontend
Embed AI chat directly in the UI:

```bash
cd frontend
npm install @copilotkit/react-core @copilotkit/react-ui
```

Enable users to ask "What's using all my disk space?" inline!

### Add Vapi Voice Interface
Let users analyze disk with voice commands:

```bash
npm install @vapi-ai/web
```

"Hey Vapi, analyze my disk and suggest cleanups"

### Add Auth0 for Multi-User
Secure user authentication for production:

```bash
npm install @auth0/auth0-react
```

Each user can track their own disk optimization progress.

## 📝 Environment Setup

```bash
# Required
OPENROUTER_API_KEY=sk-or-v1-xxxx  # $10 free credits!

# Optional - Enhance with more tools
COMPOSIO_API_KEY=xxxx              # 1000+ app integrations
VAPI_API_KEY=xxxx                  # Voice interface
AUTH0_DOMAIN=xxxx                  # User authentication
AUTH0_CLIENT_ID=xxxx
```

## 🐛 Troubleshooting

### "No AI suggestions"
- Check `.env` has `OPENROUTER_API_KEY`
- Verify you redeemed your hackathon promo code
- Check backend logs for API errors

### "Failed to connect"
- Ensure backend is running on port 8000
- Frontend should auto-proxy to backend
- Check CORS settings if changing ports

### "API request timed out"
- OpenRouter might be slow under load
- Try again or increase timeout in backend.py

## 🏆 Hackathon Tips

1. **Use $10 Credits Wisely**: GPT-4o-mini is cost-effective (~$0.15/1M tokens)
2. **Add Composio**: Strong differentiation + $25K prize opportunity
3. **Make it Visual**: Users love seeing before/after disk savings
4. **Add Voice with Vapi**: Natural UX for asking cleanup questions
5. **Demo Real Impact**: Show actual disk space freed on your system

## 📚 Resources

- [OpenRouter Docs](https://openrouter.ai/docs)
- [OpenRouter Models](https://openrouter.ai/models) - Browse 300+ models
- [Composio Quickstart](https://docs.composio.dev/quickstart)
- [CopilotKit Docs](https://docs.copilotkit.ai)
- [Vapi Docs](https://docs.vapi.ai)

## 📄 License

MIT License - Build whatever you want!

## 🤝 Contributing

This is a hackathon project - fork it, extend it, make it yours!

---

**Built for the OpenClaw Hackathon 2026** 🎉

*Powered by OpenRouter ($10 free credits) • Ready for Composio, CopilotKit, Vapi, Auth0, and ElevenLabs integration*
