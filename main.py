import os
import logging
from funnys import *
from usefull import *
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile, InputMediaVideo
from aiogram.enums import ParseMode
from random import choice
from datetime import datetime

DATE = str(datetime.now().strftime('%I %M%p on %B %d, %Y'))

logging.basicConfig(filename=f'log/logging {DATE}.log',
                    format='%(asctime)s %(message)s',
                    filemode='w', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('FunnyBot')
logger.setLevel(logging.INFO)
logger.info('START')
# ********* READING MY BOT TOKEN ********** #
with open('token.txt', 'r') as token_file:  #
    token = token_file.read()               #
# ***************************************** #

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
yt_downloader = YT()


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


@dp.message(Command(commands=['download_video']))
async def get_request_download_yt(message: Message):
    username = message.from_user.username
    chat_type = message.chat.type
    logger.info(f'REQUEST FOR DOWNLOADING FROM YOUTUBE FROM {username} IN {chat_type}')
    if message.chat.type in (CHAT_GROUP, CHAT_SUPERGROUP):
        logger.info(f'REQUEST FOR DOWNLOADING FROM YOUTUBE FOR {username} DENIED')
        await message.reply(text='Не могу выполнить это действие в групповом чате! Пиши мне в лс -> '
                                 'https://t.me/Sabir_Dobryak_bot')
    else:
        await message.reply(text='Кидай ссылку 🤔...')


@dp.message(F.text.regexp(r'https:\/\/(?:www\.)?(?:youtube\.com|youtu.be)\/.+'))
async def send_yt_video(message: Message):
    username = message.from_user.username
    chat_type = message.chat.type
    if chat_type == CHAT_PRIVATE:
        logger.info(f'GOT YOUTUBE LINK FROM {username}')
        link = message.text
        my_message = await message.reply('Ищу по ссылке... 🤓')
        answer: Optional[str] = yt_downloader.download(link, username)
        if isinstance(answer, str):
            await my_message.edit_text(text=answer)
            logger.info(f'VIDEO FOR {username} IN IS NOT LOADED')
        elif answer is None:
            logger.info(f'VIDEO FOR {username} IS DOWNLOADED')
            await my_message.edit_text(text='Видео нашёл, скачал, отправляю... 🫡')
            title = os.listdir('videos/')[0]
            try:
                title = f'./videos/{title}'
                video = FSInputFile(path=title)
                await bot.send_document(message.chat.id, video)
                await message.answer('Пожалуйста😊!')
                logger.info(f'VIDEO FOR {username} IS SENT SUCCESSFULLY')
            except Exception as e:
                logger.error(f'VIDEO FOR {username} IS NOT SENT')
                logger.error(e)
            finally:
                os.remove(title)


if __name__ == '__main__':
    dp.run_polling(bot)
    logger.info('SHUTDOWN')
