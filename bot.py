import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Telegram Bot Token
BOT_TOKEN = "8994199161:AAHctwnIncMvmhaRwwThT-d4nsGKLExbmcw"

# Saytingiz domeni
WEBAPP_URL = "https://ustago.up.railway.app"  # Agar server havolangiz boshqacha bo'lsa, shuni qo'yasiz

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛠️ UstaGo Platformasini Ochish",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="👨‍💻 Admin bilan bog'lanish",
                    url="https://t.me/tokhirov0777"
                )
            ]
        ]
    )

    welcome_text = (
        f"Salom, **{message.from_user.first_name}**! 👋\n\n"
        f"**UstaGo** — Usta va mijozlarni tezkor bog'lovchi rasmiy botga xush kelibsiz.\n\n"
        f"Pastdagi **'UstaGo Platformasini Ochish'** tugmasi orqali kerakli ustani topishingiz yoki o'z arizangizni qoldirishingiz mumkin!"
    )

    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=keyboard)

async def main():
    logging.basicConfig(level=logging.INFO)
    print("UstaGo boti muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
