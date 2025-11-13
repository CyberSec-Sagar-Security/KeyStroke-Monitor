# 🔬 KeyStroke Monitor

### Educational Typing Behavior Analysis & Input Event Recorder

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Research](https://img.shields.io/badge/purpose-educational-brightgreen)
![Status](https://img.shields.io/badge/status-active-success)

---

## 📋 Overview

**KeyStroke Monitor** is a consent-based, educational terminal application designed for **cybersecurity research**, **typing dynamics analysis**, and **behavioral studies**. This tool helps students, researchers, and security professionals understand:

- How input event monitoring works at the system level
- Typing behavior patterns and speed analysis
- Defensive security techniques against unauthorized monitoring
- Ethical data collection for usability research

### 🎓 Educational Purpose

This project is specifically created for:
- **Academic research** on typing patterns and user behavior
- **Cybersecurity education** to understand monitoring techniques
- **Defensive security training** to learn detection methods
- **Usability testing** in controlled environments
- **Typing performance analysis** for accessibility studies

---

## 🛡️ Safety & Ethics Disclaimer

### ⚠️ CRITICAL - READ BEFORE USE

**This tool is STRICTLY for educational and research purposes with explicit consent.**

#### ✅ Authorized Use Cases:
- Personal typing behavior analysis on your own computer
- Academic research with participant consent
- Cybersecurity labs in controlled environments
- Educational demonstrations with proper authorization
- Typing speed improvement studies
- Accessibility and usability research

#### ❌ PROHIBITED Use Cases:
- Monitoring others without explicit written consent
- Use on systems you don't own or have permission to use
- Any malicious or unauthorized data collection
- Violation of privacy laws or institutional policies
- Deployment without clear user notification

#### 🔒 Legal Compliance:
- User must **explicitly agree** to monitoring before tool starts
- Data is stored **locally only** - no remote transmission
- Tool requires **manual user initiation** - does not run in background
- Complies with **GDPR**, **CFAA**, and **data protection regulations**
- Designed for **transparent, consent-based** operation

#### ⚖️ Responsibility Statement:
The author is **NOT responsible** for any misuse of this software. Users are solely responsible for ensuring their use complies with all applicable laws, regulations, and ethical guidelines. This tool is provided "AS IS" for educational purposes only.

## 🎯 Features

### Core Features (Basic Level)
- ✅ **Key Recording**: Captures all keyboard inputs with timestamps
- ✅ **Session Management**: Organize recordings into named sessions
- ✅ **Timestamp Logging**: Precise time tracking for each keystroke
- ✅ **Log Storage**: Multiple export formats (JSON, TXT)

### Medium-Level Features
- ✅ **Active Window Tracking**: Records which application was active
- ✅ **Log Rotation**: Auto-splits large log files
- ✅ **Encryption Support**: Optional AES encryption for privacy
- ✅ **Typing Speed Analysis**: Calculates WPM and CPM
- ✅ **Backspace Tracking**: Monitors editing behavior
- ✅ **Clean Terminal UI**: Colorful, professional CLI interface
- ✅ **Statistics Dashboard**: Real-time session analytics

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Windows OS (for `pywin32` support)
- Administrator privileges (for keyboard monitoring)

### Setup Steps

1. **Clone or download the project**
```powershell
cd "d:\CyberSecurity\Cyber_Security_Future_Projects\Keylogger"
```

2. **Install dependencies**
```powershell
pip install -r requirements.txt
```

3. **Run the application**
```powershell
python keystroke.py
```

## 📖 How to Use

### Starting a Recording Session

1. Run the program: `python keystroke.py`
2. Accept the legal agreement
3. Select option `[1] Start Recording Session`
4. Enter a session name (or press Enter for auto-generated name)
5. Type normally in any application
6. **Press ESC to stop recording**

### Viewing Recorded Sessions

1. Select option `[2] View Sessions`
2. All sessions are listed with file counts
3. Navigate to `logs/<session_name>/` to view files

### Understanding Log Files

Each session creates two types of files:

**JSON Format** (`log_1.json`)
```json
{
  "session_name": "test_session",
  "session_start": "2025-11-13T10:30:00",
  "log_number": 1,
  "keys": [
    {
      "timestamp": "2025-11-13T10:30:01.123456",
      "window": "Visual Studio Code",
      "process": "Code.exe",
      "key": "h",
      "key_type": "standard"
    }
  ]
}
```

**TXT Format** (`log_1.txt`)
```
KeyStroke Session Log
Session: test_session
Started: 2025-11-13 10:30:00
================================================================================

[2025-11-13T10:30:01.123456] [Code.exe] [Visual Studio Code] h
[2025-11-13T10:30:01.234567] [Code.exe] [Visual Studio Code] e
[2025-11-13T10:30:01.345678] [Code.exe] [Visual Studio Code] l
```

## 🔧 Configuration & Settings

### Enable Encryption
1. Go to `[4] Settings`
2. Select `[1] Toggle Encryption`
3. Encryption key is auto-generated
4. All future logs will be encrypted with `.enc` extension

### Log Rotation
- Default: 100KB per file
- Change in Settings → `[2] Set Log Rotation Size`
- Prevents massive single files

## 📊 Statistics & Analysis

The tool calculates:
- **Total Keys Pressed**
- **Word Count** (space-separated)
- **Backspace Count** (error corrections)
- **Special Keys** (Ctrl, Shift, etc.)
- **WPM** (Words Per Minute)
- **CPM** (Characters Per Minute)
- **Session Duration**

## 🎓 Educational Use Cases

### For Students
1. **Cybersecurity Awareness**: Understand how attackers capture data
2. **Defensive Techniques**: Learn to detect such tools
3. **Typing Analysis**: Improve typing speed and accuracy
4. **Behavioral Research**: Study typing patterns

### For Researchers
1. **Usability Testing**: Analyze user interaction patterns
2. **Accessibility Studies**: Understand typing difficulties
3. **Security Training**: Demonstrate attack vectors
4. **Forensics**: Understand evidence collection

## 🛡️ How It Works (Technical Overview)

### Workflow
```
1. Initialize Settings
   ↓
2. Start Keyboard Listener (pynput)
   ↓
3. Capture Key Events
   ├─ Key pressed
   ├─ Timestamp
   ├─ Active window (win32gui)
   └─ Process name (psutil)
   ↓
4. Process Data
   ├─ Calculate typing metrics
   ├─ Detect backspaces
   └─ Reconstruct words
   ↓
5. Store Logs
   ├─ JSON (structured)
   ├─ TXT (readable)
   └─ Encrypt (optional)
   ↓
6. Session Complete
   └─ Generate statistics
```

### Key Technologies
- **pynput**: Cross-platform keyboard monitoring
- **colorama**: Terminal colors (Windows-compatible)
- **cryptography**: Fernet symmetric encryption
- **psutil**: Process information
- **pywin32**: Windows API access for window tracking

## 📁 Project Structure

```
Keylogger/
├── keystroke.py          # Main application
├── requirements.txt      # Dependencies
├── README.md            # This file
├── config.json          # Auto-generated settings
└── logs/                # Session logs
    └── <session_name>/
        ├── log_1.json
        ├── log_1.txt
        ├── log_2.json
        └── log_2.txt
```

## 🎨 Terminal Interface

The application features a clean, colorful terminal UI:
- 🟢 **Green**: Success messages
- 🔵 **Cyan**: Headers and borders
- 🟡 **Yellow**: Warnings and input prompts
- 🔴 **Red**: Errors and critical warnings
- ⚪ **White**: Standard text

## ❓ FAQ

**Q: Do I need admin rights?**  
A: Yes, keyboard monitoring typically requires elevated privileges.

**Q: Does it work on Linux/Mac?**  
A: Partially. Remove `pywin32` dependency and modify window tracking code.

**Q: Can I analyze old sessions?**  
A: Yes, all logs are saved in `logs/` directory.

**Q: Is the encryption secure?**  
A: Uses Fernet (AES-128), suitable for educational purposes.

**Q: How to stop recording?**  
A: Press ESC key or use Ctrl+C in terminal.

## 🐛 Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'win32gui'`  
**Solution**: `pip install pywin32`

**Issue**: Program doesn't record keys  
**Solution**: Run as Administrator

**Issue**: Encryption fails  
**Solution**: Regenerate encryption key in Settings

## 🎯 Presentation Tips (For Viva)

### Key Points to Mention:
1. **Educational Purpose**: Emphasize learning objectives
2. **Legal Compliance**: Always mention consent requirements
3. **Technical Skills**: Explain keyboard hooking, process monitoring
4. **Security Awareness**: Defensive applications
5. **Clean Code**: Well-structured, documented Python code

### Demo Flow:
1. Show the banner and legal warning
2. Start a session with a meaningful name
3. Type in different applications (Notepad, Browser)
4. Stop and show statistics
5. Open log files to show data structure
6. Demonstrate encryption feature
7. Explain defensive countermeasures

## 📚 Further Learning

- Study anti-keylogger techniques
- Learn about rootkit detection
- Understand Windows API hooks
- Explore machine learning for typing pattern recognition
- Research behavioral biometrics

## 🤝 Contributing

This is an educational project. Feel free to:
- Add more features (clipboard tracking, screenshots)
- Improve UI/UX
- Add Linux/Mac support
- Enhance analytics

## 📝 License

**Educational Use Only**  
Not licensed for commercial or unauthorized monitoring use.

## 📧 Contact

For educational queries or project collaboration, create an issue in the repository.

---

**Remember**: *With great power comes great responsibility.* Use this tool ethically and legally.

**Made for Cybersecurity Education** 🔒🎓
