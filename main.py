import os
import asyncio
import datetime
import pytz
import platform
from platform import python_version
from psutil import boot_time, cpu_percent, disk_usage, virtual_memory
from telegram import __version__
from telegram.constants import ParseMode
from telegram.ext import CommandHandler
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.errors import FloodWait

load_dotenv()

app = Client(
    name="st_userbot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    session_string=os.getenv("SESSION_STRING")
)

bot = Client(
    name="st_bot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

BOT_LIST = [x.strip() for x in os.getenv("BOT_LIST").split(' ')]
CHANNEL_OR_GROUP_ID = int(os.getenv("CHANNEL_OR_GROUP_ID"))
MESSAGE_ID = int(os.getenv("MESSAGE_ID"))
TIME_ZONE = os.getenv("TIME_ZONE")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot.start()


async def main():
    print("Status Checker Bot Started")
    async with app:
        while True:
            TEXT = "This is the live bot status of all Bots 🤖"
            for bots in BOT_LIST:
                ok = await app.get_users(f"@{bots}")
                try:
                    await app.send_message(bots, "/ping")
                    await asyncio.sleep(2)
                    messages = app.get_chat_history(bots, limit=1)
                    async for x in messages:
                        msg = x.text
                    if msg == "/ping":
                        TEXT += f"\n\n**🤖-[{ok.first_name}](tg://openmessage?user_id={ok.id}): OFFLINE** 💀"
                        await bot.send_message(OWNER_ID, f'Alert {ok.first_name} is offline 💀')
                        await app.read_chat_history(bots)
                    else:
                        TEXT += f"\n\n**🤖-[{ok.first_name}](tg://openmessage?user_id={ok.id}): {msg}**"
                        await app.read_chat_history(bots)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
            time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
            date = time.strftime("%d %b %Y")
            time = time.strftime("%I:%M: %p")
            TEXT += f"\n\n--Last checked on--: \n{date}\n{time} ({TIME_ZONE})\n\n**Refreshes Automatically After Every 15 Min.**"
            await bot.edit_message_text(int(CHANNEL_OR_GROUP_ID), MESSAGE_ID, TEXT)
            await asyncio.sleep(900)


async def system_status(update, context):
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    status = "<b>======[ SYSTEM INFO ]======</b>\n\n"
    status += "<b>sʏsᴛᴇᴍ ᴜᴘᴛɪᴍᴇ:</b> <code>" + str(uptime) + "</code>\n"

    uname = platform.uname()
    status += "<b>sʏsᴛᴇᴍ:</b> <code>" + str(uname.system) + "</code>\n"
    status += "<b>ɴᴏᴅᴇ ɴᴀᴍᴇ:</b> <code>" + str(uname.node) + "</code>\n"
    status += "<b>ʀᴇʟᴇᴀsᴇ:</b> <code>" + str(uname.release) + "</code>\n"
    status += "<b>ᴠᴇʀsɪᴏɴ:</b> <code>" + str(uname.version) + "</code>\n"
    status += "<b>ᴍᴀᴄʜɪɴᴇ:</b> <code>" + str(uname.machine) + "</code>\n"
    status += "<b>ᴘʀᴏᴄᴇssᴏʀ:</b> <code>" + str(uname.processor) + "</code>\n\n"
    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += "<b>ᴄᴘᴜ ᴜsᴀɢᴇ:</b> <code>" + str(cpu) + " %</code>\n"
    status += "<b>ʀᴀᴍ ᴜsᴀɢᴇ:</b> <code>" + str(mem[2]) + " %</code>\n"
    status += "<b>sᴛᴏʀᴀɢᴇ ᴜsᴇᴅ:</b> <code>" + str(disk[3]) + " %</code>\n\n"
    status += "<b>ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ:</b> <code>" + python_version() + "</code>\n"
    status += "<b>ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ:</b> <code>" + str(__version__) + "</code>\n"
    await context.bot.sendMessage(
        update.effective_chat.id, status, parse_mode=ParseMode.HTML
    )


SYS_STATUS_HANDLER = CommandHandler(["stats", "sysinfo"], system_status, block=False)
rani.add_handler(SYS_STATUS_HANDLER)

bot.run(main())
