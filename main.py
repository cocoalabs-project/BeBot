import asyncio, json

from aiogram import Bot, Dispatcher, F
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import FSInputFile, Message
from aiogram.filters import Command

from os import getenv

with open(getenv("BEBOT_CONFIG_PATH", "./config.json"), "r") as f:
    config = json.load(f)

TOKEN = getenv("BEBOT_TOKEN")
GLOBAL_IMAGE_PATH = config.get("global_image_path", "./be.jpg")
GLOBAL_CAPTION = config.get("global_caption", "")
WORDS = config.get(
    "words",
    [
        {"word": "бе", "image_path": "{}", "caption": "{}"},
        {"word": "be", "image_path": "{}", "caption": "{}"},
        {"word": "бэ", "image_path": "{}", "caption": "{}"}
    ]
)
BOT_VERSION = "0.2.0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_readable_list_of_words(for_start: bool):
    list_ = ""
    for i, word in enumerate(WORDS):
        list_ += f"'{word["word"]}', "
        if i+1 == len(WORDS):
            list_ = list_[:-abs(6 + len(word["word"]))]
            if for_start:
                list_ += f" или '{word["word"]}'"
    return list_

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.reply(
        text="здарова!\n"
           + f"я присылаю картинку на каждое сообщение, где есть {await get_readable_list_of_words(True)}\n\n"
           + 'этого шедеврального бота сделал <a href="https://t.me/m1lkydev">@m1lkydev</a> '
           + 'из очередного конфликта <a href="https://t.me/iam_cocoa">@iam_cocoa</a> в осени 2025 года с одним чатом, '
           + 'которого уже нет\n\n'
           + "исходники бота: https://github.com/cocoalabs-project/BeBot"
           + "\n\n"
           + f"BeBot {BOT_VERSION}",
        parse_mode="HTML"
    )

@dp.message(Command("words"))
async def words_command(message: Message):
    message.reply(await get_readable_list_of_words())

@dp.message(~F.command)
async def catch_all(message: Message):
    text = message.text.lower() if message.text else ""
    for word in WORDS:
        image_path = GLOBAL_IMAGE_PATH \
                     if word.get("image_path", "{}") == "{}" \
                     else word.get("image_path", "{}")
        caption = GLOBAL_CAPTION \
                  if word.get("caption", "{}") == "{}" \
                  else word.get("caption", "{}")

        if word["word"] in text:
            await message.reply_photo(
                FSInputFile(image_path),
                caption=caption
            )
            return # Update 0.3.0 will include a custom setting 
                   # instead of a hard termination of the function

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
