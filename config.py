
from os import getenv


PREFIXES = ['.', '!', '?']
NAME = "NandhaUB"
API_ID = getenv('API_ID', 6)
API_HASH = getenv('API_HASH', "eb06d4abfb49dc3eeb1aeb98ae0f581e")
S_STRING = getenv('S_STRING', "...")
GIST_TOKEN = getenv('GIST', "...")

PORT = int(getenv("PORT", 8080))
BIND_ADDRESS = str(getenv("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))

HELP = {}
HELP_COLUMNS = 4
