# Twitch Stream Steam Key Scraper

Automatically monitors Twitch chat for Steam key fragments and instantly redeems them in real-time, handling various key formats and fragment orders.




https://github.com/user-attachments/assets/1a06d53f-c9c3-4f16-933e-8142486a70b7



  
## Features
- Real-time key detection and redemption
- Handles multiple key formats:
  - Full keys (with or without spaces)
  - Individual fragments
  - Spaced fragments
  - Reverse order fragments
- Colored terminal output:
  - Channel owner's messages in yellow
  - Key fragments in red
  - Success messages in green
- Keyboard controls for quick adjustments
- Automatic Steam window management

## Prerequisites
- Python 3.6+
- Steam client installed
- Twitch account with chat access
- OAuth token from https://twitchtokengenerator.com

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```properties
CHANNEL_NAME=channel_to_monitor    # e.g., FiraxisGames
OAUTH_TOKEN=oauth:xxxxx            # From twitchtokengenerator.com
```

## Required Window Setup

1. Steam Window:
   - Open Steam
   - Click "Games" menu → "Activate a Product on Steam..."
   - Click through to the "Product Code" entry screen
   - **Critical:** Ensure cursor is in the code entry box

2. Twitch Window:
   - Open browser to twitch.tv/CHANNEL_NAME
   - Keep stream page open (focus not required)

## Key Processing Capabilities

The bot handles all common key distribution methods:

1. Full Key Detection:
```
FiraxisGames: XXAXX-XXBXX-XXCXX
[Bot instantly pastes complete key and presses Enter]
```

2. Standard Fragment Order:
```
FiraxisGames: XXAXX
[Bot pastes: XXAXX-]

FiraxisGames: XXBXX
[Bot pastes: XXBXX-]

FiraxisGames: XXCXX
[Bot pastes: XXCXX + Enter]
```

3. Spaced Fragments:
```
FiraxisGames: X X A X X
[Bot cleans and pastes: XXAXX-]

FiraxisGames: X X B X X
[Bot cleans and pastes: XXBXX-]

FiraxisGames: X X C X X
[Bot cleans and pastes: XXCXX + Enter]
```

4. Reverse Fragment Order:
```
[Press 'R' to enable reverse order]

FiraxisGames: XXCXX
[Bot adds to start: XXCXX]

FiraxisGames: XXBXX
[Bot adds to start: XXBXX-XXCXX]

FiraxisGames: XXAXX
[Bot completes: XXAXX-XXBXX-XXCXX + Enter]
```

## Controls

- **'R' Key**: Toggle reverse fragment order
  - Press when streamer announces reverse order
  - Press again to return to normal order
- **Ctrl+C**: Stop the bot

## Terminal Output

Monitor the terminal for:
- Bot initialization (green)
- Channel connection status (cyan)
- Chat messages:
  - Channel owner's name in yellow
  - Key fragments in red
  - Success messages in green
- Order toggle status (cyan)

## Configuration

Settings in `config.py`:
```python
KEY_FRAGMENT_LENGTH = 5    # Length of each fragment
REQUIRED_FRAGMENTS = 3     # Fragments needed for full key
PASTE_DELAY = 0.1         # Seconds between operations
```

## Pattern Matching

- Full keys: `[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}`
- Fragments: `\b[A-Z0-9](?:\s*[A-Z0-9]){4}\b`
  - Matches 5-character sequences
  - Allows optional spaces between characters
  - Word boundaries prevent partial matches

## Error Handling

The bot handles:
- Window focus failures
- Clipboard operation errors
- Invalid key formats
- Incomplete sequences
- Connection issues

## Important Notes

- Keep Steam "Enter Product Code" window open
- Ensure text cursor is in code entry box
- Window focus is handled automatically
- Logs are saved in `logs` directory

## Limitations

- Only processes channel owner's messages
- Requires Steam window to remain open
- Windows OS required for window management
