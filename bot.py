import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# 1. BotFather'dan olingan API Token'ni kiriting
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

# 2. Saytingiz manzili (Render, Railway yoki serveringiz domeni)
WEBAPP_URL = "https://ustago.up.railway.app"  # O'zingizning domeningizga o'zgartiring

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    # Telegram ichida Mini App tugmasi
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
                    url="https://t.me/tokhirov0777"  # Sizning Telegram username'ingiz
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
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
