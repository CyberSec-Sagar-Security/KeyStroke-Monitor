"""
KeyStroke - Educational Keystroke Logger
A terminal-based keystroke recording tool for research and educational purposes only.
"""

import os
import sys
import json
import time
import datetime
from pathlib import Path
from pynput import keyboard
from colorama import init, Fore, Style, Back
from threading import Thread, Event
import hashlib
from cryptography.fernet import Fernet
import psutil
import win32gui
import win32process

# Initialize colorama for Windows
init(autoreset=True)

class KeyStroke:
    def __init__(self):
        self.session_name = ""
        self.log_dir = Path("logs")
        self.config_file = Path("config.json")
        self.keys_pressed = []
        self.session_start = None
        self.session_end = None
        self.is_running = False
        self.listener = None
        self.encryption_enabled = False
        self.encryption_key = None
        self.max_log_size = 1024 * 100  # 100KB per file
        self.current_log_count = 1
        
        # Statistics
        self.total_keys = 0
        self.total_words = 0
        self.backspace_count = 0
        self.special_keys_count = 0
        
        # Create directories
        self.log_dir.mkdir(exist_ok=True)
        
        # Load or create config
        self.load_config()
    
    def print_banner(self):
        """Display beautiful ASCII banner"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  {Fore.YELLOW}██╗  ██╗███████╗██╗   ██╗███████╗████████╗██████╗  ██████╗  {Fore.CYAN}║
║  {Fore.YELLOW}██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗{Fore.CYAN} ║
║  {Fore.YELLOW}█████╔╝ █████╗   ╚████╔╝ ███████╗   ██║   ██████╔╝██║   ██║{Fore.CYAN} ║
║  {Fore.YELLOW}██╔═██╗ ██╔══╝    ╚██╔╝  ╚════██║   ██║   ██╔══██╗██║   ██║{Fore.CYAN} ║
║  {Fore.YELLOW}██║  ██╗███████╗   ██║   ███████║   ██║   ██║  ██║╚██████╔╝{Fore.CYAN} ║
║  {Fore.YELLOW}╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ {Fore.CYAN} ║
║                                                               ║
║           {Fore.GREEN}Educational Keystroke Recording Tool v2.0{Fore.CYAN}          ║
║               {Fore.WHITE}For Research & Learning Purposes Only{Fore.CYAN}            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
    
    def print_menu(self):
        """Display main menu - Interactive terminal menu system"""
        print(f"\n{Fore.CYAN}┌─────────────────── MAIN MENU ───────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│                                                 │{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│  {Fore.GREEN}[1]{Fore.WHITE} Start Recording Session                  │{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│  {Fore.GREEN}[2]{Fore.WHITE} View Sessions                             │{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│  {Fore.GREEN}[3]{Fore.WHITE} View Statistics                           │{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│  {Fore.GREEN}[4]{Fore.WHITE} Settings                                  │{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│  {Fore.GREEN}[5]{Fore.WHITE} Help & Documentation                      │{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│  {Fore.RED}[0]{Fore.WHITE} Exit                                      │{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│                                                 │{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────┘{Style.RESET_ALL}\n")
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.encryption_enabled = config.get('encryption_enabled', False)
                self.max_log_size = config.get('max_log_size', 1024 * 100)
                if self.encryption_enabled and config.get('encryption_key'):
                    self.encryption_key = config['encryption_key'].encode()
        else:
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        config = {
            'encryption_enabled': self.encryption_enabled,
            'max_log_size': self.max_log_size,
            'encryption_key': self.encryption_key.decode() if self.encryption_key else None
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def get_active_window(self):
        """Get the currently active window title and process name"""
        try:
            window = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(window)
            _, pid = win32process.GetWindowThreadProcessId(window)
            process = psutil.Process(pid)
            process_name = process.name()
            return window_title, process_name
        except:
            return "Unknown", "Unknown"
    
    def on_press(self, key):
        """Callback for key press events"""
        if not self.is_running:
            return False
        
        # Check for ESC key to stop recording
        try:
            if key == keyboard.Key.esc:
                self.is_running = False
                return False
        except:
            pass
        
        timestamp = datetime.datetime.now()
        window_title, process_name = self.get_active_window()
        
        key_data = {
            'timestamp': timestamp.isoformat(),
            'window': window_title,
            'process': process_name,
            'key': None,
            'key_type': 'standard'
        }
        
        try:
            # Standard character key
            if hasattr(key, 'char') and key.char:
                key_data['key'] = key.char
                self.total_keys += 1
            else:
                # Special key
                key_name = str(key).replace('Key.', '')
                key_data['key'] = f"<{key_name}>"
                key_data['key_type'] = 'special'
                self.special_keys_count += 1
                
                if 'backspace' in key_name.lower():
                    self.backspace_count += 1
                elif 'space' in key_name.lower():
                    self.total_words += 1
                    self.total_keys += 1
        except AttributeError:
            key_data['key'] = str(key)
            key_data['key_type'] = 'special'
            self.special_keys_count += 1
        
        self.keys_pressed.append(key_data)
        
        # Auto-save if log is getting too large
        if len(self.keys_pressed) % 100 == 0:
            self.save_session_log()
    
    def start_recording(self):
        """Start a new recording session"""
        print(f"\n{Fore.CYAN}╔══════════════ NEW SESSION ══════════════╗{Style.RESET_ALL}")
        
        try:
            session_name = input(f"{Fore.WHITE}Enter session name (or press Enter for auto): {Fore.YELLOW}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Fore.RED}✗ Session creation cancelled.{Style.RESET_ALL}")
            return
        
        if not session_name:
            session_name = f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.session_name = session_name
        self.session_start = datetime.datetime.now()
        self.keys_pressed = []
        self.total_keys = 0
        self.total_words = 0
        self.backspace_count = 0
        self.special_keys_count = 0
        self.current_log_count = 1
        self.is_running = True
        
        print(f"\n{Fore.GREEN}✓ Session '{session_name}' started!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Started at: {Fore.YELLOW}{self.session_start.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Encryption: {Fore.YELLOW}{'Enabled' if self.encryption_enabled else 'Disabled'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}📝 Recording keystrokes...{Style.RESET_ALL}")
        print(f"{Fore.RED}⚠ Press ESC key to stop recording{Style.RESET_ALL}\n")
        
        # Start listener in a separate thread
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        
        # Wait for listener to stop (ESC key pressed)
        self.listener.join()
        
        # Stop recording
        self.stop_recording()
    
    def stop_recording(self):
        """Stop the current recording session"""
        if not self.is_running and not self.session_start:
            print(f"{Fore.RED}✗ No active session to stop.{Style.RESET_ALL}")
            return
        
        self.is_running = False
        self.session_end = datetime.datetime.now()
        
        if self.listener and self.listener.is_alive():
            self.listener.stop()
        
        # Save final log
        if self.keys_pressed:
            self.save_session_log()
        
        # Calculate statistics
        duration = (self.session_end - self.session_start).total_seconds()
        minutes = duration / 60
        
        print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Session stopped successfully!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Session Name:    {Fore.YELLOW}{self.session_name}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Duration:        {Fore.YELLOW}{int(duration // 60)}m {int(duration % 60)}s{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Total Keys:      {Fore.YELLOW}{self.total_keys}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Total Words:     {Fore.YELLOW}{self.total_words}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Backspaces:      {Fore.YELLOW}{self.backspace_count}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Special Keys:    {Fore.YELLOW}{self.special_keys_count}{Style.RESET_ALL}")
        if minutes > 0:
            print(f"{Fore.WHITE}WPM:             {Fore.YELLOW}{int(self.total_words / minutes)}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}CPM:             {Fore.YELLOW}{int(self.total_keys / minutes)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")
        
        # Reset session
        self.session_start = None
        self.session_name = ""
    
    def save_session_log(self):
        """Save session data to file"""
        if not self.keys_pressed:
            return
        
        # Check if we need log rotation
        session_dir = self.log_dir / self.session_name
        session_dir.mkdir(exist_ok=True)
        
        log_file = session_dir / f"log_{self.current_log_count}.json"
        
        # Check file size for rotation
        if log_file.exists() and log_file.stat().st_size > self.max_log_size:
            self.current_log_count += 1
            log_file = session_dir / f"log_{self.current_log_count}.json"
        
        # Prepare data
        data = {
            'session_name': self.session_name,
            'session_start': self.session_start.isoformat() if self.session_start else None,
            'log_number': self.current_log_count,
            'keys': self.keys_pressed
        }
        
        # Save to JSON
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Also save as readable TXT
        txt_file = session_dir / f"log_{self.current_log_count}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"KeyStroke Session Log\n")
            f.write(f"Session: {self.session_name}\n")
            f.write(f"Started: {self.session_start}\n")
            f.write("=" * 80 + "\n\n")
            
            for entry in self.keys_pressed:
                f.write(f"[{entry['timestamp']}] ")
                f.write(f"[{entry['process']}] ")
                f.write(f"[{entry['window'][:30]}...] " if len(entry['window']) > 30 else f"[{entry['window']}] ")
                f.write(f"{entry['key']}\n")
        
        # Encrypt if enabled
        if self.encryption_enabled and self.encryption_key:
            self.encrypt_file(log_file)
            self.encrypt_file(txt_file)
        
        print(f"{Fore.GREEN}💾 Log saved: {log_file.name}{Style.RESET_ALL}")
    
    def encrypt_file(self, filepath):
        """Encrypt a file"""
        try:
            fernet = Fernet(self.encryption_key)
            with open(filepath, 'rb') as f:
                data = f.read()
            encrypted = fernet.encrypt(data)
            enc_file = filepath.parent / f"{filepath.name}.enc"
            with open(enc_file, 'wb') as f:
                f.write(encrypted)
            # Remove original
            filepath.unlink()
        except Exception as e:
            print(f"{Fore.RED}✗ Encryption error: {e}{Style.RESET_ALL}")
    
    def view_sessions(self):
        """Display all recorded sessions"""
        sessions = [d for d in self.log_dir.iterdir() if d.is_dir()]
        
        if not sessions:
            print(f"\n{Fore.YELLOW}⚠ No sessions found.{Style.RESET_ALL}\n")
            return
        
        print(f"\n{Fore.CYAN}╔══════════════ RECORDED SESSIONS ══════════════╗{Style.RESET_ALL}\n")
        
        for idx, session in enumerate(sessions, 1):
            logs = list(session.glob("*.json")) + list(session.glob("*.json.enc"))
            print(f"{Fore.WHITE}{idx}. {Fore.YELLOW}{session.name}{Style.RESET_ALL}")
            print(f"   {Fore.WHITE}Files: {len(logs)}{Style.RESET_ALL}")
            print(f"   {Fore.WHITE}Path: {session}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    def view_statistics(self):
        """View overall statistics"""
        sessions = [d for d in self.log_dir.iterdir() if d.is_dir()]
        total_sessions = len(sessions)
        total_files = sum(len(list(s.glob("*"))) for s in sessions)
        
        print(f"\n{Fore.CYAN}╔══════════════ STATISTICS ══════════════╗{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│                                        │{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│  Total Sessions:  {Fore.YELLOW}{total_sessions:<19}  {Fore.WHITE}│{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│  Total Log Files: {Fore.YELLOW}{total_files:<19}  {Fore.WHITE}│{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│  Encryption:      {Fore.YELLOW}{'Enabled' if self.encryption_enabled else 'Disabled':<19}  {Fore.WHITE}│{Style.RESET_ALL}")
        print(f"{Fore.WHITE}│                                        │{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    def settings_menu(self):
        """Settings configuration"""
        while True:
            print(f"\n{Fore.CYAN}╔══════════════ SETTINGS ══════════════╗{Style.RESET_ALL}")
            print(f"{Fore.WHITE}│                                      │{Style.RESET_ALL}")
            print(f"{Fore.WHITE}│  {Fore.GREEN}[1]{Fore.WHITE} Toggle Encryption ({Fore.YELLOW}{'ON' if self.encryption_enabled else 'OFF'}{Fore.WHITE})     │{Style.RESET_ALL}")
            print(f"{Fore.WHITE}│  {Fore.GREEN}[2]{Fore.WHITE} Set Log Rotation Size            │{Style.RESET_ALL}")
            print(f"{Fore.WHITE}│  {Fore.GREEN}[3]{Fore.WHITE} Generate New Encryption Key      │{Style.RESET_ALL}")
            print(f"{Fore.WHITE}│  {Fore.RED}[0]{Fore.WHITE} Back to Main Menu                │{Style.RESET_ALL}")
            print(f"{Fore.WHITE}│                                      │{Style.RESET_ALL}")
            print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}\n")
            
            try:
                choice = input(f"{Fore.WHITE}Choose option: {Fore.YELLOW}").strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Fore.YELLOW}Returning to main menu...{Style.RESET_ALL}")
                break
            
            if choice == '1':
                self.encryption_enabled = not self.encryption_enabled
                if self.encryption_enabled and not self.encryption_key:
                    self.encryption_key = Fernet.generate_key()
                self.save_config()
                print(f"{Fore.GREEN}✓ Encryption {'enabled' if self.encryption_enabled else 'disabled'}{Style.RESET_ALL}")
            elif choice == '2':
                try:
                    size = input(f"{Fore.WHITE}Enter max log size in KB (current: {self.max_log_size // 1024}): {Fore.YELLOW}")
                    self.max_log_size = int(size) * 1024
                    self.save_config()
                    print(f"{Fore.GREEN}✓ Log size updated{Style.RESET_ALL}")
                except (ValueError, EOFError, KeyboardInterrupt):
                    print(f"{Fore.RED}✗ Invalid size{Style.RESET_ALL}")
            elif choice == '3':
                self.encryption_key = Fernet.generate_key()
                self.encryption_enabled = True
                self.save_config()
                print(f"{Fore.GREEN}✓ New encryption key generated{Style.RESET_ALL}")
            elif choice == '0':
                break
            else:
                print(f"{Fore.RED}✗ Invalid option{Style.RESET_ALL}")
    
    def show_help(self):
        """Display help documentation"""
        help_text = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                    KEYSTROKE DOCUMENTATION                    ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}📚 What is KeyStroke?{Style.RESET_ALL}
{Fore.WHITE}KeyStroke is an educational tool that records keyboard input for
research, monitoring, usability testing, and cybersecurity education.{Style.RESET_ALL}

{Fore.YELLOW}🎯 Features:{Style.RESET_ALL}
{Fore.GREEN}✓{Fore.WHITE} Key Recording with timestamps
{Fore.GREEN}✓{Fore.WHITE} Active window tracking
{Fore.GREEN}✓{Fore.WHITE} Session-based logging
{Fore.GREEN}✓{Fore.WHITE} Log rotation (auto-split large files)
{Fore.GREEN}✓{Fore.WHITE} Encryption support
{Fore.GREEN}✓{Fore.WHITE} Typing speed calculation (WPM/CPM)
{Fore.GREEN}✓{Fore.WHITE} Backspace & editing behavior tracking
{Fore.GREEN}✓{Fore.WHITE} Multiple export formats (JSON, TXT)

{Fore.YELLOW}🔧 How to Use:{Style.RESET_ALL}
{Fore.WHITE}1. Start a recording session from main menu
2. Type normally in any application
3. Press ESC to stop recording
4. View logs in the 'logs' folder
5. Analyze typing patterns and behavior{Style.RESET_ALL}

{Fore.YELLOW}⚠ Legal Notice:{Style.RESET_ALL}
{Fore.RED}This tool is for EDUCATIONAL purposes only. Unauthorized use
of keystroke logging software may be illegal. Always obtain proper
consent before monitoring keyboard activity.{Style.RESET_ALL}

{Fore.YELLOW}📁 Log File Locations:{Style.RESET_ALL}
{Fore.WHITE}All logs are saved in: ./logs/<session_name>/
Formats: JSON (structured), TXT (readable){Style.RESET_ALL}

"""
        print(help_text)
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def run(self):
        """Main application loop"""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        
        print(f"{Fore.RED}⚠  LEGAL WARNING ⚠{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}This tool is for EDUCATIONAL and RESEARCH purposes only.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Unauthorized keystroke logging may be illegal in your jurisdiction.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Always obtain proper consent before use.{Style.RESET_ALL}\n")
        
        try:
            consent = input(f"{Fore.WHITE}Do you agree to use this tool responsibly? (yes/no): {Fore.YELLOW}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Fore.RED}Exiting...{Style.RESET_ALL}")
            sys.exit(0)
        
        if consent != 'yes':
            print(f"\n{Fore.RED}Exiting...{Style.RESET_ALL}")
            sys.exit(0)
        
        while True:
            try:
                self.print_menu()
                choice = input(f"{Fore.WHITE}Enter your choice: {Fore.YELLOW}").strip()
                
                if choice == '1':
                    self.start_recording()
                elif choice == '2':
                    self.view_sessions()
                elif choice == '3':
                    self.view_statistics()
                elif choice == '4':
                    self.settings_menu()
                elif choice == '5':
                    self.show_help()
                elif choice == '0':
                    print(f"\n{Fore.CYAN}Thank you for using KeyStroke!{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Stay ethical, stay legal. 🔒{Style.RESET_ALL}\n")
                    sys.exit(0)
                else:
                    print(f"{Fore.RED}✗ Invalid choice. Please try again.{Style.RESET_ALL}")
            except (EOFError, KeyboardInterrupt):
                print(f"\n\n{Fore.CYAN}Exiting KeyStroke...{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Thank you for using KeyStroke! Stay ethical, stay legal. 🔒{Style.RESET_ALL}\n")
                sys.exit(0)
            except Exception as e:
                print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Returning to main menu...{Style.RESET_ALL}\n")


if __name__ == "__main__":
    try:
        app = KeyStroke()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}Program interrupted by user.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
