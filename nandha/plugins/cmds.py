
import os
import asyncio

from subprocess import getoutput

from pyrogram import filters, types, raw, errors
from nandha import app, HELP, log

from nandha.help.utils import paste, LANGS
from nandha.help.scripts import with_premium



HELP['copy_or_forward'] = "Copy or forward a content from restricted or any channel/group/private."
@app.on_message(filters.command(['forward', 'copy']) & filters.me & ~filters.forwarded)
async def copy_or_forward_func(app, message):
    # Check if the command format is correct
    if len(message.text.split()) != 4:
        return await message.edit('<b><emoji id=5465665476971471368>❌</emoji> Incorrect format! Example:</b> <code>.copy chat_id start_id end_id</code>')

    # Extract command arguments
    _, chat_id, start_id, end_id = message.text.split()

    # Validate that start_id and end_id are integers
    if not (start_id.isdigit() and end_id.isdigit()):
        return await message.edit('<b><emoji id=5465665476971471368>❌</emoji> start_id and end_id must be integer values!</b>')

    # Convert start_id and end_id to integers
    start_id, end_id = int(start_id), int(end_id)

    # Validate that the range is valid
    if end_id <= start_id:
        return await message.edit('<b><emoji id=5465665476971471368>❌</emoji> The end_id must be greater than start_id!</b>')

    try:
        success = 0
        failed = 0

        # Fetch messages in the specified range
        msgs = await app.get_messages(chat_id, message_ids=list(range(start_id, end_id + 1)))

        # Process each message
        for idx, msg in enumerate(msgs, start=1):

            if idx % 5 == 0:
                 await asyncio.sleep(5)
            try:
                if message.command[0] == 'forward':
                    await msg.forward(message.chat.id)
                else:
                    await msg.copy(message.chat.id)
                success += 1
            except Exception as e:
                failed += 1
                # Optionally log the error for debugging
                log.error(f"Error processing message {msg.id}: {e}")

        # Provide feedback on the operation
        await message.reply_text(f'<b><emoji id=5206607081334906820>✅</emoji> {success} Successful and <emoji id=5465665476971471368>❌</emoji> {failed} failed.</b>')
      
    except (errors.UsernameNotOccupied, errors.PeerIdInvalid):
        return await message.edit('<b><emoji id=5274099962655816924>❗</emoji> Make sure to interact with that channel/group/private.</b>')
    except Exception as e:
        return await message.edit(f'<b><emoji id=5465665476971471368>❌</emoji> Unexpected error:</b> <code>{e}</code>')
           


HELP['vtt'] = "Voice to text module, reply to any voice message."
@app.on_message(filters.command('vtt') & ~filters.forwarded & filters.me)
@with_premium
async def voice_to_text_func(app, message):
       reply = message.reply_to_message
       voice = reply and reply.voice
       if voice:
            chat = await app.resolve_peer(message.chat.id)
            result = await app.invoke(
            raw.functions.messages.TranscribeAudio(
                peer=chat,
                msg_id=reply.id
            )
        )
            text = f"<b><emoji id=5447410659077661506>🌐</emoji> Voice to text:</b>\n\n{result.text}"
            return await message.edit(text)
       
       else:
           return await message.edit('<emoji id=5465665476971471368>❌</emoji> <b>Reply to voice message.</b>')




HELP['tr'] = "Translate any text messages, usage: .tr lang_code"
@app.on_message(~filters.forwarded & filters.me & filters.command(['translate', 'tr']))
@with_premium
async def translate_func(app, message):
    # Check if the message is a reply and contains text or caption
    reply = message.reply_to_message
    if not reply or not (reply.text or reply.caption):
        return await message.edit('<emoji id=5465665476971471368>❌</emoji> <b>Reply to a message with text or caption.</b>')

    # Extract the command arguments
    command_args = message.text.split()

    # If no language code is provided, show the list of supported languages
    if len(command_args) == 1:
        text = "<emoji id=5447410659077661506>🌐</emoji> <b>Supported Languages:</b>\n\n"
        formatted_langs = [f"{lang['lang_title']}: [{lang['lang_code']}]" for lang in LANGS]
        text += "<blockquote expandable>" + "\n".join(formatted_langs) + "</blockquote>"
        return await message.edit(text)

    # Extract the language code from the command
    lang_code = command_args[1].lower()

    # Validate the language code
    supported_codes = {lang['lang_code']: lang['lang_title'] for lang in LANGS}

    if lang_code not in list(supported_codes.keys()):
        return await message.edit(f'<emoji id=5465665476971471368>❌</emoji> <b>Unsupported language code: {lang_code}</b>')

    try:
        # Translate the replied message
        translated = await app.translate_message_text(
            to_language_code=lang_code,
            chat_id=message.chat.id,
            message_ids=reply.id
        )

        # Format and send the translated message
        translation_text = f"<emoji id=5447410659077661506>🌐</emoji> <b>Translated to {supported_codes[lang_code]}:</b>\n\n{translated.text}"
        await message.edit(translation_text)

    except Exception as e:
        await message.edit(f'<emoji id=5465665476971471368>❌</emoji> <b>Translation failed:</b> <code>{e}</code>') 



HELP['paste'] = 'Paste long text messages or document, Reply to any text message or document with .paste'
@app.on_message(filters.me & ~filters.forwarded & filters.command('paste'))
async def paste_func(app, message):
       reply = message.reply_to_message
       text_content = reply and (reply.text or reply.caption)
       document_content = reply and reply.document and (reply.document.file_size/(1024*1024) <= 3)
       
       if document_content:
            file = await reply.download()
            try:
               content = open(file, 'r').read()
               paste_text = await paste(content)
            except Exception as e:
               return await message.edit(f'<emoji id=5465665476971471368>❌</emoji> <b>Error when reading/pasting file content</b>: <code>{e}</code>')
            finally:
               if os.path.exists(file):
                    os.remove(file)
         
       elif text_content:
            paste_text = await paste(reply.text or reply.caption)
         
       else:
            return await message.edit('<b><emoji id=5465665476971471368>❌</emoji> Reply to message text or text document file.</b>')

       await message.edit(paste_text)



HELP['logs'] = 'Shows app loggings...'
@app.on_message(filters.me & ~filters.forwarded & filters.command('logs'))
async def logs_func(app, message):
    file = 'logs.txt'

    if os.path.exists(file):
        text = getoutput(f'cat {file}')
        if len(text) >= 4000:
            paste_text = await paste(text)
            await message.reply_document(file, caption=paste_text)
            await message.delete()
        else:
            logs_text = (
                f"<pre language='shell'> LOGGING (INFO-LEVEL):\n\n{text}\n</pre>"
            )
            await message.edit(logs_text)
    else:
        await message.edit('<b><emoji id=5465665476971471368>❌</emoji> File not found.</b>')






