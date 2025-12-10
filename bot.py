import asyncio
import logging
import re
from datetime import datetime, timedelta

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
    "FERAMONLI PARFYUMLAR", "АВТО КОБЛТ ", "СРОЧНО  2 КИШИ КЕРАК", "ПОЧТА ХИЗМАТИМИЗ БОР", "3 дона  жойимиз  бор ", "олиб  кетамиз", "юрамиз", "КЕТАДИГАНЛАР  булса",
    "✅LICHEBNIY INTIM kosmetikalar", "TAKRORLANMAS KECHA XADYA ETING!", "ГИЖЖАЛАРДАН БУТКУЛ ҚУТУЛИН!", "✅Тез шомолаш",
    "⚠️Шошилинг — акция чегараланган!", "Бу гижжалар ички органларингизни зарарлайди, ва натижада", "Фақат 72 соат ичида барча гижжалар чиқиб кетади",
    "АЁЛ  йуловчилар  бор ", "KAZINO UZ CHAT ORIGINAL", "KAZINO", "2 КИШИ КЕРАК", "976656444", "+998999776445", "999776445", "YO'LMA - YO'L QO'QON", "Egalariga jonatilmoqda", "Ertaga yana dastafka viloyatga chiqadi✅",
    "yetkazib berish 2kun ichda ✅", "adminga odam qoshdim", "UYIDA OʻTIRIB ISHLASHNI ISTAGAN", "To'lliq ma'lumot olish uchun lichkamga yozing",
    "AYOL VA QIZLARIMIZ UCHUN", "KIRSANGIZ CHIQOLMAY QOLASIZ! ", "🅰️🅰️🅰️🅰️🅰️🅰️🅰️", "HALIYAM O'TIRIPSIZMI",
    "FOYDALANING EFFECTINI SEZING", "+998911515189", "Moshina bor", "Qiziqganlarga lichkamga yozsin", "✅ Xamma uchun ish taklif qilaman",
    "Eng kamida 1 mlndan  30  milliongacha  pul topasiz", "batafsil ma’lumot uchun lichkamga yozing", "UYIDA OʻTIRIB ISHLASHNI ISTAGAN AYOL VA QIZLARIMIZ",
    "5 ta bo'sh ish o'rni bor. Ta'lim bepul", "3 дона  жойимиз  бо", "олиб  кетамиз", "+998999776445", "+998884136677",
    "TEL QILORASLAR KETADIGONLAR", "+998905884243", "ONLAYN ISHGA TAKLIF", "Assalomu aleykum uyda oʼtirgan holda onlayn ishlashni hohlaysizm", "🅰️🅰️🅱️🆎🆎🆎🆑🅾️", "hammasi noldan oʼrgatilinadi",
    "staj ketadi", "914708861", "+998916910747", "𝗣𝗢𝗖𝗛𝗧𝗔 𝗢𝗟𝗔𝗠𝗜𝗭", "ЮРАМАН", "МАШИНА КОБАЛЬТ", "машена жентира", "оламиз"
]

KEYWORDS = list(set(k.lower() for k in KEYWORDS))
REGEX_PATTERN = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.IGNORECASE)

# ---- LOGGING ----
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------- START BOT ----------------
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ---------------- GLOBAL ----------------
# Har bir guruh uchun oxirgi tozalash vaqtini saqlaymiz
group_cleanup_times = {}


# -------------------------------------------------------------------
#   🔥 1) Kalit so'zlarni topib o'chirish
# -------------------------------------------------------------------
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def cleaner(message: types.Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    chat_id = message.chat.id
    text = message.text.lower()

    # Kalit so'z bo'lsa — o'chiriladi
    if REGEX_PATTERN.search(text):
        try:
            await message.delete()
        except Exception as e:
            logger.error(f"Xabar o'chirilmadi: {e}")


# -------------------------------------------------------------------
#   🔥 2) Har 2 kunda avtomatik guruhni tozalash
# -------------------------------------------------------------------
async def auto_cleaner():
    while True:
        try:
            for chat_id, last_time in list(group_cleanup_times.items()):

                # 2 kun bo‘ldimi?
                if datetime.utcnow() - last_time >= timedelta(days=2):

                    # Guruhni tozalash
                    try:
                        # oxirgi 48 soatdagi xabarlarni o'chirish
                        async for msg in bot.iter_history(chat_id, limit=500):
                            try:
                                await bot.delete_message(chat_id, msg.message_id)
                            except:
                                pass

                        # Xabar yozish
                        try:
                            await bot.send_message(chat_id, "♻️ *Guruh tozalandi!*", parse_mode="Markdown")
                        except:
                            pass

                        # vaqtni yangilash
                        group_cleanup_times[chat_id] = datetime.utcnow()

                    except Exception as e:
                        logger.error(f"Guruhni tozalashda xatolik {chat_id}: {e}")

        except Exception as e:
            logger.error(f"Auto-cleaner xatolik: {e}")

        await asyncio.sleep(3600)  # 1 soatda 1 marta tekshiradi


# -------------------------------------------------------------------
#   🔥 3) Bot guruhga qo‘shilganda uni ro‘yxatga olish
# -------------------------------------------------------------------
@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    for user in message.new_chat_members:
        if user.id == (await bot.get_me()).id:
            # Bot guruhga qo‘shildi
            group_cleanup_times[message.chat.id] = datetime.utcnow()
            try:
                await message.answer("🧹 Tozalovchi bot ishga tushdi!")
            except:
                pass


# -------------------------------------------------------------------
async def on_startup(_):
    asyncio.create_task(auto_cleaner())


# -------------------------------------------------------------------
if __name__ == "__main__":
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )
