# cleaner_bot.py
import asyncio
import logging
import re
from aiogram import Bot, Dispatcher
from aiogram.filters import ChatTypeFilter
from aiogram.types import Message
from aiogram.enums import ChatType

# ---------------- CONFIG ----------------
TOKEN = "8534997492:AAHlG2hdvkZO1d09uMbwgly3AwrZgWuxIf8"

# ---- Siz yozgan kalit so'zlar ----
KEYWORDS = [
    "kanalimiz😎", "Tarifi", "OLTIN RAQAMLAR 7777", "💰Narxi", "MOBIUZ",
    "TEZ SOTILIB KETADI ULGURIB QOLING", "FARGONA TUNGI CHAT",
    "👠🅰️🅰️🅰️🅰️🅰️🥂", "HAR JUMA AKSIYALARI",
    "K. O. L. L. E. K. S. I. Y. A  S. I 🦋",
    "✅PIJAMALAR💣💣💣💣", "Документ кламиз", "Регистрация",
    "Whatsap✅Tелеграм✅Имо✅", "olib ketaman", "1kerak sroshniga",
    "🚕🚕  🚕🚕", "Toshkentga yuraman",
    "Rishton atrofida odam oʻsha olamiz tel", "olamiz",
    "OPTOM", "AKSIYA", "SKIDKA", "Reklamachi",
    "BREND TAVARLARI", "ОДАМ ОЛАМИЗ", "🅰️🅰️🅰️🅰️🅰️🅰️🅰️🅰️",
    "FERAMONLI PARFYUMLAR", "odam bor", "pochta bor",
    "mashina kerak", "kampilek odam bor", "kompilekt odam bor",
    "✅LICHEBNIY INTIM kosmetikalar", "TAKRORLANMAS KECHA XADYA ETING!"
]

# Hammasini lower ga o‘tkazamiz
KEYWORDS = list(set(k.lower() for k in KEYWORDS))

# REGEX pattern (super tez)
REGEX_PATTERN = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)

# ---------------- START BOT ----------------
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Guruh va superguruhlar uchun filtr
@dp.message(ChatTypeFilter(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP]))
async def cleaner(message: Message):

    if not message.text:
        return

    text = message.text.lower()

    # REGEX orqali tekshirish
    if REGEX_PATTERN.search(text):

        try:
            await message.delete()
            print(f"[O'CHIRILDI] → {text}")
        except Exception as e:
            print("❌ Xabarni o‘chirib bo‘lmadi! Botga ADMIN huquqi bering.")
            print("Xatolik:", e)


async def main():
    print("🚀 Cleaner Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
