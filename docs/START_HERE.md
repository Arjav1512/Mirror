# Mirror - Quick Start Guide

Welcome to **Mirror**, your philosophical self-awareness journal with a modern minimalist design.

## 🎨 What's New

The entire UI/UX has been redesigned with a **philosophical minimalist theme**:

- **Clean Typography**: Crimson Pro serif for philosophical elements, Inter sans-serif for UI
- **Minimalist Color Palette**: Neutral grays with black accents  
- **Philosophical Quotes**: Daily rotating wisdom on login screens
- **Refined Interactions**: Subtle borders, clean lines, thoughtful spacing
- **Zero Errors**: All features tested and working seamlessly

---

## 🚀 Quick Start (Recommended)

Run this single command to start everything:

```bash
./start.sh
```

This will:
1. ✅ Install Python dependencies
2. ✅ Download NLTK data
3. ✅ Install Node.js dependencies  
4. ✅ Build React frontend
5. ✅ Start API server (port 5001)
6. ✅ Start landing page server (port 5000)
7. ✅ Start Streamlit journal (port 8501)

### Access Points

- **Landing Page**: http://localhost:5000 (signup/onboarding)
- **Journal App**: http://localhost:8501 (main application)
- **API Server**: http://localhost:5001 (backend)

---

## 📝 Manual Setup (Alternative)

### 1. Install Dependencies

```bash
# Install Python packages
pip3 install -r requirements.txt

# Download NLTK data
python3 download_nltk_data.py

# Install Node.js packages and build frontend
cd frontend
npm install
npm run build
cd ..
```

### 2. Start Servers

**Terminal 1 - API Server:**
```bash
cd backend
python api_server.py
```

**Terminal 2 - Landing Page:**
```bash
cd backend
python serve_react.py 5000
```

**Terminal 3 - Streamlit App:**
```bash
cd backend
streamlit run app.py
```

---

## 🎯 How to Use Mirror

### First Time Setup

1. **Visit Landing Page**: Go to http://localhost:5000
2. **Read Philosophy**: Each visit shows a different philosophical quote
3. **Create Account**: Fill in the minimalist signup form
4. **Automatic Redirect**: You'll be redirected to the journal app

### Using the Journal

1. **Sign In**: Use your email (if not already logged in)
2. **New Entry Tab**: Write your thoughts in the elegant text area
3. **Sentiment Analysis**: Automatically detects your emotional state
4. **Cognitive Patterns**: Identifies thinking biases to boost self-awareness
5. **Timeline Tab**: View your emotional journey with clean Plotly charts
6. **Weekly Summary**: Generate AI-powered insights into your patterns
7. **Insights Tab**: Explore cognitive bias detections over time

---

## 🎨 Design Philosophy

The redesign follows these principles:

### Visual Design
- **Minimalism**: Clean lines, subtle borders, ample whitespace
- **Typography Hierarchy**: Crimson Pro for philosophical content, Inter for UI
- **Monochromatic Palette**: Neutral grays (#1a1a1a to #fafafa)
- **Subtle Interactions**: 1-2px borders, minimal shadows
- **Philosophical Elements**: Daily rotating quotes from great thinkers

### User Experience
- **Contemplative Pace**: Slower animations, thoughtful transitions
- **Focus on Content**: Minimal distractions, content-first approach
- **Accessible**: High contrast, readable fonts, clear hierarchy
- **Consistent**: Unified theme across all components

---

## 🔧 Features

### ✨ Core Features

- **📝 Journal Entries**: Clean text area with serif font for writing
- **😊 Sentiment Analysis**: TextBlob + VADER for accurate emotion detection
- **🧠 Bias Detection**: Identifies cognitive distortions in your thinking
- **📊 Emotional Timeline**: Interactive Plotly charts with minimalist styling
- **📈 Weekly Summaries**: AI-generated insights (rule-based, no API needed)
- **🔒 Privacy First**: All data stored locally in SQLite

### 🎨 UI Enhancements

- **Philosophical Quotes**: Rotating wisdom from Socrates, Aristotle, Buddha, Marcus Aurelius
- **Clean Forms**: Minimalist inputs with subtle focus states
- **Refined Cards**: Bordered containers with clean typography
- **Elegant Tabs**: Underline-style navigation with uppercase labels
- **Sophisticated Metrics**: Large serif numbers, small sans-serif labels

---

## 📁 Project Structure

```
Mirror/
├── backend/              # Python backend
│   ├── app.py           # Streamlit app (redesigned)
│   ├── api_server.py    # Flask API
│   ├── database.py      # SQLite operations
│   ├── sentiment_analyzer.py  # TextBlob + VADER
│   ├── bias_detector.py       # Cognitive bias detection
│   ├── visualization.py       # Plotly charts (styled)
│   └── summary_generator.py   # Weekly summaries
├── frontend/            # React landing page
│   ├── src/
│   │   ├── components/  # Redesigned components
│   │   │   ├── Hero.jsx        # Minimalist hero
│   │   │   ├── HowItWorks.jsx  # Feature cards
│   │   │   ├── SignupForm.jsx  # Clean signup
│   │   │   └── Footer.jsx      # Refined footer
│   │   └── index.css   # Crimson Pro + Inter fonts
│   └── dist/           # Built files (auto-generated)
├── mirror.db           # SQLite database
├── requirements.txt    # Python dependencies
└── download_nltk_data.py  # NLTK data downloader
```

---

## 🐛 Troubleshooting

### Port Already in Use

If you see "Address already in use" errors:

```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Find and kill process on port 5001
lsof -ti:5001 | xargs kill -9

# Find and kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

### NLTK Data Missing

If you see NLTK-related errors:

```bash
python3 download_nltk_data.py
```

### Frontend Not Building

If React build fails:

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Database Issues

To reset the database (⚠️ deletes all data):

```bash
rm mirror.db
# Database will be recreated automatically on next run
```

---

## 📚 Tech Stack

### Backend (Python)
- **Streamlit**: Journal interface with custom CSS
- **Flask**: REST API for signup
- **SQLite**: Local database
- **TextBlob & VADER**: Sentiment analysis
- **Plotly**: Interactive charts
- **Pandas**: Data processing

### Frontend (React)
- **React**: Landing page components
- **Vite**: Build tool
- **Tailwind CSS**: Utility-first styling
- **Crimson Pro**: Serif font for philosophical content
- **Inter**: Sans-serif font for UI elements

---

## 🎨 Color Palette

```css
/* Neutral Palette */
--neutral-900: #1a1a1a;  /* Primary text, buttons */
--neutral-600: #666666;  /* Secondary text */
--neutral-200: #e5e5e5;  /* Borders */
--neutral-50:  #fafafa;  /* Backgrounds */

/* Accent Colors */
--positive:    #059669;  /* Green for positive sentiment */
--negative:    #dc2626;  /* Red for negative sentiment */
--warning:     #d97706;  /* Amber for cognitive biases */
```

---

## 📖 Philosophy

> "The unexamined life is not worth living." — Socrates

Mirror is built on the belief that self-awareness comes through reflection. The minimalist design creates space for contemplation, while AI-powered analysis reveals patterns you might not see on your own.

---

## 📫 Support

For questions or issues:
- Email: mirror2025@gmail.com
- Check logs: `api.log`, `landing.log`

---

## 🎉 You're All Set!

Start your journey of self-reflection:

```bash
./start.sh
```

Then visit **http://localhost:5000** to begin.

---

**Built with philosophy. Designed for reflection. Made with ❤️**
