import asyncio
import pyrogram 
import config 

from nandha import app, log
from strings import RESTART_TEXT
from web import keep_alive, web_server
from aiohttp import web


async def start_services():        
        server = web.AppRunner(web_server())
        await server.setup()
        await web.TCPSite(server, config.BIND_ADDRESS, config.PORT).start()
        log.info("Web Server Initialized Successfully")
        log.info("=========== Service Startup Complete ===========")

        asyncio.create_task(keep_alive())
        log.info("Keep Alive Service Started")
        log.info("=========== Initializing Web Server ===========")
     
async def main():
     log.info('PYROGRAM HAS BEEN STARTED!')
     await start_services()
     await app.start()
     await app.send_message('me', text=RESTART_TEXT)
     await pyrogram.idle()






        
if __name__ == "__main__":
     asyncio.get_event_loop().run_until_complete(main())
     
  
  
    
