
import logging
from config import *
from pyrogram import Client, filters


# monkey-patchings
filters.command.__defaults__ = (PREFIXES, False)



log = logging.getLogger(__name__)


FORMAT = f"[APP] %(message)s"
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'), logging.StreamHandler()], format=FORMAT)


app = Client(
  name=NAME,
  api_id=API_ID,
  api_hash=API_HASH,
  session_string=S_STRING,
  plugins=dict(root='nandha'),
  
)
