# cleaner_bot.py
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums.chat_type import ChatType
import logging
import re
import os

# ---------------- CONFIG ----------------
TOKEN = "8534997492:AAHlG2hdvkZO1d09uMbwgly3AwrZgWuxIf8"

# Kalit so'zlar (o'chirilishi kerak bo'lganlar)
KEYWORDS = [
    "odam olaman", "yuraman", "yuraman", "yuramanmi", "yuramanmi?", "yuramanmi?",
    
]

# pastga yozilsa ham aniqlaydi
KEYWORDS = [k.lower() for k in KEYWORDS]

# ---------------- START BOT ----------------
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Xabarlarni tekshirish ---
@dp.message(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
async def cleaner(message: Message):

    # faqat text bo‘lsa
    if not message.text:
        return

    text = message.text.lower()

    # juda tez ishlashi uchun REGEX optimizatsiya
    for key in KEYWORDS:
        if key in text:
            try:
                await message.delete()
                print(f"[O'CHIRILDI] {key} | {text}")
            except:
                print("O'chirish muvaffaqiyatsiz (admin huquqlarini tekshiring)")
            return  # Bitta topsa bas, darhol chiqib ketadi


async def main():
    print("🚀 Cleaner Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
