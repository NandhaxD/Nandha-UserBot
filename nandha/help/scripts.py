

from typing import Optional, Union
from pyrogram import types, Client


def with_premium(func):
    async def wrapped(client: Client, message: types.Message):
        if not client.me.is_premium:
            await message.edit("<b><emoji id=5465665476971471368>❌</emoji> Premium account is required!</b>")
        else:
            return await func(client, message)

    return wrapped


def with_args(text: str):
    def decorator(func):
        async def wrapped(client: Client, message: types.Message):
            if message.text and len(message.text.split()) == 1:
                await message.edit(text)
            else:
                return await func(client, message)

        return wrapped

    return decorator


def get_args_raw(message: Union[types.Message, str], use_reply: bool = None) -> str:
    """Returns text after command.

    Args:
        message (Union[Message, str]): Message or text.

        use_reply (bool, optional): Try to get args from reply message if no args in message. Defaults to None.

    Returns:
        str: Text after command or empty string.
    """
    if isinstance(message, types.Message):
        text = message.text or message.caption
        args = text.split(maxsplit=1)[1] if len(text.split()) > 1 else ""

        if use_reply and not args:
            args = message.reply_to_message.text or message.reply_to_message.caption

    elif not isinstance(message, str):
        return ""

    return args or ""

