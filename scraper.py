import keyboard
import os
import pyperclip
import pyautogui
import re
from colorama import init, Fore, Style
from config import KEY_PATTERN, FULL_KEY_PATTERN, REQUIRED_FRAGMENTS
from dotenv import load_dotenv
from logger import setup_logger
from twitchio.ext import commands
from windows import focus_steam_window

init()  # Initialize colorama

load_dotenv()
# Twitch Bot Config
# Load config from .env file
CHANNEL_NAME = os.getenv("CHANNEL_NAME")
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")

# Initialize logger before bot creation
logger = setup_logger()

class SteamKeyBot(commands.Bot):
    def __init__(self):
        super().__init__(token=OAUTH_TOKEN, prefix="!", initial_channels=[CHANNEL_NAME])
        self.key_parts = []
        self.reverse_order = False
        logger.info("Bot initialized - waiting for chat messages...")
        print(f"{Fore.GREEN}Bot initialized - waiting for chat messages...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Press 'R' to toggle reverse order{Style.RESET_ALL}")
        
        # Set up keyboard listener
        keyboard.on_press_key('r', self.toggle_reverse_order)

    def toggle_reverse_order(self, _):
        """Toggle reverse order when R is pressed"""
        self.reverse_order = not self.reverse_order
        print(f"{Fore.CYAN}Reverse order: {self.reverse_order}{Style.RESET_ALL}")

    async def event_message(self, message):
        if message.echo:
            return

        username = message.author.name
        is_streamer = username.lower() == CHANNEL_NAME.lower()
        
        if is_streamer:
            username = f"{Fore.YELLOW}{username}{Style.RESET_ALL}"
            
            # Check for full keys first (with or without spaces)
            full_keys = re.findall(FULL_KEY_PATTERN, ''.join(message.content.split()))
            if full_keys:
                for key in full_keys:
                    self.paste_complete_key(key)
                    print(f"{Fore.GREEN}Full key detected: {key}{Style.RESET_ALL}")
                return

            # Handle fragments with flexible ordering
            key_fragments = re.findall(KEY_PATTERN, message.content)
            if key_fragments:
                for fragment in key_fragments:
                    clean_fragment = ''.join(fragment.split())  # Remove spaces
                    if self.reverse_order:
                        self.key_parts.insert(0, clean_fragment)  # Add to start for reverse order
                    else:
                        self.key_parts.append(clean_fragment)  # Add to end for normal order
                    
                    print(f"{Fore.RED}Fragment detected: {clean_fragment}{Style.RESET_ALL}")
                    print(f"Current fragments: {'-'.join(self.key_parts)}")
                    
                    is_final = len(self.key_parts) >= REQUIRED_FRAGMENTS
                    if is_final:
                        assembled_key = '-'.join(self.key_parts[:REQUIRED_FRAGMENTS])
                        print(f"{Fore.GREEN}Full key assembled: {assembled_key}{Style.RESET_ALL}")
                        self.paste_complete_key(assembled_key)
                        self.key_parts = []
                        return

        print(f"{username}: {message.content}")


def paste_key_fragment(fragment, is_final=False):
    """Pastes a key fragment and adds hyphen if not final"""
    try:
        # Remove spaces from fragment before pasting
        clean_fragment = ''.join(fragment.split())
        pyperclip.copy(clean_fragment)
        if focus_steam_window():
            pyautogui.hotkey("ctrl", "v")
            if not is_final:
                pyautogui.write("-")
            elif is_final:
                pyautogui.press("enter")
                print(f"\n{Fore.GREEN}Full key submitted!{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error pasting fragment: {e}")


def paste_complete_key(self, key):
    """Pastes a complete key"""
    try:
        pyperclip.copy(key)
        if focus_steam_window():
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
            print(f"\n{Fore.GREEN}Full key submitted!{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error pasting complete key: {e}")


# Run the Twitch bot
bot = SteamKeyBot()
bot.run()
