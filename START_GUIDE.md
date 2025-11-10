# 🚀 Mirror - Foolproof Startup Guide

## Quick Start (Recommended)

### One-Command Start

```bash
./NEW_START.sh
```

**That's it!** The script will:
1. ✅ Check all prerequisites
2. ✅ Install dependencies automatically
3. ✅ Kill any processes blocking ports
4. ✅ Start all services in correct order
5. ✅ Open browser automatically

---

## Step-by-Step Manual Start

If you prefer to start services manually:

### 1. Prerequisites Check

```bash
# Check Python (need 3.8+)
python3 --version

# Check Node.js (need 16+)
node --version

# Check npm
npm --version
```

### 2. Install Dependencies (First Time Only)

```bash
# Install Python packages
pip3 install -r requirements.txt

# Download NLTK data
python3 -c "import nltk; nltk.download('punkt'); nltk.download('brown'); nltk.download('vader_lexicon')"

# Install Node packages and build
cd frontend
npm install
npm run build
cd ..
```

### 3. Clear Ports (If Needed)

```bash
# Kill any processes on our ports
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:8501 | xargs kill -9 2>/dev/null
```

### 4. Start Services

**Terminal 1 - API Server:**
```bash
cd backend
python3 api_server.py
```

**Terminal 2 - Streamlit App:**
```bash
cd backend
streamlit run streamlit_app.py
```

### 5. Open Browser

- **Landing Page:** http://localhost:5001
- **Journal App:** http://localhost:8501

---

## Common Issues & Solutions

### Issue 1: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Kill processes on ports
lsof -ti:5001 | xargs kill -9
lsof -ti:8501 | xargs kill -9

# Wait 2 seconds
sleep 2

# Restart services
./NEW_START.sh
```

### Issue 2: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'supabase'`

**Solution:**
```bash
# Reinstall dependencies
pip3 install -r requirements.txt

# Or install supabase specifically
pip3 install supabase>=2.0.0
```

### Issue 3: NLTK Data Missing

**Error:** `Resource punkt not found`

**Solution:**
```bash
python3 -c "import nltk; nltk.download('punkt'); nltk.download('brown'); nltk.download('vader_lexicon')"
```

### Issue 4: Frontend Not Building

**Error:** Frontend dist folder missing

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
cd ..
```

### Issue 5: Supabase Connection Error

**Error:** `Supabase credentials not found`

**Solution:**
```bash
# Verify .env file exists
cat .env

# Should show:
# VITE_SUPABASE_URL=https://...
# VITE_SUPABASE_ANON_KEY=...

# If missing, contact administrator
```

### Issue 6: Page Not Loading

**Error:** Blank page or "Cannot connect"

**Solution:**
```bash
# Check if services are running
ps aux | grep python3
ps aux | grep streamlit

# Check logs
tail -f api.log
tail -f streamlit.log

# Restart everything
./NEW_START.sh
```

---

## Browser Access

### Correct URLs

✅ **Landing Page:** http://localhost:5001
✅ **Journal App:** http://localhost:8501

### Incorrect URLs (Don't Use)

❌ http://localhost:3000 (old dev server)
❌ http://localhost:5000 (old landing)
❌ http://127.0.0.1:5001 (use localhost instead)

---

## Testing the Installation

### Quick Test

1. **Start services:**
   ```bash
   ./NEW_START.sh
   ```

2. **Open browser to:** http://localhost:5001

3. **Test signup:**
   - Fill in the form
   - Click "Start Reflecting"
   - Should redirect to journal app

4. **Test journal:**
   - Write a test entry
   - Click "Save & Analyze"
   - Should show sentiment and biases

5. **Verify timeline:**
   - Should see emotional timeline chart
   - Check cognitive patterns section

---

## Automated Startup Script

The `NEW_START.sh` script handles everything:

```bash
#!/bin/bash
# Features:
# - Checks prerequisites
# - Installs dependencies
# - Clears ports automatically
# - Starts services in order
# - Shows clear status messages
# - Keeps running until Ctrl+C
```

**Usage:**
```bash
# Make executable (first time)
chmod +x NEW_START.sh

# Run it
./NEW_START.sh

# Stop it
# Press Ctrl+C
```

---

## Development Mode

For development with hot reloading:

**Terminal 1 - API:**
```bash
cd backend
python3 api_server.py
```

**Terminal 2 - Streamlit:**
```bash
cd backend
streamlit run streamlit_app.py
```

**Terminal 3 - Frontend Dev (Optional):**
```bash
cd frontend
npm run dev
# Access at http://localhost:3000
```

---

## Production Deployment

For production servers:

```bash
# Install dependencies
pip3 install -r requirements.txt
cd frontend && npm install && npm run build && cd ..

# Start with nohup (keeps running after logout)
nohup python3 backend/api_server.py > api.log 2>&1 &
nohup streamlit run backend/streamlit_app.py --server.port 8501 --server.headless true > streamlit.log 2>&1 &

# Check status
ps aux | grep python3

# Stop services
pkill -f api_server.py
pkill -f streamlit
```

---

## Environment Variables

Create `.env` in project root:

```env
# Supabase Configuration (Required)
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here

# JWT Secret (Optional - has default)
JWT_SECRET=your-secret-key-here

# Service URLs (Optional - has defaults)
STREAMLIT_URL=http://localhost:8501
LANDING_PAGE_URL=http://localhost:5001
```

---

## Logs & Debugging

### View Logs

```bash
# API Server logs
tail -f api.log

# Streamlit logs
tail -f streamlit.log

# Watch both
tail -f api.log streamlit.log
```

### Debug Mode

```bash
# Enable debug output
export DEBUG=1

# Run with verbose output
python3 backend/api_server.py
```

---

## Performance Tips

### Speed Up Startup

1. **Keep services running** - Don't restart unless needed
2. **Use the unified script** - It's optimized
3. **Pre-install dependencies** - Do once, use forever

### Reduce Memory Usage

```bash
# Close unused applications
# Check memory usage
free -h

# If low on memory, restart services one at a time
```

---

## Troubleshooting Checklist

Run through this if anything fails:

```bash
# 1. Check Python version
python3 --version  # Should be 3.8+

# 2. Check Node version
node --version     # Should be 16+

# 3. Check dependencies
pip3 list | grep supabase
pip3 list | grep streamlit

# 4. Check ports
lsof -i :5001
lsof -i :8501

# 5. Check .env file
cat .env

# 6. Check frontend build
ls -la frontend/dist/

# 7. Run startup script
./NEW_START.sh
```

---

## Getting Help

If you still have issues:

1. **Check logs:**
   ```bash
   cat api.log
   cat streamlit.log
   ```

2. **Check this guide:** Review relevant sections above

3. **Check docs:**
   - README.md
   - REFACTOR_GUIDE.md

4. **Contact support:** mirror2025@gmail.com

---

## Success Indicators

You know everything is working when:

✅ No error messages in terminal
✅ Both services show "Running on http://..."
✅ Browser opens to landing page automatically
✅ Landing page loads completely
✅ Signup form is visible
✅ Can create account
✅ Redirects to journal app after signup
✅ Can write and save journal entries
✅ Timeline chart displays correctly
✅ Cognitive patterns are detected

---

## Quick Reference

| Action | Command |
|--------|---------|
| Start Everything | `./NEW_START.sh` |
| Stop Everything | `Ctrl+C` |
| Clear Ports | `lsof -ti:5001,8501 \| xargs kill -9` |
| View Logs | `tail -f *.log` |
| Reinstall Deps | `pip3 install -r requirements.txt` |
| Rebuild Frontend | `cd frontend && npm run build` |
| Check Status | `ps aux \| grep python3` |

---

**Last Updated:** 2025-11-10
**Works With:** Mirror v2.0.0
