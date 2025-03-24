from Aizen import app
from Aizen.core.call import TgBot as devine
from Aizen.utils.database import is_music_playing, music_off
from Aizen.utils.decorators import AdminRightsCheck
from Aizen.utils.inline import close_markup
from config import BANNED_USERS

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

@app.on_message(filters.command(["pause", "cpause"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await devine.pause_stream(chat_id)

    buttons = [
        [
            InlineKeyboardButton(
                text="ʀᴇsᴜᴍᴇ", callback_data=f"ADMIN Resume|{chat_id}"
            ),
            InlineKeyboardButton(
                text="ʀᴇᴘʟᴀʏ", callback_data=f"ADMIN Replay|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ᴄʟᴏsᴇ", callback_data="close"
            ),
        ]
    ]
    await message.reply_text(
        _["admin_2"].format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons),
    )




@app.on_callback_query(filters.regex("close"))
async def close_stream(cli, callback_query):
     await callback_query.message.delete(
         
     )