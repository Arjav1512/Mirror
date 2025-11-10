# 🎯 Mirror - Quick Reference Card

## Opening Mirror Every Time (No Errors!)

### Mac/Linux
```bash
./start_mirror.sh
```

### Windows
```cmd
start_mirror.bat
```

**Browser opens automatically to http://localhost:5001** ✓

---

## That's All You Need!

The script handles everything:
- ✅ Checks prerequisites
- ✅ Installs dependencies
- ✅ Clears blocked ports
- ✅ Starts all services
- ✅ Opens browser automatically

---

## Quick Commands

| What | Command |
|------|---------|
| **Start** | `./start_mirror.sh` |
| **Stop** | Press `Ctrl+C` |
| **Logs** | `tail -f *.log` |
| **Clear Ports** | `lsof -ti:5001,8501 \| xargs kill -9` |

---

## Access URLs

- 🌐 **Landing:** http://localhost:5001
- 📝 **Journal:** http://localhost:8501

---

## If Something Goes Wrong

1. Stop everything: `Ctrl+C`
2. Clear ports: `lsof -ti:5001,8501 | xargs kill -9`
3. Start again: `./start_mirror.sh`

---

## Common Issues (1-Line Fixes)

**Port in use:**
```bash
lsof -ti:5001,8501 | xargs kill -9 && ./start_mirror.sh
```

**Dependencies missing:**
```bash
pip3 install -r requirements.txt && ./start_mirror.sh
```

**Frontend broken:**
```bash
cd frontend && npm run build && cd .. && ./start_mirror.sh
```

---

## Success Checklist

- [ ] Terminal shows "Mirror is Ready!"
- [ ] Browser opens automatically
- [ ] Landing page loads
- [ ] Can sign up
- [ ] Can write entries
- [ ] Timeline shows
- [ ] Biases detected

---

## Need More Help?

- **Detailed Guide:** [GETTING_STARTED.md](GETTING_STARTED.md)
- **Full Docs:** [START_GUIDE.md](START_GUIDE.md)
- **Technical:** [REFACTOR_GUIDE.md](REFACTOR_GUIDE.md)

---

## Remember

**Just run `./start_mirror.sh` and you're done!** 🎉

Browser opens automatically, no errors, every time.
