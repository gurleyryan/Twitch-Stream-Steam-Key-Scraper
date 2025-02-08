# Steam key configuration
KEY_FRAGMENT_LENGTH = 5  # Length of each key fragment
REQUIRED_FRAGMENTS = 3   # Number of fragments needed for complete key
KEY_PATTERN = r'\b[A-Z0-9](?:\s*[A-Z0-9]){4}\b'  # Matches 5 chars with optional spaces between them

# Keep full key pattern as is
FULL_KEY_PATTERN = r"[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}"

# Automation settings
PASTE_DELAY = 0.1    # Seconds to wait between paste and submit