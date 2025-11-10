# 🚀 Getting Started with Mirror

## The Easiest Way to Open Mirror Every Time

### For Mac/Linux Users

```bash
./start_mirror.sh
```

**That's it!** The script will:
- ✅ Install all dependencies automatically
- ✅ Clear any blocking ports
- ✅ Start all services
- ✅ **Open your browser automatically to http://localhost:5001**
- ✅ Keep everything running smoothly

### For Windows Users

```cmd
start_mirror.bat
```

**Done!** The batch file will:
- ✅ Install dependencies
- ✅ Clear ports
- ✅ Start services
- ✅ **Open your browser automatically**

---

## First Time Setup (One Time Only)

### 1. Make Scripts Executable (Mac/Linux)

```bash
chmod +x start_mirror.sh
chmod +x NEW_START.sh
```

### 2. That's All!

No other setup needed. The scripts handle everything.

---

## Access Points

Once started, open these URLs:

| Service | URL | Description |
|---------|-----|-------------|
| **Landing Page** | http://localhost:5001 | Sign up here |
| **Journal App** | http://localhost:8501 | Main journaling interface |

---

## What Happens When You Start

1. **Prerequisites Check** ✓
   - Verifies Python 3.8+
   - Verifies Node.js 16+

2. **Dependencies Install** ✓
   - Installs Python packages
   - Downloads NLTK data
   - Installs Node packages
   - Builds React frontend

3. **Port Management** ✓
   - Clears ports 5001 and 8501
   - Ensures no conflicts

4. **Service Startup** ✓
   - Starts API Server (Flask)
   - Starts Journal App (Streamlit)

5. **Browser Launch** ✓
   - Automatically opens http://localhost:5001
   - Ready to sign up!

---

## Quick Start Workflow

### Step 1: Start the Application

```bash
# Mac/Linux
./start_mirror.sh

# Windows
start_mirror.bat
```

### Step 2: Sign Up

1. Browser opens automatically to **http://localhost:5001**
2. Fill in the signup form:
   - Name and email
   - Age group and occupation
   - Journaling experience
   - Primary goals
3. Click **"Start Reflecting"**

### Step 3: Start Journaling

1. Automatically redirected to **http://localhost:8501**
2. Write your first entry
3. Click **"Save & Analyze"**
4. See instant AI insights!

---

## Stopping the Application

### Mac/Linux

Press **Ctrl+C** in the terminal

Or run:
```bash
# Find process IDs
ps aux | grep python3

# Kill specific processes
kill <PID>
```

### Windows

Close the command window

Or run:
```cmd
# Find and kill processes
netstat -aon | findstr :5001
netstat -aon | findstr :8501
taskkill /F /PID <PID>
```

---

## Troubleshooting

### Problem: Script won't run

**Mac/Linux:**
```bash
# Make executable
chmod +x start_mirror.sh

# Try again
./start_mirror.sh
```

**Windows:**
```cmd
# Run as Administrator (right-click → Run as Administrator)
start_mirror.bat
```

### Problem: Port already in use

**Mac/Linux:**
```bash
# Kill all processes on our ports
lsof -ti:5001,8501 | xargs kill -9

# Start again
./start_mirror.sh
```

**Windows:**
```cmd
# Kill processes
for /f "tokens=5" %a in ('netstat -aon ^| findstr :5001') do taskkill /F /PID %a
for /f "tokens=5" %a in ('netstat -aon ^| findstr :8501') do taskkill /F /PID %a

# Start again
start_mirror.bat
```

### Problem: Browser doesn't open

**Solution:** Manually open your browser to:
- http://localhost:5001 (Landing page)
- http://localhost:8501 (Journal app)

### Problem: Blank page or errors

**Check logs:**
```bash
# View API logs
cat api.log

# View Streamlit logs
cat streamlit.log

# Watch logs live
tail -f api.log streamlit.log
```

**Common fixes:**
```bash
# Reinstall dependencies
pip3 install -r requirements.txt

# Rebuild frontend
cd frontend && npm run build && cd ..

# Restart everything
./start_mirror.sh
```

---

## Alternative Start Methods

### Method 1: Enhanced Script (Recommended)
```bash
./start_mirror.sh  # Auto-opens browser
```

### Method 2: Original Script
```bash
./NEW_START.sh     # Manual browser open
```

### Method 3: Manual Start
```bash
# Terminal 1
cd backend && python3 api_server.py

# Terminal 2
cd backend && streamlit run streamlit_app.py

# Then open http://localhost:5001
```

---

## Development Mode

For development with code changes:

```bash
# Start with hot reload (frontend)
cd frontend
npm run dev  # Port 3000

# In another terminal
cd backend
python3 api_server.py  # Port 5001

# In another terminal
cd backend
streamlit run streamlit_app.py  # Port 8501
```

---

## Verifying Everything Works

### Checklist

- [ ] Terminal shows "Mirror is Ready!"
- [ ] Browser opens automatically
- [ ] Landing page loads (http://localhost:5001)
- [ ] Signup form is visible
- [ ] Can create account
- [ ] Redirects to journal app after signup
- [ ] Can write and save entries
- [ ] Timeline chart displays
- [ ] Cognitive patterns detected

### Test Entry

Try this to test AI features:

```
I always mess up everything I do. Nothing ever works out for me.
This is definitely going to fail just like everything else.
I can tell everyone thinks I'm terrible at this. I feel hopeless,
so it must be true that I can't succeed.
```

**Expected Results:**
- Sentiment: Negative (-0.7 to -0.9)
- Emotions: Sadness detected
- Biases: 4-5 patterns detected
  - Catastrophizing (high confidence)
  - Overgeneralization
  - Mind Reading
  - Emotional Reasoning

---

## Quick Reference

| What You Want | Command |
|---------------|---------|
| Start everything | `./start_mirror.sh` |
| Stop everything | `Ctrl+C` |
| View logs | `tail -f *.log` |
| Clear ports | `lsof -ti:5001,8501 \| xargs kill -9` |
| Rebuild frontend | `cd frontend && npm run build` |
| Reinstall Python | `pip3 install -r requirements.txt` |

---

## URLs Quick Reference

| Service | URL | Use For |
|---------|-----|---------|
| Landing | http://localhost:5001 | Signup |
| Journal | http://localhost:8501 | Writing |
| API | http://localhost:5001/api | Backend |

---

## What If Nothing Works?

### Nuclear Option (Start Fresh)

```bash
# 1. Stop everything
pkill -f python3
pkill -f streamlit

# 2. Clean everything
rm -rf frontend/node_modules
rm -rf frontend/dist
pip3 uninstall -y -r requirements.txt

# 3. Reinstall
pip3 install -r requirements.txt
cd frontend && npm install && npm run build && cd ..

# 4. Start fresh
./start_mirror.sh
```

---

## Getting Help

1. **Check this guide** - Most issues covered above
2. **Check logs** - `cat api.log streamlit.log`
3. **Check docs** - See [START_GUIDE.md](START_GUIDE.md)
4. **Contact support** - mirror2025@gmail.com

---

## Success Indicators

You'll know it's working when:

1. ✅ No red error messages in terminal
2. ✅ See "Mirror is Ready!" message
3. ✅ Browser opens automatically
4. ✅ Landing page loads with signup form
5. ✅ Can create account and login
6. ✅ Journal app works smoothly

---

## Pro Tips

### Tip 1: Keep It Running

Once started, you can minimize the terminal. Everything keeps running.

### Tip 2: Bookmark URLs

Bookmark these for quick access:
- http://localhost:5001
- http://localhost:8501

### Tip 3: Check Logs

If something seems off:
```bash
tail -f api.log streamlit.log
```

### Tip 4: Restart When Needed

If you modify backend code:
```bash
Ctrl+C
./start_mirror.sh
```

### Tip 5: Use Tab Completion

Most shells support tab completion:
```bash
./start<TAB>  # Completes to ./start_mirror.sh
```

---

## Next Steps

Once you have Mirror running:

1. **Create your first entry** - Share your thoughts
2. **Review AI insights** - See detected emotions
3. **Check timeline** - Visualize your emotional journey
4. **Generate weekly summary** - Get pattern analysis

---

**Remember:** Just run `./start_mirror.sh` and your browser opens automatically!

**That's all you need to know!** 🎉

---

**Last Updated:** 2025-11-10
**Works With:** Mirror v2.0.0
