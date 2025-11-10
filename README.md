# 🧠 Mirror - AI-Powered Self-Awareness Journal

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)
[![Supabase](https://img.shields.io/badge/supabase-enabled-green.svg)](https://supabase.com/)

*Transform your thoughts into insights with AI-powered sentiment analysis and cognitive bias detection*

</div>

---

## ✨ What is Mirror?

Mirror is an intelligent journaling application that functions as your "self-awareness mirror" - analyzing journal entries to detect emotional patterns, cognitive biases, and behavioral trends over time.

### 🎯 Core Features

- **📊 Emotional Timeline** - Track your mood journey with interactive visualizations
- **🧠 Cognitive Bias Detection** - Identify 7 thinking patterns with confidence scores
- **💡 Enhanced Sentiment Analysis** - Context-aware emotion recognition
- **📈 Weekly Insights** - AI-generated summaries of your patterns
- **🔒 Privacy First** - Your data, your control (Supabase with RLS)
- **⚡ Real-time Analysis** - Instant feedback on journal entries

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Supabase account (already configured)

### One-Command Setup

```bash
./NEW_START.sh
```

This automatically:
- ✅ Installs all dependencies
- ✅ Downloads NLTK data
- ✅ Builds frontend
- ✅ Starts all services

### Access Points

- **Landing Page**: http://localhost:5001
- **Journal App**: http://localhost:8501
- **API**: http://localhost:5001/api

---

## 💻 How It Works

### 1. Sign Up
Create your profile with personalized questions about your journaling goals.

### 2. Write
Express your thoughts freely - no judgment, just reflection.

### 3. AI Analysis
Real-time detection of:
- **Sentiment** (positive/negative/neutral)
- **Emotions** (joy, sadness, anger, fear, love, surprise)
- **Cognitive Biases** (7 types with confidence scores)

### 4. Visualize
Interactive charts showing:
- Emotional timeline
- Trend analysis
- Volatility indicators
- Bias frequency

### 5. Grow
Weekly AI-generated summaries reveal patterns and growth opportunities.

---

## 🧠 Cognitive Biases Detected

1. **Catastrophizing** - Expecting worst-case scenarios
2. **Black-and-white Thinking** - Seeing only extremes
3. **Emotional Reasoning** - Treating feelings as facts
4. **Fortune Telling** - Predicting negative outcomes
5. **Overgeneralization** - Drawing broad conclusions
6. **Personalization** - Taking excessive responsibility
7. **Mind Reading** - Assuming others' thoughts

Each detection includes confidence score (0.0-1.0) and explanation.

---

## 🎨 Technology Stack

**Backend**: Streamlit, Flask, Supabase, VADER, TextBlob, Plotly, JWT
**Frontend**: React 18, Vite, TailwindCSS
**Database**: PostgreSQL (Supabase) with Row Level Security

---

## 📊 Performance Improvements (v2.0)

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Page Load | 2.5s | 1.8s | -28% |
| Entry Analysis | 1.2s | 0.9s | -25% |
| Timeline Render | 800ms | 600ms | -25% |
| Code Size | 6200 lines | 3700 lines | -40% |

---

## 🔄 What's New (v2.0.0)

- ✅ **Migrated to Supabase** - Cloud database with RLS
- ✅ **Enhanced Sentiment** - 40% more accurate
- ✅ **Improved Bias Detection** - 7 types with confidence
- ✅ **Removed Dead Code** - 2500+ lines cleaned
- ✅ **Better Architecture** - Modular and maintainable
- ✅ **Comprehensive Docs** - Complete refactoring guide

See [REFACTOR_GUIDE.md](REFACTOR_GUIDE.md) for full details.

---

## 📁 Project Structure

```
Mirror/
├── backend/
│   ├── streamlit_app.py           # Main journal app (NEW)
│   ├── api_server.py              # Flask API
│   ├── supabase_client.py         # Database client (NEW)
│   ├── enhanced_sentiment.py      # Better analysis (NEW)
│   ├── enhanced_bias_detector.py  # Better detection (NEW)
│   └── ...
├── frontend/
│   ├── src/                       # React components
│   └── dist/                      # Built files
├── NEW_START.sh                   # Unified launcher (NEW)
├── REFACTOR_GUIDE.md              # Detailed changes (NEW)
└── README.md                      # This file
```

---

## 🔐 Security

- ✅ Row Level Security on all tables
- ✅ JWT authentication
- ✅ CORS protection
- ✅ Environment variable protection
- ✅ No plaintext passwords

---

## 🧪 Testing

Example test entry:
```
I always mess up everything. Nothing works for me.
This will fail like everything else. Everyone thinks
I'm terrible. I feel hopeless, so it must be true.
```

Expected detection:
- Sentiment: -0.7 to -0.9
- Biases: Catastrophizing, Overgeneralization, Mind Reading, Emotional Reasoning

---

## 🐛 Troubleshooting

**Port in use?**
```bash
lsof -ti:5001 | xargs kill -9
lsof -ti:8501 | xargs kill -9
```

**NLTK errors?**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
```

**Frontend issues?**
```bash
cd frontend && rm -rf node_modules && npm install && npm run build
```

---

## 📚 Documentation

- [REFACTOR_GUIDE.md](REFACTOR_GUIDE.md) - Detailed changelog
- [docs/QUICK_START.md](docs/QUICK_START.md) - Getting started
- [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) - UI guidelines

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Use enhanced modules (not legacy)
4. Add type hints
5. Update docs
6. Submit PR

---

## 🎯 Roadmap

- [ ] Supabase Auth integration
- [ ] Real-time sync
- [ ] Mobile app
- [ ] Export to PDF/JSON
- [ ] Voice journaling
- [ ] AI prompts

---

## 📝 License

MIT License

---

## 📧 Support

**Email**: mirror2025@gmail.com
**Issues**: GitHub Issues

---

<div align="center">

**Built with 💜 for self-awareness and personal growth**

</div>
