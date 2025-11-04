# Mirror - AI-Powered Self-Awareness Journal

Mirror is an intelligent journaling application that functions as a "self-awareness mirror" - analyzing user journal entries to detect emotional patterns, cognitive biases, and behavioral trends.

## Features

- **Emotional Timeline**: Track your emotional journey over time with sentiment analysis
- **AI Weekly Summary**: Get "You in 7 Days" summaries with insights into your patterns
- **Cognitive Bias Detection**: Identify common cognitive distortions in your thinking
- **Interactive Visualizations**: Beautiful Plotly charts showing your emotional trajectory
- **Privacy First**: All processing done locally, no unnecessary data storage

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. Clone or navigate to the project directory:
```bash
cd Mirror
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download NLTK data for TextBlob:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('brown'); nltk.download('vader_lexicon')"
```

5. (Optional) Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings if needed
```

## Running the Application

### 🪞 Mirror

> **AI-Powered Self-Reflection Journal** - Transform your thoughts into insights

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

Mirror helps you understand your emotional patterns, detect cognitive biases, and track your personal growth through AI-powered sentiment analysis and beautiful visualizations.

---

## ✨ Features

- 📊 **Emotional Timeline** - Interactive charts showing your mood patterns
- 🧠 **AI Analysis** - Sentiment detection and cognitive bias identification  
- 📈 **Weekly Insights** - AI-generated summaries of your emotional journey
- 🎯 **Pattern Recognition** - Discover hidden connections in your thoughts
- 🔒 **Privacy First** - All data stored locally and encrypted

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm

### Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Download NLTK data
python download_nltk_data.py

# 3. Install frontend dependencies
cd frontend && npm install && cd ..
```

### Running the App

**Easiest way - Use start script:**

```bash
# Mac/Linux
./start.sh

# Windows
start.bat
```

**Or start services manually:**

```bash
# Terminal 1: API Server (port 5001)
python backend/api_server.py

# Terminal 2: Streamlit App (port 8501)  
streamlit run backend/app.py

# Terminal 3: Frontend (port 3000)
cd frontend && npm run build && cd ..
python backend/serve_react.py 3000
```

### Access

- 🌐 **Landing Page**: http://localhost:3000
- 📝 **Journal Dashboard**: http://localhost:8501  
- 🔌 **API**: http://localhost:5001

---

## 📁 Project Structure

```
Mirror/
├── backend/               # Python backend
│   ├── app.py            # Streamlit dashboard
│   ├── api_server.py     # Flask API  
│   ├── database.py       # SQLite database
│   ├── sentiment_analyzer.py
│   ├── bias_detector.py
│   └── visualization.py
│
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page views
│   │   └── utils/        # API utilities
│   └── package.json
│
├── docs/                 # Documentation
│   ├── DESIGN_SYSTEM.md  # UI/UX design rules
│   ├── QUICK_START.md    # Getting started guide
│   └── archive/          # Historical docs
│
├── mirror.db             # SQLite database
├── requirements.txt      # Python packages
├── start.sh / start.bat  # Launch scripts
└── README.md            # This file
```

---

## 🎯 How It Works

### 1. **Sign Up**
Create your profile with personalized questions (age, goals, journaling experience)

### 2. **Write**  
Express your thoughts freely in the journal - no judgment, just reflection

### 3. **Analyze**
AI analyzes your emotions, detects patterns, and identifies cognitive biases

### 4. **Grow**
Track your progress over time and gain insights into your emotional patterns

---

## 💻 Tech Stack

**Backend**
- Streamlit (Dashboard)
- Flask (API)
- SQLite (Database)
- VADER (Sentiment Analysis)
- Plotly (Visualization)

**Frontend**
- React 18
- Vite  
- TailwindCSS
- Fetch API

---

## 🎨 Key Features

### Emotional Analysis
Real-time sentiment analysis using VADER algorithm to understand your emotional state

### Cognitive Bias Detection
Identifies patterns like:
- Catastrophizing
- Black-and-white thinking
- Emotional reasoning
- Overgeneralization

### Interactive Visualizations  
Beautiful charts showing:
- Mood timeline
- Emotional volatility
- Bias frequency
- Weekly trends

### Weekly Summaries
AI-generated insights discovering:
- Dominant emotions
- Recurring themes
- Behavioral patterns
- Growth opportunities

---

## 📊 Database Schema

**users** - User profiles and onboarding data
**journal_entries** - Journal text with sentiment scores
**biases** - Detected cognitive patterns
**weekly_summaries** - AI-generated weekly insights

See `docs/DATABASE_SCHEMA.md` for details.

---

## 🔐 Privacy

- ✅ All data stored locally
- ✅ No external data transmission
- ✅ Encrypted at rest
- ✅ You own your data

---

## 🛠️ Troubleshooting

**Ports in use?**
```bash
lsof -ti:3000 | xargs kill -9
lsof -ti:5001 | xargs kill -9  
lsof -ti:8501 | xargs kill -9
```

**NLTK errors?**
```bash
python download_nltk_data.py
```

**Build issues?**
```bash
cd frontend
rm -rf node_modules && npm install
npm run build
```

---

## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.md)
- [Design System](docs/DESIGN_SYSTEM.md)
- [Setup Guide](docs/SETUP.md)
- [Restart Instructions](docs/RESTART_SERVER.md)

---

## 🤝 Contributing

Contributions welcome! Please fork, branch, and submit a PR.

---

## 📝 License

MIT License - see LICENSE file for details

---

## 📧 Support

Questions? Email [mirror2025@gmail.com](mailto:mirror2025@gmail.com)

---

**Built for self-awareness and personal growth** ✨
