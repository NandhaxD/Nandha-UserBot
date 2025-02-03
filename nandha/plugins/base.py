
from nandha import app, HELP, HELP_COLUMNS
from strings import START_TEXT
from pyrogram import filters, enums


HELP['start'] = "Check whether the program is alive or not."
@app.on_message(~filters.forwarded & filters.me & filters.command('start'))
async def start_func(app, message):
      await message.reply_text(START_TEXT)


HELP['help'] = 'Shows help commands.'
@app.on_message(~filters.forwarded & filters.me & filters.command('help'))
async def help_func(app, message):
    txt = message.text
    if len(txt.split()) == 1:
        text = "<b><emoji id=5416117059207572332>➡️</emoji> Help Commands:</b>\n\n"
        
        commands = sorted(list(HELP.keys()))
        
        rows = [commands[i:i + HELP_COLUMNS] for i in range(0, len(commands), HELP_COLUMNS)]
        
        formatted_rows = []
        for row in rows:
            formatted_keys = [f"<code>{key}</code>" for key in row]
            formatted_rows.append(", ".join(formatted_keys))
        
        text += "\n".join(formatted_rows)
        return await message.edit(text, parse_mode=enums.ParseMode.HTML)
          
    else:
        cmd = txt.split()[1].lower()
        cmd_msg = HELP.get(cmd, None)
        if not cmd_msg:
            return await message.edit('<emoji id=5465665476971471368>❌</emoji> <b>This command does not exist.</b>')
        else:
            text = f"<b><emoji id=5456140674028019486>⚡</emoji>Help for '{cmd}'</b>\n\n<code>{cmd_msg}</code>"
            return await message.edit(text, parse_mode=enums.ParseMode.HTML)
