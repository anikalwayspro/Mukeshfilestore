#(©)CodeXBotz




import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from utils import verify_user, check_token

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    message=update
    reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data = "about"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
    
    if len(update.command) != 2:
      
        await bot.send_message(
            chat_id=update.chat.id,
            text=START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup=reply_markup,
            reply_to_message_id=update.id
        )
        return
    data = update.command[1]

    if data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(update.from_user.id) != str(userid):
            return await update.reply_text(
                text="<b>ᴇxᴘɪʀᴇᴅ ʟɪɴᴋ ᴏʀ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ !</b>",
                protect_content=True
            )
        is_valid = await check_token(bot, userid, token)
        if is_valid == True:
            await update.reply_text(
                text=f"<b>ʜᴇʟʟᴏ {update.from_user.mention} 👋,\nʏᴏᴜ ᴀʀᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴇʀɪғɪᴇᴅ !\n\nɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ғᴏʀ ᴀʟʟ ᴜʀʟ ᴜᴘʟᴏᴀᴅɪɴɢ ᴛɪʟʟ ᴛᴏᴅᴀʏ ᴍɪᴅɴɪɢʜᴛ.</b>",
                protect_content=True
            )
            await verify_user(bot, userid, token)
        else:
            return await update.reply_text(
                text="<b>ᴇxᴘɪʀᴇᴅ ʟɪɴᴋ ᴏʀ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋ !</b>",
                protect_content=True
            ) 
@Bot.on_message(filters.private & ~filters.via_bot & filters.regex(pattern=".*http.*"))
async def echo(bot, update):
    if not await check_verification(bot, update.from_user.id) and Config.TECH_VJ == True:
        btn = [[
            InlineKeyboardButton("👨‍💻 ᴠᴇʀɪғʏ", url=await get_token(bot, update.from_user.id, f"https://telegram.me/{Config.TECH_VJ_BOT_USERNAME}?start="))
            ],[
            InlineKeyboardButton("🔻 ʜᴏᴡ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋ ᴀɴᴅ ᴠᴇʀɪғʏ 🔺", url=f"{Config.TECH_VJ_TUTORIAL}")
        ]]
        await update.reply_text(
            text="<b>ᴅᴜᴇ ᴛᴏ ᴏᴠᴇʀʟᴏᴀᴅ ᴏɴ ʙᴏᴛ ʏᴏᴜ ʜᴀᴠᴇ ᴠᴇʀɪғʏ ғɪʀsᴛ\nᴋɪɴᴅʟʏ ᴠᴇʀɪғʏ ғɪʀsᴛ\n\nɪғ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴠᴇʀɪғʏ ᴛʜᴇɴ ᴛᴀᴘ ᴏɴ ʜᴏᴡ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ ᴛʜᴇɴ sᴇᴇ 60 sᴇᴄᴏɴᴅ ᴠɪᴅᴇᴏ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴠᴇʀɪғʏ ʙᴜᴛᴛᴏɴ ᴀɴᴅ ᴠᴇʀɪғу</b>",
            protect_content=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )

# Run verification system on startup

#===m========================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(
                "Join Channel",
                url = client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
