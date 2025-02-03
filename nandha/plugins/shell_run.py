import asyncio
import time
import html
import aiofiles
import os
from typing import Optional, Union, Tuple
from nandha import app, HELP
from nandha.help.utils import paste
from nandha.help.scripts import get_args_raw, with_args
from pyrogram import filters, types, enums


async def shell_exec(
    command: str,
    timeout: Optional[Union[int, float]] = None,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
) -> Tuple[int, str, str]:
    """Executes shell command and returns tuple with return code, decoded stdout and stderr"""
    process = await asyncio.create_subprocess_shell(
        cmd=command, stdout=stdout, stderr=stderr, shell=True
    )

    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout)
    except asyncio.exceptions.TimeoutError as e:
        process.kill()
        raise e

    return process.returncode, stdout.decode(), stderr.decode()


HELP['shell'] = "Run python shell, e.g .shell ls"
@app.on_message(
    ~filters.scheduled & filters.command(["shell", "sh"]) & filters.me & ~filters.forwarded
)
@with_args("<b>Command is not provided!</b>")
async def shell_handler(_: app, message: types.Message):
    await message.edit("<b><emoji id=5974235702701853774>🔃</emoji> Executing...</b>")

    cmd_text = get_args_raw(message)

    text = (
        "<b><emoji id=5821388137443626414>🌐</emoji> Language:</b>\n<code>Shell</code>\n\n"
        "<b><emoji id=6206214505630796400>💻</emoji> Command:</b>\n"
        f'<pre language="sh">{html.escape(cmd_text)}</pre>\n\n'
    )

    timeout = 60
    try:
        start_time = time.perf_counter()
        rcode, stdout, stderr = await shell_exec(command=cmd_text, timeout=timeout)
    except asyncio.exceptions.TimeoutError:
        text += (
            "<b><emoji id=5465665476971471368>❌</emoji> Error!</b>\n"
            f"<b>Timeout expired ({timeout} seconds)</b>"
        )
        await message.edit(text)
        return
    except Exception as e:
        text += (
            "<b><emoji id=5465665476971471368>❌</emoji>Unexpected Error!</b>\n"
            f"<b>({e.__class__.__name__})</b>"
        )
        await message.edit(text)
        return
     
    stop_time = time.perf_counter()
    code = html.escape(stderr or stdout)
    doc = False
    file_name = 'shell.txt'

    if len(code) > 4000:
        paste_text = await paste(code)
        if paste_text == 'Pasting failed':
            doc = True
            async with aiofiles.open(file_name, mode='w+') as file:
                await file.write(code)
        else:
            text += (
                "<b><emoji id=5363943823720333444>✨</emoji> Result</b>:\n"
                f"{paste_text}\n\n"
            )
    else:
        text += (
            "<b><emoji id=5363943823720333444>✨</emoji> Result</b>:\n"
            f"<code>{code}</code>\n\n"
        )

    text += f"<b>Completed in {round(stop_time - start_time, 5)} seconds with code {rcode}</b>"

    if doc:
        await message.reply_document(file_name)
        await message.edit(text, parse_mode=enums.ParseMode.HTML)
        if os.path.exists(file_name):
             os.remove(file_name)
    else:
        await message.edit(text)
