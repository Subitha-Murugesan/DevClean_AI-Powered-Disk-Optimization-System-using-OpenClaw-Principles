# DevClean React UI

A modern React frontend for the DevClean disk optimization backend.

## Overview

This is a beautiful, responsive UI that displays:
- **File Types Analysis**: Shows disk usage breakdown by file type (top 10)
- **Largest Folders**: Lists the biggest directories consuming disk space (top 10)
- **AI Suggestions**: Displays optimization recommendations from the AI assistant

## Features

✨ Modern, dark-themed UI  
📊 Interactive disk analysis visualization  
💡 AI-powered optimization suggestions  
📱 Fully responsive design  
⚡ Fast development with Vite  
🎨 TypeScript for type safety  

## Quick Start

### Prerequisites

- Node.js 16+
- The DevClean backend running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
npm run preview
```

## How to Use

1. Start the DevClean backend:
   ```bash
   cd devclean
   python3 -m pip install -r requirements.txt
   uvicorn backend:app --reload
   ```

2. Start the React frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Open `http://localhost:5173` in your browser

4. Click "Analyze Disk" button to scan your disk and get AI suggestions

## Architecture

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI (Python)
- **Communication**: REST API with CORS enabled
- **Styling**: Pure CSS with modern gradients and animations

## File Structure

```
frontend/
├── src/
│   ├── App.tsx          # Main component
│   ├── App.css          # Styling
│   ├── index.css        # Global styles
│   └── main.tsx         # Entry point
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## API Integration

The frontend connects to the backend's `/analyze` endpoint:

```
GET http://localhost:8000/analyze

Response:
{
  "analysis": {
    "file_types": {"extension": bytes, ...},
    "folders": {"path": bytes, ...}
  },
  "ai_suggestions": "string with recommendations"
}
```

## Environment Configuration

The frontend is configured to proxy API requests to `http://localhost:8000`. Modify `vite.config.ts` to change the backend URL if needed.

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## License

MIT
