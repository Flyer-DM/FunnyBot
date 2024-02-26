import logging
from funnys import *
from usefull import *
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile
from aiogram.enums import ParseMode
from random import choice
from datetime import datetime

DATE = str(datetime.now().strftime('%I %M%p on %B %d, %Y'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info('START')
# ********* READING MY BOT TOKEN ***********#
with open('token.txt', 'r') as token_file:  #
    token = token_file.read()               #
# ******************************************#

bot = Bot(token=token)
dp = Dispatcher()

CHAT_GROUP = 'group'
CHAT_PRIVATE = 'private'
CHAT_SUPERGROUP = 'supergroup'

KRINGE = "Kringe"
BLACK = "Black"
HOROSYMBS = '♈♉♊♋♌♍♎♏♐♑♒♓'

dbfunny = DBFUNNY()
logger.info('START OF WEB PARSING')
rfunny1 = RFUNNY('https://anekdoty.ru/cherniy-yumor/', (1, 6), 'holder-body')
rfunny2 = RFUNNY('https://anekdotov.net/anekdot/black/index-page-', (0, 37), 'anekdot', False)
rfunny3 = RFUNNY('https://anekdotovstreet.com/chernyy-yumor/', (1, 16), 'anekdot-text')
aztro = AZTRO()
logger.info('END OF WEB PARSING')


@dp.message(Command(commands=['anecdote']))
async def get_request_anecdote(message: Message):
    logger.info(f'REQUEST FOR JOKES FROM {message.from_user.username}')
    kb = [
        [
            KeyboardButton(text=KRINGE),
            KeyboardButton(text=BLACK)
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply(text='Какой?', reply_markup=keyboard)


@dp.message(Command(commands=['horoscope']))
async def get_request_horoscope(message: Message):
    logger.info(f'REQUEST FOR HOROSCOPE FROM {message.from_user.username}')
    kb = [
        [KeyboardButton(text=elem) for elem in HOROSYMBS]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply(text='Кто ты?', reply_markup=keyboard)


@dp.message(F.text.in_([KRINGE, BLACK]))
async def send_joke(message: Message):
    text = message.text
    logger.info(f'MESSAGE FROM {message.from_user.username}')
    if text == KRINGE:
        joke: str = dbfunny.get_joke()
        await message.answer(f"<b>{joke}</b>", parse_mode=ParseMode.HTML)
    elif text == BLACK:
        joke: RFUNNY = choice((rfunny1, rfunny2, rfunny3))
        joke = joke.get_joke()
        await message.answer(f"<b>{joke}</b>", parse_mode=ParseMode.HTML)
    logger.info(f'RESPONSE SENT TO {message.from_user.username}')


@dp.message(F.text.in_(HOROSYMBS))
async def send_horoscope(message: Message):
    text = message.text
    logger.info(f'MESSAGE FROM {message.from_user.username}')
    response: tuple[str, str] | None = aztro.get_answer(text)
    if response is not None:
        sign, text = response
        await message.answer(f"<b>{sign}</b>\n{text}", parse_mode=ParseMode.HTML)
    else:
        await message.answer(f"<b>Ничего не нашёл(</b>", parse_mode=ParseMode.HTML)
    logger.info(f'RESPONSE SENT TO {message.from_user.username}')


@dp.message(F.media_group_id)
async def handle_albums(message: Message, album: List[Message]):
    username = message.from_user.username
    chat_type = message.chat.type
    logger.info(f'REQUEST FOR IMAGE TO PDF FROM {username} IN {chat_type}')
    if message.chat.type in (CHAT_GROUP, CHAT_SUPERGROUP):
        logger.info(f'REQUEST FOR IMAGE TO PDF FOR {username} DENIED')
        await message.reply(text='Не могу выполнить это действие в групповом чате! Пиши мне в лс -> '
                                 'https://t.me/Sabir_Dobryak_bot')
        await bot.send_message(message.from_user.id, "Скинь мне одну или несколько картинок и я сделаю из них pdf.")
        return
    photos = []
    my_message = await message.answer("Фото получил сохраняю...")
    for element in album:
        if element.photo:
            photos.append(element.photo[-1].file_id)
    for i, file_id in enumerate(photos, 1):
        await my_message.edit_text(f"Сохраняю фото номер {i}")
        file = await bot.get_file(file_id)
        file_path = file.file_path
        downloaded_file = await bot.download_file(file_path)
        with open(f"./photos/photo_{username}_{i}.jpg", "wb") as new_file:
            new_file.write(downloaded_file.read())
    await my_message.edit_text("Сохранил! Преобразую...")
    pdfer = PDFer(username)
    pdf = FSInputFile(pdfer())
    await my_message.edit_text("Преобразовал! Отправляю...")
    await bot.send_document(message.chat.id, pdf, caption="Ваш PDF-файл")
    await my_message.delete()
    pdfer.clear()


if __name__ == '__main__':
    dp.message.middleware(MediaGroupMiddleware())
    dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())
    logger.info('SHUTDOWN')
