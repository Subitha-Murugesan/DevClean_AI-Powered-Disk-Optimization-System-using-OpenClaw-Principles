# DevClean - Intelligent Disk Space Optimizer (OpenClaw Hackathon Edition)

DevClean is a full-stack application that analyzes disk usage and provides AI-powered optimization recommendations using **OpenRouter** (hackathon sponsor with $10 free credits).

## 🎯 Hackathon Quick Start

1. Sign up at [openrouter.ai](https://openrouter.ai)
2. Copy your API key from the dashboard

### Setup (5 minutes)

```bash
# Backend
cd devclean
pip install -r requirements.txt
cp .env.example .env
# Add OPENROUTER_API_KEY to .env
uvicorn backend:app --reload

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` and click "Analyze Disk"!

## 🎯 Features

### Backend
- **Disk Analysis Engine**: Scans filesystem and categorizes files by type and folder
- **OpenRouter Integration**: AI analysis using 300+ models via unified API
- **REST API**: FastAPI-based API for frontend communication
- **CORS Enabled**: Secure frontend-backend communication

### Frontend
- **Modern React UI**: Built with React 18 + TypeScript + Vite
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Analysis**: Display disk analysis with formatted data
- **AI Recommendations**: Shows optimization suggestions from GPT-4o-mini
- **Visual Data**: Progress bars and tables for easy scanning

## 📡 API Endpoints

### `/analyze` (GET)
Analyzes disk and returns AI suggestions

**Response:**
```json
{
  "analysis": {
    "file_types": {
      ".log": 1024000,
      ".tmp": 512000,
      ".py": 256000
    },
    "folders": {
      "/home/user/.cache": 2048000,
      "/tmp": 1024000,
      "/var/log": 512000
    }
  },
  "ai_suggestions": "🤖 **AI Analysis** (via OpenRouter - gpt-4o-mini)\n\n... optimization recommendations ..."
}
```

## 🚀 Hackathon Enhancements

### Add Composio (Prize Opportunity!)
Give your AI agent real tools to execute cleanup:
```bash
pip install composio-core
export COMPOSIO_API_KEY=your_key
```
**Prize**: Top team using Composio gets $25K credits + feature interview!

### Add CopilotKit to React UI
Embed AI chat directly in the interface:
```bash
cd frontend
npm install @copilotkit/react-core @copilotkit/react-ui
```

### Add Vapi Voice Interface
Voice commands for disk analysis:
```bash
npm install @vapi-ai/web
export VAPI_API_KEY=your_key
```
**Free Credits**: Use code `Openclaw022026` at dashboard.vapi.ai

## 📁 Project Structure

```
.
├── devclean/              # Backend (Python/FastAPI)
│   ├── backend.py         # Main API server with OpenRouter
│   ├── requirements.txt   # Python dependencies
│   ├── .env.example       # Hackathon API key template
│   └── logs/              # Backend logs
│
├── frontend/              # Frontend (React/TypeScript)
│   ├── src/
│   │   ├── App.tsx        # Main component
│   │   ├── App.css        # Styling
│   │   └── main.tsx       # Entry point
│   ├── package.json       # Node dependencies
│   ├── tsconfig.json      # TypeScript config
│   └── vite.config.ts     # Vite config
│
└── HACKATHON_README.md    # Detailed hackathon guide
```

## 🔧 Development

### Backend Development
```bash
cd devclean
uvicorn backend:app --reload
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Production Build
```bash
# Frontend
cd frontend
npm run build
npm run preview

# Backend
cd devclean
uvicorn backend:app
```

## 📦 Dependencies

### Backend
- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **python-dotenv**: Environment config
- **requests**: HTTP client for OpenRouter API

### Frontend
- **react**: UI framework
- **typescript**: Type safety
- **vite**: Build tool

### Optional Enhancements
- **composio-core**: 1000+ app integrations ($25K prize!)
- **@copilotkit/react-core**: Embedded AI copilots
- **@vapi-ai/web**: Voice interface (free credits!)

## 🔐 Security

- CORS configured for localhost only
- Environment variables for sensitive keys
- No credentials in source code
- API key validation before requests

## 🐛 Troubleshooting

### Backend won't start
```bash
# Install missing packages
pip install -r requirements.txt

# Run with verbose output
uvicorn backend:app --reload --log-level debug
```

### Frontend shows "Failed to connect"
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `backend.py`
- Verify frontend is on `http://localhost:5173`

### No AI suggestions
- Check `.env` file exists and has `OPENROUTER_API_KEY`
- Verify you redeemed hackathon promo code at openrouter.ai/redeem
- Check $10 credits are available in OpenRouter dashboard
- Check internet connection
- See backend logs for errors

### OpenRouter API errors
- Verify API key is correct (starts with `sk-or-v1-`)
- Check you haven't exceeded $10 credit limit
- Try using a different model (check openrouter.ai/models)

## 📝 License

MIT License - Build whatever you want for the hackathon!

## 🤝 Hackathon Resources

See **[HACKATHON_README.md](../HACKATHON_README.md)** for:
- Complete sponsor tool integration guides
- Prize opportunities
- API key setup instructions
- Extension ideas

## 📚 Learn More

- [OpenRouter Docs](https://openrouter.ai/docs) - $10 free credits!
- [Composio Quickstart](https://docs.composio.dev/quickstart) - $25K prize!
- [CopilotKit Docs](https://docs.copilotkit.ai) - AI copilots
- [Vapi Docs](https://docs.vapi.ai) - Voice AI (free credits)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

---

**Built for OpenClaw Hackathon 2026** 🎉
