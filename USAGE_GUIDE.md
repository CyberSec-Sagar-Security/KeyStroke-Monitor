# KeyStroke - Complete Usage Guide

## 🎯 For College Presentation & Viva

### Quick Start Commands

```powershell
# Navigate to project directory
cd "d:\CyberSecurity\Cyber_Security_Future_Projects\Keylogger"

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the application
python keystroke.py
```

## 📋 Viva Preparation Script

### 1. Introduction
*"Good morning/afternoon. Today I'll demonstrate **KeyStroke**, an educational keystroke logging tool I developed for cybersecurity research and learning purposes."*

### 2. Problem Statement
*"Keystroke loggers are commonly used by attackers to steal passwords and sensitive information. This project helps students understand:**
- How keystroke loggers work
- What data they capture
- How to detect and prevent them"*

### 3. Features Explanation

#### Basic Features (Say This):
| Feature | Explanation |
|---------|-------------|
| **Key Recording** | "Captures every key pressed with millisecond precision" |
| **Timestamp Logging** | "Records exact time of each keystroke for pattern analysis" |
| **Session Management** | "Organizes logs into separate sessions for better tracking" |
| **Log Storage** | "Saves data in both JSON (structured) and TXT (human-readable) formats" |

#### Medium-Level Features (Say This):
| Feature | Explanation |
|---------|-------------|
| **Active Window Tracking** | "Identifies which application was active (browser, notepad, etc.)" |
| **Process Monitoring** | "Captures the process name (chrome.exe, notepad.exe)" |
| **Log Rotation** | "Automatically splits logs when they reach 100KB to prevent huge files" |
| **Encryption** | "Optional AES encryption to protect sensitive logs" |
| **Typing Speed Analysis** | "Calculates WPM and CPM for usability research" |
| **Backspace Tracking** | "Monitors error corrections and editing behavior" |

### 4. Technical Implementation

#### Technologies Used:
```
✓ Python 3.8+ (Core language)
✓ pynput → Keyboard event monitoring
✓ colorama → Terminal UI colors
✓ cryptography → Fernet encryption
✓ psutil → Process information
✓ pywin32 → Windows API (active window detection)
```

#### Architecture Flow:
```
User Input → Keyboard Hook → Event Capture → Data Processing → 
Window Detection → Timestamp Addition → Log Storage → Encryption (optional)
```

### 5. Demo Script

#### Step 1: Launch Application
```powershell
python keystroke.py
```
*"As you can see, the tool displays a professional banner and legal warning, ensuring ethical use."*

#### Step 2: Accept Terms
```
Do you agree to use this tool responsibly? yes
```
*"I accept the terms, acknowledging this is for educational purposes only."*

#### Step 3: Start Session
```
Menu: [1] Start Recording Session
Enter session name: demo_presentation
```
*"I'll create a session called 'demo_presentation' to demonstrate the features."*

#### Step 4: Demonstrate Recording
*"Now I'll type in different applications to show window tracking:"*
- Open Notepad → Type: "This is a test"
- Open Chrome → Type: "google.com"
- Open VS Code → Type: "print('hello')"

#### Step 5: Stop Recording
*Press ESC*
*"The session stops and immediately shows statistics: total keys, words, WPM, CPM, and backspace count."*

#### Step 6: View Logs
```
Menu: [2] View Sessions
```
*"Here we can see all recorded sessions. Let me open the log file..."*

**Show the JSON structure:**
```json
{
  "session_name": "demo_presentation",
  "keys": [
    {
      "timestamp": "2025-11-13T10:30:01.123456",
      "window": "Notepad",
      "process": "notepad.exe",
      "key": "T",
      "key_type": "standard"
    }
  ]
}
```

#### Step 7: Show Settings
```
Menu: [4] Settings
[1] Toggle Encryption
```
*"I can enable encryption to protect sensitive logs. The system uses Fernet (AES-128) encryption."*

### 6. Security & Defense Discussion

*"While this tool demonstrates offensive capabilities, it's crucial to discuss defense:**

**Detection Methods:**
- Monitor unusual keyboard API hooks
- Check for suspicious processes
- Use anti-keylogger software
- Behavioral analysis (unusual network traffic)

**Prevention:**
- Virtual keyboards for passwords
- Two-factor authentication
- Regular system scans
- Principle of least privilege"*

### 7. Expected Viva Questions & Answers

#### Q1: "Is this legal?"
**A:** *"This tool is strictly educational. Real-world keystroke logging without consent is illegal under privacy laws like GDPR, CFAA, and IT Act 2000. I've included legal warnings and consent mechanisms."*

#### Q2: "How does keyboard hooking work?"
**A:** *"The pynput library registers a low-level keyboard hook with the OS. Whenever a key is pressed, the OS calls our callback function with the key event. We process and store this event."*

#### Q3: "Can this be detected?"
**A:** *"Yes, several ways:*
- *Process monitoring (Task Manager shows python.exe)*
- *Anti-virus software detects keyboard hooks*
- *Network monitoring (if logs are transmitted)*
- *Behavioral analysis (CPU/memory usage)"*

#### Q4: "What's the difference between this and commercial keyloggers?"
**A:** *"Commercial keyloggers often:*
- *Hide themselves (rootkit techniques)*
- *Capture screenshots*
- *Record clipboard*
- *Transmit data remotely*
*Mine is transparent and educational with no stealth features."*

#### Q5: "How accurate is the typing speed calculation?"
**A:** *"Very accurate. I calculate WPM by dividing word count by minutes elapsed. Industry standard is 5 characters = 1 word. CPM is direct character count divided by minutes."*

#### Q6: "Why use log rotation?"
**A:** *"Large files consume memory and slow down I/O operations. Rotating logs at 100KB ensures:*
- *Better performance*
- *Easier management*
- *Reduced corruption risk"*

#### Q7: "What encryption algorithm do you use?"
**A:** *"Fernet from the cryptography library, which uses AES-128 in CBC mode with HMAC for authentication. It's suitable for educational purposes and demonstrates secure storage principles."*

#### Q8: "Can you extend this to capture passwords?"
**A:** *"Technically yes, but ethically no. Passwords can be reconstructed from keystroke sequences, which is why this tool has consent mechanisms and is for authorized use only."*

### 8. Code Highlights to Explain

#### Key Press Handler:
```python
def on_press(self, key):
    timestamp = datetime.datetime.now()
    window_title, process_name = self.get_active_window()
    
    key_data = {
        'timestamp': timestamp.isoformat(),
        'window': window_title,
        'process': process_name,
        'key': key.char if hasattr(key, 'char') else f"<{key}>"
    }
    
    self.keys_pressed.append(key_data)
```
*"This callback captures the key, timestamp, and active window for each keystroke."*

#### Window Detection:
```python
def get_active_window(self):
    window = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(window)
    _, pid = win32process.GetWindowThreadProcessId(window)
    process = psutil.Process(pid)
    return window_title, process.name()
```
*"Uses Windows API to get the foreground window and psutil to identify the process."*

### 9. Project Outcomes

*"Through this project, I achieved:**
- ✅ Understanding of keyboard event handling
- ✅ Windows API integration
- ✅ Data encryption techniques
- ✅ Professional CLI development
- ✅ Ethical hacking awareness
- ✅ Defensive security mindset"*

### 10. Future Enhancements

*"Possible improvements:**
- Multi-language support (Linux/Mac)
- Machine learning for typing pattern analysis
- Real-time dashboard with graphs
- Network transmission simulation (for detection practice)
- Integration with SIEM tools for security training"*

### 11. Closing Statement

*"In conclusion, KeyStroke is a comprehensive educational tool that demonstrates both offensive and defensive cybersecurity concepts. It emphasizes responsible use and legal compliance while providing hands-on learning experience."*

---

## 🎓 Presentation Checklist

Before your viva, ensure:
- [ ] All dependencies are installed
- [ ] Application runs without errors
- [ ] Sample session data is prepared
- [ ] You can explain each feature
- [ ] You understand the code structure
- [ ] You know the legal implications
- [ ] You can discuss defense mechanisms
- [ ] You have backup slides/documentation

## 📊 Key Statistics to Remember

- **Lines of Code**: ~500+ (well-structured)
- **Features**: 12+ (Basic to Medium level)
- **Dependencies**: 5 main libraries
- **File Formats**: 2 (JSON, TXT)
- **Encryption**: AES-128 (Fernet)
- **Platforms**: Windows (extendable)

## 🎯 Final Tips

1. **Be Confident**: You built this, you understand it
2. **Be Honest**: If you don't know something, say so
3. **Be Ethical**: Always emphasize legal and responsible use
4. **Be Prepared**: Have logs ready to show
5. **Be Professional**: Dress well, speak clearly

---

**Good Luck with Your Presentation! 🚀**
