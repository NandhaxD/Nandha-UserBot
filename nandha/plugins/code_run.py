import asyncio
import html
import time
import random
import aiofiles
import io
import re

from contextlib import redirect_stderr, redirect_stdout
from traceback import print_exc
from pyrogram import filters, types, enums

from strings import CODE_RESULT_TEXT
from nandha import app, HELP
from nandha.help.utils import paste





async def aexec(code, client, message, timeout=None):
    exec(
        "async def __todo(client, message, *args):\n"
        + " from pyrogram import raw, types, enums\n"
        + " app = client\n"
        + " m = message\n"
        + " my = m.from_user\n"
        + " r = m.reply_to_message\n"
        + " u = m.from_user\n"
        + " ru = getattr(r, 'from_user', None)\n"
        + " p = print\n"
        + " here = m.chat.id\n"
        + "".join(f"\n {_l}" for _l in code.split("\n"))
    )

    f = io.StringIO()

    with redirect_stdout(f):
        await asyncio.wait_for(locals()["__todo"](client, message), timeout=timeout)

    return f.getvalue()
  

HELP['eval'] = "Run python code, [reval] for run replied eval."
@app.on_message(
    ~filters.scheduled & filters.command(["eval", "reval", 'e']) & filters.me & ~filters.forwarded
)
async def python_exec(client: app, message: types.Message):
    if len(message.command) == 1 and message.command[0] != "reval":
        return await message.edit_text("<b><emoji id=5465665476971471368>❌</emoji> Code to execute isn't provided</b>")

    if message.command[0] == "reval":
        if not message.reply_to_message:
            return await message.edit_text("<b><emoji id=5465665476971471368>❌</emoji> Code to execute isn't provided</b>")

        # Check if message is a reply to message with already executed code
        for entity in message.reply_to_message.entities:
            if (
                entity.type == enums.MessageEntityType.PRE
                and entity.language == "python"
            ):
                code = message.reply_to_message.text[
                    entity.offset : entity.offset + entity.length
                ]
                break
        else:
            code = message.reply_to_message.text
    else:
        code = message.text.split(maxsplit=1)[1]

    await message.edit_text(
        "<b><emoji id=5974235702701853774>🔃</emoji> Executing...</b>"
    )

    try:
        code = code.replace("\u00a0", "")

        start_time = time.perf_counter()
        result = await aexec(
            code, client, message, timeout=60
        )
        stop_time = time.perf_counter()

        # Replace account phone number to anonymous
        random_phone_number = "".join(str(random.randint(0, 9)) for _ in range(8))
        result = result.replace(client.me.phone_number, f"999{random_phone_number}")

        if not result:
            result = "No result"
        elif len(result) > 4000:
            paste_result = html.escape(await paste(result))

            if paste_result == "Pasting failed":
                async with aiofiles.open("error.txt", mode="w") as file:
                    await file.write(result)

                result = None
            else:
                result = paste_result

        elif re.match(r"^(https?):\/\/[^\s\/$.?#].[^\s]*$", result):
            result = html.escape(result)
        else:
            result = f"<pre>{html.escape(result)}</pre>"

        if result:
            return await message.edit_text(
                CODE_RESULT_TEXT.format(
                    emoji_id=5260480440971570446,
                    language="Python",
                    pre_language="python",
                    code=html.escape(code),
                    result=f"<b><emoji id=5363943823720333444>✨</emoji> Result</b>:\n"
                    f"{result}\n"
                    f"<b>Completed in {round(stop_time - start_time, 5)}s.</b>",
                ),
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        else:
            return await message.reply_document(
                document="error.txt",
                caption=CODE_RESULT_TEXT.format(
                    emoji_id=5260480440971570446,
                    language="Python",
                    pre_language="python",
                    code=html.escape(code),
                    result=f"<b><emoji id=5472164874886846699>✨</emoji> Result is too long</b>\n"
                    f"<b>Completed in {round(stop_time - start_time, 5)}s.</b>",
                ),
                  parse_mode=enums.ParseMode.HTML,
            )
    except asyncio.TimeoutError:
        return await message.edit_text(
            CODE_RESULT_TEXT.format(
                emoji_id=5260480440971570446,
                language="Python",
                pre_language="python",
                code=html.escape(code),
                result="<b><emoji id=5465665476971471368>❌</emoji> Timeout Error!</b>",
            ),
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except Exception as e:
        err = io.StringIO()
        with redirect_stderr(err):
            print_exc()

        return await message.edit_text(
            CODE_RESULT_TEXT.format(
                emoji_id=5260480440971570446,
                language="Python",
                pre_language="python",
                code=html.escape(code),
                result=f"<b><emoji id=5465665476971471368>❌</emoji> {e.__class__.__name__}: {e}</b>\n"
                f"Traceback: {html.escape(await paste(err.getvalue()))}",
            ),
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True,
      )



  
