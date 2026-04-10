from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import Message
from aiogram import F
from aiogram.filters import Command

from os import getenv
from dotenv import load_dotenv

import asyncio
import re
import random
import unicodedata

load_dotenv()

TOKEN = getenv("TOKEN")
PROXY = getenv("SOCKS5_PROXY")
BOT_VERSION = "0.1.0"

if PROXY:
    session = AiohttpSession(proxy=f"socks5://{PROXY}")
else:
    session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply(f"здарова!\nя присылаю картинку на каждое сообщение, где есть 'бе' или 'be'\nэтого шедеврального бота сделал @m1lkydev\n\nBeBot {BOT_VERSION}")

def normalize_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
 
    normalized = unicodedata.normalize("NFKD", text)
    
    return "".join(
        ch for ch in normalized
        if ch.isalnum() or ch.isspace()
    )

@dp.message(~F.command)
async def catch_all(message: Message):
    raw = message.html_text or message.text or ""
    clean_text = normalize_text(raw)
    text_lower = clean_text.lower()

    idx = None
    for k in (
        "бе", "be", "bе", "бe", "бё", "bє", "бє", "Bе", "Бе", "BE", "БE", "BЁ", "БЁ",
        "𝓫𝓮", "𝖇𝖊", "𝐛𝐞", "𝑏𝑒", "𝒃𝒆", "𝗯𝗲", "𝘣𝘦", "𝙗𝙚", "b𝖊", "b𝔢", "b𝕖", "б𝖊", "б𝔢", "б𝕖",
        "b𝒆", "b𝓮", "b𝗲", "b𝘦", "b𝙚", "ⳝᥱ", "𝙱𝚎", "𝔅𝔢", "𝔟𝔢", "𝖡𝖊", "𝖻𝖾",
        "bḛ", "бḛ", "b̵e", "б̵e", "bͤe", "бͤe", "b̄e", "б̄e", "ḃe", "б̇e", "b̈e", "б̈e",
        "`be`", "'be'", '"be"', "‘be’", "“be”", "-be-", "~be~", ".be.", ":be:", ";be;", ",be,", "/be/", "\\be\\",
        "`бе`", "'бе'", '"бе"', "‘бе’", "“бе”", "-бе-", "~бе~", ".бе.", ":бе:", ";бе;", ",бе,", "/бе/", "\\бе\\",
        "b.e", "b-e", "b_e", "b~e", "b'e", "b`e", "b:e", "b;e", "b/e", "b\\e",
        "б.е", "б-е", "б_е", "б~е", "б'е", "б`е", "б:е", "б;е", "б/е", "б\\е",
        "b.𝖊", "b-𝖊", "b_𝖊", "b~𝖊", "b'𝖊", "b`𝖊", "b:𝖊", "b;𝖊", "b/𝖊", "b\\𝖊",
        "б.𝖊", "б-𝖊", "б_𝖊", "б~𝖊", "б'𝖊", "б`𝖊", "б:𝖊", "б;𝖊", "б/𝖊", "б\\𝖊",
        "b e", "b•e", "b∙e", "b★e", "b☆e", "b✦e",
        "б е", "б•е", "б∙е", "б★е", "б☆е", "б✦е",
        "bｅ", "bｅ", "bｅ", "bｅ", "bｅ", "бｅ", "бｅ", "бｅ", "бｅ", "b𝙚", "б𝙚"
    ):
        found = text_lower.find(k)
        if found != -1 and (idx is None or found < idx):
            idx = found

    if idx is None:
        return

    path, caption = random.choice([
        (getenv("IMAGE_PATH", "./be.jpg"), None),
    ])

    await bot.send_photo(
        chat_id=message.chat.id,
        photo=FSInputFile(path),
        caption=caption,
        reply_to_message_id=message.message_id
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())