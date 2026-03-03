# 🎯 OpenClaw Hackathon Quick Start

## ⚡ Fast Track (5 minutes)

### Step 1: Get Your Free OpenRouter API Key
1. Create account: https://openrouter.ai
2. Redeem $10 credits: https://openrouter.ai/redeem
   - Use your city's promo code (ask your chapter leader!)
   - ⚠️ **Expires March 1, 2026** - redeem now!
3. Copy your API key from the dashboard

### Step 2: Configure Environment
```bash
cd devclean
cp .env.example .env
nano .env  # or use any text editor
```

Add your key:
```
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE
```

### Step 3: Install Dependencies

**Backend:**
```bash
cd devclean
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Step 4: Run It!

**Terminal 1 - Backend:**
```bash
cd devclean
uvicorn backend:app --reload
```
Wait for: `✅ Application startup complete.`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Wait for: `✅ Local: http://localhost:5173/`

### Step 5: Test It!
1. Open http://localhost:5173
2. Click "Analyze Disk"
3. See AI recommendations! 🎉

---

## 🏆 Level Up Your Hack

### Add Composio ($25K Prize!)
**What**: Give your AI agent real tools to execute cleanup
**Prize**: Top team gets $25,000 in credits + feature interview

```bash
pip install composio-core
export COMPOSIO_API_KEY=your_key  # from platform.composio.dev
```

### Add CopilotKit (AI Chat UI)
**What**: Embed AI chat directly in your React UI

```bash
cd frontend
npm install @copilotkit/react-core @copilotkit/react-ui
```

### Add Vapi Voice (Free Credits!)
**What**: "Hey DevClean, what's using my disk space?"

```bash
npm install @vapi-ai/web
```
Use code `Openclaw022026` at dashboard.vapi.ai for free credits

---

## 🐛 Common Issues

### "No module named 'fastapi'"
```bash
cd devclean
pip install -r requirements.txt
```

### "Command 'uvicorn' not found"
```bash
pip install uvicorn
```

### "Failed to fetch analysis"
- Backend running? Check Terminal 1
- Should see: `INFO: Uvicorn running on http://127.0.0.1:8000`
- Try: http://localhost:8000/docs (should show API docs)

### "No AI suggestions"
- Did you add `OPENROUTER_API_KEY` to `.env`?
- Did you redeem your hackathon promo code?
- Check $10 credits at openrouter.ai/dashboard
- Check backend terminal for error messages

### "npm install fails"
- Try: `rm -rf node_modules package-lock.json`
- Then: `npm install` again
- Or use: `npm install --legacy-peer-deps`

---

## 🎨 Customization Ideas

### Change AI Model
Edit `devclean/backend.py`:
```python
"model": "anthropic/claude-3-haiku",  # Faster & cheaper
# or
"model": "openai/gpt-4-turbo",  # More powerful
```
Browse 300+ models at: https://openrouter.ai/models

### Analyze Different Paths
Edit `devclean/backend.py`:
```python
@app.get("/analyze")
def analyze(path: str = "."):
    data = analyze_disk(path)
    ...
```

Then call: `http://localhost:8000/analyze?path=/home/user/projects`

### Add Real Cleanup Actions
With Composio, give your agent shell access:
```python
from composio import Composio
composio = Composio(api_key=COMPOSIO_API_KEY)
tools = composio.get_tools(actions=["SHELL_EXEC_COMMAND"])

# Agent can now: rm *.log, docker system prune, etc.
```

---

## 📚 Resources

### Hackathon Sponsors
- **OpenRouter**: https://openrouter.ai/docs
- **Composio**: https://docs.composio.dev/quickstart
- **CopilotKit**: https://docs.copilotkit.ai
- **Vapi**: https://docs.vapi.ai
- **Auth0**: https://auth0.com/docs/ai
- **ElevenLabs**: https://elevenlabs.io/docs

### Tech Stack
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **Vite**: https://vitejs.dev/

---

## 💪 Pro Tips

1. **Save Your Credits**: Use `gpt-4o-mini` (default) - costs ~$0.15/1M tokens
2. **Speed Up**: Cache AI responses in memory for repeated queries
3. **Show Impact**: Display "X GB freed" after cleanup
4. **Make it Visual**: Charts.js or Recharts for disk usage graphs
5. **Go Multi-User**: Add Auth0 for team disk tracking
6. **Add Voice**: Vapi for "Tell me what to delete"
7. **Real Cleanup**: Composio to actually execute rm/docker commands

---

## 🎯 Judging Criteria Alignment

### Innovation
- ✅ AI-powered disk analysis
- 💡 Add: Voice interface (Vapi) or real-time cleanup (Composio)

### Technical Implementation
- ✅ Full-stack (React + FastAPI)
- 💡 Add: Advanced features (streaming, websockets, auth)

### Use of Sponsor Tools
- ✅ OpenRouter for AI
- 💡 Add: Composio ($25K prize!), CopilotKit, or Vapi

### Practicality
- ✅ Solves real problem (disk space)
- 💡 Add: Scheduled cleanup, notifications, team dashboards

---

## 🚀 Next Steps

1. ✅ Get basic app running
2. 🎨 Customize UI/styling
3. 🔧 Add sponsor tool (Composio/CopilotKit/Vapi)
4. 🧪 Test with real data
5. 📹 Record demo video
6. 🎉 Submit your hack!

---

**Questions?** Check:
- [HACKATHON_README.md](HACKATHON_README.md) - Full guide
- [devclean/README.md](devclean/README.md) - Technical docs
- Message Board on hackathon platform
- Your chapter leader

**Good luck! 🎉**
