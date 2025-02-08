# windows.py
import pyautogui
import time
from config import PASTE_DELAY

def focus_steam_window(title="Steam"):
    """Focus the Steam activation window"""
    try:
        windows = pyautogui.getWindowsWithTitle(title)
        print(f"Found {len(windows)} windows containing '{title}':")
        for window in windows:
            print(f"Window title: {window.title}")
            # Look for any Steam window first
            if "steam" in window.title.lower():
                window.activate()
                time.sleep(PASTE_DELAY)  # Small delay to ensure window is focused
                return True
        return False
    except Exception as e:
        print(f"Error focusing Steam window: {e}")
        return False