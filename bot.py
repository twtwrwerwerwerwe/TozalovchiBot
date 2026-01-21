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
    "FERAMONLI PARFYUMLAR", "АВТО КОБЛТ ", "СРОЧНО  2 КИШИ КЕРАК", "ПОЧТА ХИЗМАТИМИЗ БОР", "3 дона  жойимиз  бор ", "олиб  кетамиз", "юрамиз", "КЕТАДИГАНЛАР  булса",
    "✅LICHEBNIY INTIM kosmetikalar", "TAKRORLANMAS KECHA XADYA ETING!", "ГИЖЖАЛАРДАН БУТКУЛ ҚУТУЛИН!", "✅Тез шомолаш",
    "⚠️Шошилинг — акция чегараланган!", "Бу гижжалар ички органларингизни зарарлайди, ва натижада", "Фақат 72 соат ичида барча гижжалар чиқиб кетади",
    "АЁЛ  йуловчилар  бор ", "KAZINO UZ CHAT ORIGINAL", "KAZINO", "2 КИШИ КЕРАК", "976656444", "999776445", "999776445", "YO'LMA - YO'L QO'QON", "Egalariga jonatilmoqda", "Ertaga yana dastafka viloyatga chiqadi✅",
    "yetkazib berish 2kun ichda ✅", "adminga odam qoshdim", "UYIDA OʻTIRIB ISHLASHNI ISTAGAN", "To'lliq ma'lumot olish uchun lichkamga yozing",
    "AYOL VA QIZLARIMIZ UCHUN", "KIRSANGIZ CHIQOLMAY QOLASIZ! ", "🅰️🅰️🅰️🅰️🅰️🅰️🅰️", "HALIYAM O'TIRIPSIZMI",
    "FOYDALANING EFFECTINI SEZING", "911515189", "Moshina bor", "Qiziqganlarga lichkamga yozsin", "✅ Xamma uchun ish taklif qilaman",
    "Eng kamida 1 mlndan  30  milliongacha  pul topasiz", "batafsil ma’lumot uchun lichkamga yozing", "UYIDA OʻTIRIB ISHLASHNI ISTAGAN AYOL VA QIZLARIMIZ",
    "5 ta bo'sh ish o'rni bor. Ta'lim bepul", "3 дона  жойимиз  бо", "олиб  кетамиз", "999776445", "+998884136677",
    "TEL QILORASLAR KETADIGONLAR", "905884243", "ONLAYN ISHGA TAKLIF", "Assalomu aleykum uyda oʼtirgan holda onlayn ishlashni hohlaysizm", "🅰️🅰️🅱️🆎🆎🆎🆑🅾️", "hammasi noldan oʼrgatilinadi",
    "staj ketadi", "914708861", "916910747", "𝗣𝗢𝗖𝗛𝗧𝗔 𝗢𝗟𝗔𝗠𝗜𝗭", "ЮРАМАН", "МАШИНА КОБАЛЬТ", "машена жентира", "оламиз",
    "946858486", "916858486", "932349830", "🏥Аптека", "https://t.me/aptekaonlinesam/618402", "Адрес:Беруний кўчаси 32А-уй", "Аптека: ALPHA PHARM",
    "Ориентир", "@alphapharm111", "Иш вакти: 7:00 дан 23:00 гача", "ULAMOLAR BISOTIDAN", "Saodatga yetaklovchi hikmatlar", "@Bahodir2580", " Suhandon: Muhammad Nur",
    "@Mohira_Diamond_Director", "901460112", "Bts", "Emu pochtalaridan chqaramiz", "Qizlajonla Sovunli gul buketlani", "ulab qoyamiz  uzb bòylab", "ҚОН БОСИМИМ 10 ЙИЛДАН БЕРИ 180 ГА 120 БЎЛАР ЭДИ",
    "✅Бу мўъжиза эди", "@JoinHiderar_Bot", "https://shop.mxmedia.uz/faeton/?web=2", "944931293", "YURAMIZ", "@TozalaBot", "💆‍♀️Болаларим кундан кунга инжиқлашиб кетяпти.", "Тезда уланиб олинглар бу ёпиқ канал кейин қидириб топа олмайсизлар!👇",
    "bir oyli vipi bilan", "Murojaat uchun Lichka", "Songi dizayindagi DARVOZALAR", "@Darvoza_666", "⏰ 11 yillik uzluksiz tajriba 🤝1500 dan ortiq mijozlar", "Namangan", "Namangandan", "Namanganga", "NAMANGAN", "namangan",
    "Ketadiganlar", "2 kishi kerak", "termizga", "termiz", "beshariq", "bewariq", "501554406", "Beshariqga", "besh ariqga", "MiLadiy_boutique", "Dastafka bormi", 'Milady', "Чекланмаган миқдорда", "Пенаблок сотилади",
    "@Xisoblovchibot", "Қиз фарзандингиз бўлса, асло мушук боқманг! Сабабини билсангиз, шокка тушишингиз аниқ", "93.437.66.59", "олиб кетаман"
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
