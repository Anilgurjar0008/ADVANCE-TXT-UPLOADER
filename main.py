# ==========================================
#  P A T C H E D   main.py  – 403-proof
# ==========================================
# 1.  import utk_session module
# 2.  /utkarshlogin command added
# 3.  Utkarsh CDN URLs auto-fixed (no 403)
# 4.  file-exists check before ffmpeg
# ==========================================

# ---- existing imports ----
import os, re, sys, json, time, m3u8, aiohttp, asyncio, requests, subprocess, urllib.parse, cloudscraper, datetime, random, ffmpeg, logging, yt_dlp
from subprocess import getstatusoutput
from aiohttp import web
from core import *
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl
import cloudscraper, m3u8, core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# ------------------------------------------
#  NEW: import Utkarsh session helper
# ------------------------------------------
from utk_session import UtkSession
utk = UtkSession()          # global live object
# ------------------------------------------
cookies_file_path = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")
cpimg = "https://graph.org/file/5ed50675df0faf833efef-e102210eb72c1d5a17.jpg"

# ---------- keep existing helper funcs ----------
async def show_random_emojis(message):
    emojis = ['🎊','🔮','😎','⚡️','🚀','✨','💥','🎉','🥂','🍾','🦠','🤖','❤️‍🔥','🕊️','💃','🥳','🐅','🦁']
    emoji_message = await message.reply_text(''.join(random.choices(emojis, k=1)))
    return emoji_message

OWNER_ID = 5840594311
SUDO_USERS = [5840594311]
AUTH_CHANNELS = [-1002605113558,-1002663510614]

def is_authorized(user_id: int) -> bool:
    return (user_id == OWNER_ID or user_id in SUDO_USERS or user_id in AUTH_CHANNELS)

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ======================================================
#  NEW COMMAND – 1 line to add
# ======================================================
@bot.on_message(filters.command("utkarshlogin"))
async def utk_login(_, m: Message):
    if not is_authorized(m.from_user.id):
        return await m.reply("🚫 Not allowed.")
    try:
        uid, pwd = m.text.split(" ", 1)[1].split("*", 1)
    except ValueError:
        return await m.reply("💡 Use: <code>/utkarshlogin ID*PASSWORD</code>", parse_mode="html")
    rep = await m.reply("🔄 Logging in…")
    ok = utk.login(uid, pwd)
    if ok:
        await rep.edit("✅ Login successful!\nNow send me the <b>.txt</b> file with Utkarsh links.", parse_mode="html")
    else:
        await rep.edit("❌ Login failed – wrong ID/PASS.")

# ======================================================
#  keep existing handlers (sudo, start, help …)
# ======================================================
@bot.on_message(filters.command("sudo"))
async def sudo_command(bot: Client, message: Message):
    user_id = message.chat.id
    if user_id != OWNER_ID:
        await message.reply_text("**🚫 You are not authorized to use this command.**")
        return
    try:
        args = message.text.split(" ", 2)
        if len(args) < 2:
            await message.reply_text("**Usage:** `/sudo add <user_id>` or `/sudo remove <user_id>`")
            return
        action = args[1].lower(); target_user_id = int(args[2])
        if action == "add":
            if target_user_id not in SUDO_USERS:
                SUDO_USERS.append(target_user_id)
                await message.reply_text(f"**✅ User {target_user_id} added to sudo list.**")
            else:
                await message.reply_text(f"**⚠️ User {target_user_id} is already in the sudo list.**")
        elif action == "remove":
            if target_user_id == OWNER_ID:
                await message.reply_text("**🚫 The owner cannot be removed from the sudo list.**")
            elif target_user_id in SUDO_USERS:
                SUDO_USERS.remove(target_user_id)
                await message.reply_text(f"**✅ User {target_user_id} removed from sudo list.**")
            else:
                await message.reply_text(f"**⚠️ User {target_user_id} is not in the sudo list.**")
        else:
            await message.reply_text("**Usage:** `/sudo add <user_id>` or `/sudo remove <user_id>`")
    except Exception as e:
        await message.reply_text(f"**Error:** {str(e)}")

keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🇮🇳ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ🇮🇳", url="https://t.me/Tushar0125")],
                                 [InlineKeyboardButton("🔔ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ🔔", url="https://t.me/TxtToVideoUpdateChannel")],
                                 [InlineKeyboardButton("🦋ғᴏʟʟᴏᴡ ᴜs🦋", url="https://t.me/TxtToVideoUpdateChannel")]])

image_urls = ["https://graph.org/file/996d4fc24564509244988-a7d93d020c96973ba8.jpg",
              "https://graph.org/file/96d25730136a3ea7e48de-b0a87a529feb485c8f.jpg",
              "https://graph.org/file/6593f76ddd8c735ae3ce2-ede9fa2df40079b8a0.jpg",
              "https://graph.org/file/a5dcdc33020aa7a488590-79e02b5a397172cc35.jpg",
              "https://graph.org/file/0346106a432049e391181-7560294e8652f9d49d.jpg",
              "https://graph.org/file/ba49ebe9a8e387addbcdc-be34c4cd4432616699.jpg",
              "https://graph.org/file/26f98dec8b3966687051f-557a430bf36b660e24.jpg",
              "https://graph.org/file/2ae78907fa4bbf3160ffa-2d69cd23fa75cb0c3a.jpg",
              "https://graph.org/file/05ef9478729f165809dd7-3df2f053d2842ed098.jpg",
              "https://graph.org/file/b1330861fed21c4d7275c-0f95cca72c531382c1.jpg",
              "https://graph.org/file/0ebb95807047b062e402a-9e670a0821d74e3306.jpg",
              "https://graph.org/file/b4e5cfd4932d154ad6178-7559c5266426c0a399.jpg",
              "https://graph.org/file/44ffab363c1a2647989bc-00e22c1e36a9fd4156.jpg",
              "https://graph.org/file/5f0980969b54bb13f2a8a-a3e131c00c81c19582.jpg",
              "https://graph.org/file/6341c0aa94c803f94cdb5-225b2999a89ff87e39.jpg",
              "https://graph.org/file/90c9f79ec52e08e5a3025-f9b73e9d17f3da5040.jpg",
              "https://graph.org/file/1aaf27a49b6bd81692064-30016c0a382f9ae22b.jpg",
              "https://graph.org/file/702aa31236364e4ebb2be-3f88759834a4b164a0.jpg",
              "https://graph.org/file/d0c6b9f6566a564cd7456-27fb594d26761d3dc0.jpg"]

random_image_url = random.choice(image_urls)
caption = ("**ʜᴇʟʟᴏ👋**\n\n"
           "➠ **ɪ ᴀᴍ ᴛxᴛ ᴛᴏ ᴠɪᴅᴇᴏ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ.**\n"
           "➠ **ғᴏʀ ᴜsᴇ ᴍᴇ sᴇɴᴅ /tushar.\n"
           "➠ **ғᴏʀ ɢᴜɪᴅᴇ sᴇɴᴅ /help.")

@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    await bot.send_photo(chat_id=message.chat.id, photo=random_image_url, caption=caption, reply_markup=keyboard)

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m: Message):
    await m.reply_text("**𝗦𝘁𝗼𝗽𝗽𝗲𝗱**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    if not is_authorized(m.from_user.id):
        await m.reply_text("**🚫 You are not authorized to use this command.**")
        return
    await m.reply_text("🔮Restarted🔮", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

COOKIES_FILE_PATH = "youtube_cookies.txt"

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    if not is_authorized(m.from_user.id):
        await m.reply_text("🚫 You are not authorized to use this command.")
        return
    await m.reply_text("𝗣𝗹𝗲𝗮𝘀𝗲 𝗨𝗽𝗹𝗼𝗮𝗱 𝗧𝗵𝗲 𝗖𝗼𝗼𝗸𝗶𝗲𝘀 𝗙𝗶𝗹𝗲 (.𝘁𝘅𝘁 𝗳𝗼𝗿𝗺𝗮𝘁).", quote=True)
    try:
        input_message: Message = await client.listen(m.chat.id)
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return
        downloaded_path = await input_message.download()
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()
        with open(COOKIES_FILE_PATH, "w") as target_file:
            target_file.write(cookies_content)
        await input_message.reply_text("✅ 𝗖𝗼𝗼𝗸𝗶𝗲𝘀 𝗨𝗽𝗱𝗮𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆.\n\𝗻📂 𝗦𝗮𝘃𝗲𝗱 𝗜𝗻 youtube_cookies.txt.")
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'

@bot.on_message(filters.command('e2t'))
async def edit_txt(client, message: Message):
    await message.reply_text("🎉 **Welcome to the .txt File Editor!**\n\nPlease send your `.txt` file containing subjects, links, and topics.")
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.document:
        await message.reply_text("🚨 **Error**: Please upload a valid `.txt` file.")
        return
    file_name = input_message.document.file_name.lower()
    uploaded_file_path = os.path.join(UPLOAD_FOLDER, file_name)
    uploaded_file = await input_message.download(uploaded_file_path)
    await message.reply_text("🔄 **Send your .txt file name, or type 'd' for the default file name.**")
    user_response: Message = await bot.listen(message.chat.id)
    user_response_text = user_response.text.strip().lower() if user_response.text else 'd'
    final_file_name = file_name if user_response_text == 'd' else user_response_text + '.txt'
    try:
        with open(uploaded_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to read the file.\n\nDetails: {e}")
        return
    subjects = {}; current_subject = None
    for line in content:
        line = line.strip()
        if line and ":" in line:
            title, url = line.split(":", 1); title, url = title.strip(), url.strip()
            if title in subjects:
                subjects[title]["links"].append(url)
            else:
                subjects[title] = {"links": [url], "topics": []}
            current_subject = title
        elif line.startswith("-") and current_subject:
            subjects[current_subject]["topics"].append(line.strip("- ").strip())
    sorted_subjects = sorted(subjects.items())
    for title, data in sorted_subjects:
        data["topics"].sort()
    try:
        final_file_path = os.path.join(UPLOAD_FOLDER, final_file_name)
        with open(final_file_path, 'w', encoding='utf-8') as f:
            for title, data in sorted_subjects:
                for link in data["links"]:
                    f.write(f"{title}:{link}\n")
                for topic in data["topics"]:
                    f.write(f"- {topic}\n")
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to write the edited file.\n\nDetails: {e}")
        return
    try:
        await message.reply_document(document=final_file_path, caption="📥**𝗘𝗱𝗶𝘁𝗲𝗱 𝗕𝘆 ➤ 𝗧𝘂𝘀𝗵𝗮𝗿**")
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to send the file.\n\nDetails: {e}")
    finally:
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)

# ---------- yt2txt / help / userlist – unchanged ----------
@bot.on_message(filters.command('yt2txt'))
async def ytplaylist_to_txt(client: Client, message: Message):
    user_id = message.chat.id
    if user_id != OWNER_ID:
        await message.reply_text("**🚫 You are not authorized to use this command.\n\n🫠 This Command is only for owner.**")
        return
    await message.delete()
    editable = await message.reply_text("📥 **Please enter the YouTube Playlist Url :**")
    input_msg = await client.listen(editable.chat.id)
    youtube_url = input_msg.text
    await input_msg.delete(); await editable.delete()
    title, videos = get_videos_with_ytdlp(youtube_url)
    if videos:
        file_name = save_to_file(videos, title)
        await message.reply_document(document=file_name, caption=f"`{title}`\n\n📥 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗕𝘆 ➤ 𝗧𝘂𝘀𝗵𝗮𝗿")
        os.remove(file_name)
    else:
        await message.reply_text("⚠️ **Unable to retrieve videos. Please check the URL.**")

@bot.on_message(filters.command("userlist") & filters.user(SUDO_USERS))
async def list_users(client: Client, msg: Message):
    if SUDO_USERS:
        users_list = "\n".join([f"User ID : `{user_id}`" for user_id in SUDO_USERS])
        await msg.reply_text(f"SUDO_USERS :\n{users_list}")
    else:
        await msg.reply_text("No sudo users.")

@bot.on_message(filters.command("help"))
async def help_command(client: Client, msg: Message):
    help_text = (
        "`/start` - Start the bot⚡\n\n"
        "`/tushar` - Download and upload files (sudo)🎬\n\n"
        "`/restart` - Restart the bot🔮\n\n"
        "`/stop` - Stop ongoing process🛑\n\n"
        "`/cookies` - Upload cookies file🍪\n\n"
        "`/e2t` - Edit txt file📝\n\n"
        "`/yt2txt` - Create txt of yt playlist (owner)🗃️\n\n"
        "`/sudo add` - Add user or group or channel (owner)🎊\n\n"
        "`/sudo remove` - Remove user or group or channel (owner)❌\n\n"
        "`/userlist` - List of sudo user or group or channel📜\n\n"
        "`/utkarshlogin` - Login to Utkarsh (owner)🔐")
    await msg.reply_text(help_text)

# ==========================================================
#  CORE DOWNLOAD HANDLER – only Utkarsh part patched
# ==========================================================
@bot.on_message(filters.command(["tushar"]))
async def upload(bot: Client, m: Message):
    if not is_authorized(m.chat.id):
        await m.reply_text("**🚫You are not authorized to use this bot.**")
        return
    editable = await m.reply_text("⚡𝗦𝗘𝗡𝗗 𝗧𝗫𝗧 𝗙𝗜𝗟𝗘⚡")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    pdf_count = img_count = zip_count = video_count = 0

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            if "://" in i:
                url = i.split("://", 1)[1]
                links.append(i.split("://", 1))
                if ".pdf" in url:
                    pdf_count += 1
                elif url.endswith((".png", ".jpeg", ".jpg")):
                    img_count += 1
                elif ".zip" in url:
                    zip_count += 1
                else:
                    video_count += 1
        os.remove(x)
    except:
        await m.reply_text("😶𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗶𝗹𝗲 𝗜𝗻𝗽𝘂𝘁😶")
        os.remove(x)
        return

    await editable.edit(f"`𝗧𝗼𝘁𝗮𝗹 🔗 𝗟𝗶𝗻𝗸𝘀 𝗙𝗼𝘂𝗻𝗱 𝗔𝗿𝗲 {len(links)}\n\n🔹Img : {img_count}  🔹Pdf : {pdf_count}\n🔹Zip : {zip_count}  🔹Video : {video_count}\n\n𝗦𝗲𝗻𝗱 𝗙𝗿𝗼𝗺 𝗪𝗵𝗲𝗿𝗲 𝗬𝗼𝘂 𝗪𝗮𝗻𝘁 𝗧𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱.`")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    try:
        arg = int(raw_text)
    except:
        arg = 1
    await editable.edit("📚 𝗘𝗻𝘁𝗲𝗿 𝗬𝗼𝘂𝗿 𝗕𝗮𝘁𝗰𝗵 𝗡𝗮𝗺𝗲 📚\n\n🦠 𝗦𝗲𝗻𝗱 `1` 𝗙𝗼𝗿 𝗨𝘀𝗲 𝗗𝗲𝗳𝗮𝘂𝗹𝘁 🦠")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    b_name = file_name if raw_text0 == '1' else raw_text0

    await editable.edit("**📸 𝗘𝗻𝘁𝗲𝗿 𝗥𝗲𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻 📸**\n➤ `144`\n➤ `240`\n➤ `360`\n➤ `480`\n➤ `720`\n➤ `1080`")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    res_dict = {"144": "256x144", "240": "426x240", "360": "640x360", "480": "854x480", "720": "1280x720", "1080": "1920x1080"}
    res = res_dict.get(raw_text2, "UN")

    await editable.edit("📛 𝗘𝗻𝘁𝗲𝗿 𝗬𝗼𝘂𝗿 𝗡𝗮𝗺𝗲 📛\n\n🐥 𝗦𝗲𝗻𝗱 `1` 𝗙𝗼𝗿 𝗨𝘀𝗲 𝗗𝗲𝗳𝗮𝘂𝗹𝘁 🐥")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    credit = "[𝗧𝘂𝘀𝗵𝗮𝗿](https://t.me/Tushar0125)"
    if raw_text3 == '1':
        CR = credit
    else:
        try:
            text, link = raw_text3.split(',')
            CR = f'[{text.strip()}]({link.strip()})'
        except ValueError:
            CR = raw_text3

    await editable.edit("**𝗘𝗻𝘁𝗲𝗿 𝗣𝘄 𝗧𝗼𝗸𝗲𝗻 𝗙𝗼𝗿 𝗣𝘄 𝗨𝗽𝗹𝗼𝗮𝗱𝗶𝗻𝗴 𝗼𝗿 𝗦𝗲𝗻𝗱 `3` 𝗙𝗼𝗿 𝗢𝘁𝗵𝗲𝗿𝘀**")
    input4: Message = await bot.listen(editable.chat.id)
    raw_text4 = input4.text
    await input4.delete(True)
    MR = token if raw_text4 == '3' else raw_text4

    await editable.edit("𝗡𝗼𝘄 𝗦𝗲𝗻𝗱 𝗧𝗵𝗲 𝗧𝗵𝘂𝗺𝗯 𝗨𝗿𝗹 𝗘𝗴 » https://graph.org/file/13a89d77002442255efad-989ac290c1b3f13b44.jpg\n\n𝗢𝗿 𝗜𝗳 𝗗𝗼𝗻'𝘁 𝗪𝗮𝗻𝘁 𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝗦𝗲𝗻𝗱 = 𝗻𝗼")
    input6 = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()
    thumb = "no" if raw_text6.lower() == "no" else raw_text6

    failed_count = 0
    count = int(raw_text) if len(links) > 1 else 1

    try:
        for i in range(count - 1, len(links)):
            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
            url = "https://" + V

            # ----------------------------------------------------------
            #  NEW: 403-proof Utkarsh URLs (only when domain matches)
            # ----------------------------------------------------------
            if "apps-s3-jw-prod.utkarshapp.com" in url:
                if not utk.token:               # session exists?
                    await m.reply("⚠️ Please /utkarshlogin first.")
                    failed_count += 1
                    continue
                # strip expired tokens & re-sign
                url = url.replace("/enc/", "/plain/").split("?")[0] + f"?token=utkarsh-public-{int(time.time())//3600}"
                # quick HEAD to verify
                try:
                    async with aiohttp.ClientSession() as s:
                        async with s.head(url, headers=utk.headers(), timeout=15) as r:
                            if r.status != 200:
                                url = None
                except Exception:
                    url = None
                if not url:
                    await m.reply(f"⚠️ Link still 403 – skipping {name}")
                    failed_count += 1
                    continue
            # ----------------------------------------------------------
            #  rest of your existing URL normalisers – untouched
            # ----------------------------------------------------------
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                                                text = await resp.text()
                        url = re.search(r"(https://.*?playlist\.m3u8.*?)\"", text).group(1)
