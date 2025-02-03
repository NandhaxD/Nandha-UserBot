import asyncio

from nandha import app
from pyrogram import idle
from strings import RESTART_TEXT

async def main():
     await app.start()
     await app.send_message('me', text=RESTART_TEXT)
     await idle()
  
if __name__ == "__main__":
     loop = asyncio.get_event_loop()
     loop.run_until_complete(main())
  
  
    
