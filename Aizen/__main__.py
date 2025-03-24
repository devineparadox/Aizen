import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from Aizen import LOGGER, app, userbot
from Aizen.core.call import TgBot
from Aizen.misc import sudo
from Aizen.plugins import ALL_MODULES
from Aizen.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    await sudo()

    try:
        users = await get_gbanned()
        BANNED_USERS.update(users)

        users = await get_banned_users()
        BANNED_USERS.update(users)

    except Exception as e:
        LOGGER(__name__).error(f"Error fetching banned users: {e}")

    await app.start()

    for module in ALL_MODULES:
        importlib.import_module("Aizen.plugins." + module)

    LOGGER("Aizen.plugins").info("Successfully Imported Modules...")

    await userbot.start()
    await TgBot.start()

    try:
        await TgBot.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("Aizen").error("No active group call found! Retrying in 10 seconds...")
        await asyncio.sleep(10)
        await TgBot.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except Exception as e:
        LOGGER("Aizen").error(f"Error starting stream: {e}")

    await TgBot.decorators()

    LOGGER("Aizen").info("Powered by @devine_network")

    await idle()

    await app.stop()
    await userbot.stop()

    LOGGER("Aizen").info("Stopping Aizen Bot...")


if __name__ == "__main__":
    asyncio.run(init())