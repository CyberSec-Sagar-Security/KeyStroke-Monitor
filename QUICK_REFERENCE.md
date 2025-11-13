# 🎯 KEYSTROKE - QUICK REFERENCE CARD

## 🚀 Quick Start (3 Commands)
```powershell
cd "d:\CyberSecurity\Cyber_Security_Future_Projects\Keylogger"
pip install -r requirements.txt
python keystroke.py
```

## 📋 All Features At A Glance

| Feature | Level | Working | Command/Menu |
|---------|-------|---------|--------------|
| Key Recording | Basic | ✅ | Auto-captures |
| Timestamp Logging | Basic | ✅ | Auto-captures |
| Session Management | Basic | ✅ | Menu [1] |
| Window Tracking | Medium | ✅ | Auto-captures |
| Log Storage (JSON/TXT) | Basic | ✅ | Auto-saves |
| Log Rotation | Medium | ✅ | Settings [2] |
| Encryption | Medium | ✅ | Settings [1] |
| Backspace Tracking | Basic | ✅ | Auto-captures |
| Word Count | Basic | ✅ | Shows in stats |
| Typing Speed (WPM/CPM) | Medium | ✅ | Shows in stats |
| Process Detection | Medium | ✅ | Auto-captures |
| Colorful CLI | Medium | ✅ | Always on |

## 🎯 Menu Options
```
[1] Start Recording    → Begin new session
[2] View Sessions      → List all recordings
[3] View Statistics    → Overall stats
[4] Settings           → Configure app
[5] Help              → Documentation
[0] Exit              → Close app
```

## 📊 What Gets Logged
```json
{
  "timestamp": "2025-11-13T10:30:01.123456",
  "window": "Visual Studio Code",
  "process": "Code.exe",
  "key": "h",
  "key_type": "standard"
}
```

## 🎓 Viva Quick Points

**Q: What is KeyStroke?**  
A: Educational keystroke logger for cybersecurity research

**Q: What does it record?**  
A: Keys, timestamps, active window, process name, editing behavior

**Q: How to stop recording?**  
A: Press ESC key

**Q: What formats does it save?**  
A: JSON (structured) and TXT (readable)

**Q: Is it encrypted?**  
A: Optional AES-128 Fernet encryption

**Q: Is it legal?**  
A: Educational use only with consent

**Q: Technologies used?**  
A: Python, pynput, colorama, cryptography, psutil, pywin32

**Q: How is typing speed calculated?**  
A: WPM = words/minutes, CPM = characters/minutes

## 🧪 Testing
```powershell
python test_features.py
# Result: 86/86 PASS (100%)
```

## 📁 File Structure
```
keystroke.py       → Main app (451 lines)
test_features.py   → Tests (86 tests)
requirements.txt   → Dependencies
README.md          → Documentation
USAGE_GUIDE.md     → Viva guide
VERIFICATION.md    → Test results
```

## ⚡ Quick Demo Script
1. `python keystroke.py` → Launch
2. Type `yes` → Accept terms
3. Press `1` → Start recording
4. Enter session name → e.g., "demo"
5. Type in apps → Notepad, Chrome, VS Code
6. Press `ESC` → Stop & see stats
7. Press `2` → View sessions
8. Open `logs/demo/` → Show files

## 🔑 Key Statistics Shown
- Total Keys Pressed
- Total Words
- Backspace Count
- Special Keys Count
- WPM (Words Per Minute)
- CPM (Characters Per Minute)
- Duration (minutes:seconds)

## 🛡️ Security Features
✅ Encryption toggle  
✅ Encryption key generation  
✅ Legal warning  
✅ Consent mechanism  
✅ No stealth features

## 📝 Log Locations
- All sessions: `./logs/`
- Each session: `./logs/<session_name>/`
- Log files: `log_1.json`, `log_1.txt`, etc.
- Config: `./config.json`

## 🎨 Terminal Colors
- 🟢 Green = Success
- 🔴 Red = Error
- 🟡 Yellow = Warning/Input
- 🔵 Cyan = Headers
- ⚪ White = Standard text

## ⚠️ Requirements
- Python 3.8+
- Windows OS (for pywin32)
- Administrator privileges (recommended)

## 🎯 Test Results
- **Total Tests:** 86
- **Passed:** 86 ✅
- **Failed:** 0
- **Pass Rate:** 100%

## 💡 Pro Tips for Viva
1. Emphasize educational purpose
2. Explain each feature clearly
3. Show live demo
4. Discuss defense mechanisms
5. Mention legal compliance
6. Know your code structure
7. Be confident!

## 🚨 Common Issues & Solutions

**Issue:** "ModuleNotFoundError"  
**Fix:** `pip install -r requirements.txt`

**Issue:** "Keys not recording"  
**Fix:** Run as Administrator

**Issue:** "Encryption fails"  
**Fix:** Regenerate key in Settings

## 🎊 Final Checklist
- [x] All dependencies installed
- [x] Application runs without errors
- [x] All 12 features working
- [x] 100% test pass rate
- [x] Documentation complete
- [x] Ready for demonstration

---

**Status:** ✅ 100% READY FOR PRESENTATION  
**Quality:** ⭐⭐⭐⭐⭐  
**Confidence Level:** VERY HIGH

**Good Luck! 🚀**
