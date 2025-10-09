from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import __version__ as pyrover
from pytgcalls.__version__ import __version__ as pytgver
from sys import version as pyver
import platform
import psutil

from config import BANNED_USERS
from TEAMZYRO import app
from TEAMZYRO.core.userbot import assistants
from TEAMZYRO.utils import bot_sys_stats
from TEAMZYRO.utils.decorators.language import language
from TEAMZYRO.utils.inline import supp_markup

@app.on_message(filters.command("stats") & ~filters.edited & ~filters.private & ~filters.bot & ~filters.via_bot & filters.user(assistants))
@language
async def stats_command(client, message: Message, _):
    msg = await message.reply_text(_["sys_1"])
    
    try:
        stats = await bot_sys_stats()
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        python_ver = pyver.split()[0]
        platform_sys = platform.system()
        platform_rel = platform.release()
        assistants_count = len(assistants)

        text = (
            f"🔧 **System Stats**\n\n"
            f"📱 **Pyrogram:** `{pyrover}`\n"
            f"📞 **Py-TgCalls:** `{pytgver}`\n"
            f"🐍 **Python:** `{python_ver}`\n"
            f"💻 **Platform:** `{platform_sys} {platform_rel}`\n"
            f"⚙️ **CPU:** `{cpu}%`\n"
            f"📟 **RAM:** `{ram}%`\n"
            f"💾 **Disk:** `{disk}%`\n\n"
            f"🤖 **Assistant Bots:** `{assistants_count}`\n"
            f"{stats}"
        )

        await msg.edit_text(text, reply_markup=supp_markup(message.from_user.id))
    except Exception as e:
        await msg.edit_text(f"❌ Failed to fetch stats:\n`{e}`")
