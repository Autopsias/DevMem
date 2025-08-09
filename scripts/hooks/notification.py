#!/usr/bin/env python3
import json
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime

class ClaudeNotificationHandler:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.log_file = self.project_root / ".claude" / "notifications.log"
        self.config = self._load_config()
        
    def _load_config(self):
        return {
            "audio_alerts": os.getenv("CLAUDE_AUDIO_ALERTS", "true") == "true",
            "desktop_notifications": os.getenv("CLAUDE_DESKTOP_NOTIFICATIONS", "true") == "true",
            "notification_level": os.getenv("CLAUDE_NOTIFICATION_LEVEL", "info")
        }
    
    def send_desktop_notification(self, title, message):
        if not self.config["desktop_notifications"]:
            return
            
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], check=True, timeout=3)
        except Exception:
            pass
    
    def play_notification_sound(self, sound_type="default"):
        if not self.config["audio_alerts"]:
            return
            
        sound_map = {
            "input": "/System/Library/Sounds/Glass.aiff",
            "warning": "/System/Library/Sounds/Sosumi.aiff",
            "error": "/System/Library/Sounds/Basso.aiff",
            "default": "/System/Library/Sounds/Ping.aiff"
        }
        
        sound_file = sound_map.get(sound_type, sound_map["default"])
        try:
            subprocess.Popen(["afplay", sound_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
    
    def handle_notification(self, data):
        message = data.get("message", "")
        if "needs input" in message.lower():
            self.send_desktop_notification("Claude Code", "Input needed")
            self.play_notification_sound("input")

def main():
    if not sys.stdin.isatty():
        data = json.load(sys.stdin)
    else:
        data = {"message": " ".join(sys.argv[1:])}
    
    handler = ClaudeNotificationHandler()
    handler.handle_notification(data)

if __name__ == "__main__":
    main()