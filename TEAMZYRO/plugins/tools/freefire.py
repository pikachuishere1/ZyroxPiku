from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from datetime import datetime
from TEAMZYRO import app

DEFAULT_REGION = "ind"

@app.on_message(filters.command("ff"))
async def freefire_info(client: Client, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("Usage: /ff <player_id> [region]")
            return

        args = message.text.split()
        player_id = args[1]
        region = args[2].lower() if len(args) > 2 else DEFAULT_REGION

        api_url = f"https://ariiflexlabs-playerinfo-icxc.onrender.com/ff_info?uid={player_id}&region={region}"
        response = requests.get(api_url)

        if response.status_code != 200:
            await message.reply_text("Failed to fetch player info. Please check the ID and try again.")
            return

        data = response.json()

        account = data.get("AccountInfo", {})
        profile = data.get("AccountProfileInfo", {})
        guild = data.get("GuildInfo", {})
        captain = data.get("captainBasicInfo", {})
        social = data.get("socialinfo", {})

        name = account.get("AccountName", captain.get("nickname", "N/A"))
        level = account.get("AccountLevel", captain.get("level", "N/A"))
        exp = account.get("AccountEXP", captain.get("exp", "N/A"))
        region_display = account.get("AccountRegion", captain.get("region", "N/A")).upper()

        create_time = (
            datetime.fromtimestamp(int(account.get("AccountCreateTime", captain.get("createAt", 0)))).strftime('%Y-%m-%d')
            if account.get("AccountCreateTime") else 'N/A'
        )
        last_login = (
            datetime.fromtimestamp(int(account.get("AccountLastLogin", captain.get("lastLoginAt", 0)))).strftime('%Y-%m-%d %H:%M')
            if account.get("AccountLastLogin") else 'N/A'
        )

        br_rank = account.get('BrRankPoint', captain.get('rankingPoints', 'N/A'))
        br_max = account.get('BrMaxRank', captain.get('maxRank', 'N/A'))
        cs_rank = account.get('CsRankPoint', captain.get('csRankingPoints', 'N/A'))
        cs_max = account.get('CsMaxRank', captain.get('csMaxRank', 'N/A'))

        weapons = ', '.join(map(str, account.get('EquippedWeapon', []))) or 'N/A'
        outfits = ', '.join(map(str, profile.get('EquippedOutfit', []))) or 'N/A'

        guild_name = guild.get('GuildName', 'N/A')
        guild_level = guild.get('GuildLevel', 'N/A')
        guild_members = f"{guild.get('GuildMember', 'N/A')}/{guild.get('GuildCapacity', 'N/A')}"

        signature = social.get('AccountSignature', 'N/A')
        prefer_mode = social.get('AccountPreferMode', 'N/A')
        prefer_mode = prefer_mode.split('_')[-1] if prefer_mode else 'N/A'

        info_text = f"""
🎮 **Free Fire Player Info** 🎮

👤 **Basic Info:**
├─ Name: `{name}`
├─ Level: `{level}`
├─ EXP: `{exp}`
├─ Region: `{region_display}`
├─ Created: `{create_time}`
└─ Last Login: `{last_login}`

🏆 **Rank Info:**
├─ BR Rank: `{br_rank} pts (Max: {br_max})`
└─ CS Rank: `{cs_rank} pts (Max: {cs_max})`

👕 **Equipment:**
├─ Weapons: `{weapons}`
└─ Outfit: `{outfits}`

🏛️ **Guild Info:**
├─ Name: `{guild_name}`
├─ Level: `{guild_level}`
└─ Members: `{guild_members}`

📝 **Social:**
├─ Signature: `{signature}`
└─ Preferred Mode: `{prefer_mode}`

🔗 **Profile Link:** [View in FF](https://freefiremobile.com/profile/{player_id})
"""

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_ff_{player_id}_{region}")],
            [InlineKeyboardButton("👨‍💻 Credits", url="https://t.me/sukuna_dev")]
        ])

        await message.reply_text(
            info_text.strip(),
            reply_markup=buttons,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.reply_text(f"An error occurred:\n`{str(e)}`")

@app.on_callback_query(filters.regex(r"^refresh_ff_(\d+)_(\w+)$"))
async def refresh_ff_info(client, callback_query):
    try:
        player_id = callback_query.matches[0].group(1)
        region = callback_query.matches[0].group(2)

        api_url = f"https://ariiflexlabs-playerinfo-icxc.onrender.com/ff_info?uid={player_id}&region={region}"
        response = requests.get(api_url)

        if response.status_code != 200:
            await callback_query.answer("Failed to refresh data", show_alert=True)
            return

        data = response.json()
        account = data.get("AccountInfo", {})

        last_login = (
            datetime.fromtimestamp(int(account.get('AccountLastLogin', 0))).strftime('%Y-%m-%d %H:%M')
            if account.get("AccountLastLogin") else 'N/A'
        )

        old_text_lines = callback_query.message.text.splitlines()
        new_text_lines = []
        for line in old_text_lines:
            if "Last Login:" in line:
                new_text_lines.append(f"└─ Last Login: `{last_login}`")
            else:
                new_text_lines.append(line)

        await callback_query.edit_message_text(
            "\n".join(new_text_lines),
            reply_markup=callback_query.message.reply_markup
        )
        await callback_query.answer("Data refreshed!")

    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)
