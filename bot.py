# cleaner_bot.py
import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ---------------- CONFIG ----------------
TOKEN = "8534997492:AAHlG2hdvkZO1d09uMbwgly3AwrZgWuxIf8"

# ---- Kalit so'zlar ----
KEYWORDS = [
    "kanalimiz😎", "Tarifi", "OLTIN RAQAMLAR 7777", "💰Narxi", "MOBIUZ",
    "TEZ SOTILIB KETADI ULGURIB QOLING", "FARGONA TUNGI CHAT",
    "👠🅰️🅰️🅰️🅰️🅰️🥂", "HAR JUMA AKSIYALARI",
    "K. O. L. L. E. K. S. I. Y. A  S. I 🦋",
    "✅PIJAMALAR💣💣💣💣", "Документ кламиз", "Регистрация",
    "Whatsap✅Tелеграм✅Имо✅", "olib ketaman", "1kerak sroshniga",
    "🚕🚕  🚕🚕", "Toshkentga yuraman",
    "Rishton atrofida odam poʻsha olamiz tel", "olamiz",
    "OPTOM", "AKSIYA", "SKIDKA", "Reklamachi",
    "BREND TAVARLARI", "ОДАМ ОЛАМИЗ", "🅰️🅰️🅰️🅰️🅰️🅰️🅰️🅰️",
    "FERAMONLI PARFYUMLAR", "БАГАЖ БОР", "АВТО КОБЛТ "
    "✅LICHEBNIY INTIM kosmetikalar", "TAKRORLANMAS KECHA XADYA ETING!", "ГИЖЖАЛАРДАН БУТКУЛ ҚУТУЛИН!", "✅Тез шомолаш",
    "⚠️Шошилинг — акция чегараланган!", "Бу гижжалар ички органларингизни зарарлайди, ва натижада", "Фақат 72 соат ичида барча гижжалар чиқиб кетади"
]

# ---- Hammasini lowercase ----
KEYWORDS = list(set(k.lower() for k in KEYWORDS))

# ---- REGEX pattern ----
REGEX_PATTERN = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)

# ---- LOGGING ----
logging.basicConfig(
    level=logging.ERROR,  # ❗ faqat xatolar chiqsin
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# ---------------- START BOT ----------------
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def cleaner(message: types.Message):

    # Faqat grouplarda ishlasin
    if message.chat.type not in ["group", "supergroup"]:
        return

    text = message.text.lower()

    # Kalit so‘z bordimi?
    if REGEX_PATTERN.search(text):

        try:
            await message.delete()

        except Exception as e:
            # ❗ Faqat bitta ERROR log bo‘ladi, Railwayni portlatmaydi
            logger.error(f"Xabar o‘chirilmadi! Sabab: {e}")


async def on_startup(_):
    # ❗ hech qanday print/log yo‘q → Railway safe
    pass


if __name__ == "__main__":
    executor.start_polling(
        dp,
        skip_updates=True,   # eski xabarlarni o‘qimaydi → log kam
        on_startup=on_startup
    )
