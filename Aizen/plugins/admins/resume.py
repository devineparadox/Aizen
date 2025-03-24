from pyrogram import filters
from pyrogram.types import Message

from Aizen import app
from Aizen.core.call import TgBot as devine
from Aizen.utils.database import is_music_playing, music_on
from Aizen.utils.decorators import AdminRightsCheck
from Aizen.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(filters.command(["resume", "cresume"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await devine.resume_stream(chat_id)
    buttons_resume = [
        [
            InlineKeyboardButton(
                text="sᴋɪᴘ", callback_data=f"ADMIN Skip|{chat_id}"
            ),
            InlineKeyboardButton(
                text="ᴘᴀᴜsᴇ", callback_data=f"ADMIN Pause|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ᴄʟᴏsᴇ", callback_data="close"
            ),
        ]
    ]
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons_resume),
    )


@app.on_callback_query(filters.regex("close"))
async def close_stream(cli, callback_query):
     await callback_query.message.delete()