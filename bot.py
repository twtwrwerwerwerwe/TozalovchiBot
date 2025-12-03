# cleaner_bot.py
import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

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

# Hammasini lowerga o‘tkazamiz
KEYWORDS = list(set(k.lower() for k in KEYWORDS))

# REGEX pattern — juda tez ishlaydi!
REGEX_PATTERN = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)

# ---------------- START BOT ----------------
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# Faqat guruh va superguruhdagi xabarlarni olish
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def cleaner(message: types.Message):

    # Chat turi GROUP yoki SUPERGROUP bo‘lishi shart
    if message.chat.type not in ["group", "supergroup"]:
        return

    text = message.text.lower()

    # Kalit so‘zlarni tekshirish
    if REGEX_PATTERN.search(text):

        try:
            await message.delete()
            print(f"[O'CHIRILDI] → {text}")
        except Exception as e:
            print("❌ Bot xabarni o‘chira olmadi! ADMIN huquqi kerak.")
            print("Xatolik:", e)


async def on_startup(_):
    print("🚀 Cleaner Bot ishga tushdi...")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
