from funnys import *
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.enums import ParseMode
from random import choice

# ********* READING MY BOT TOKEN ***********#
with open('token.txt', 'r') as token_file:  #
    token = token_file.read()               #
# ******************************************#

bot = Bot(token=token)
dp = Dispatcher()

KRINGE = "Kringe"
BLACK = "Black"

dbfunny = DBFUNNY()
rfunny1 = RFUNNY('https://anekdoty.ru/cherniy-yumor/', (1, 6), 'holder-body')
rfunny2 = RFUNNY('https://anekdotov.net/anekdot/black/index-page-', (0, 37), 'anekdot', False)
rfunny3 = RFUNNY('https://anekdotovstreet.com/chernyy-yumor/', (1, 16), 'anekdot-text')


@dp.message(Command(commands='анекдот'))
async def send_text_funny(message: Message):
    kb = [
        [
            KeyboardButton(text=KRINGE),
            KeyboardButton(text=BLACK)
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply(text='Какой?', reply_markup=keyboard)


@dp.message()
async def send_echo(message: Message):
    text = message.text
    if text is not None:
        if text == KRINGE:
            joke: str = dbfunny.get_joke()
            await message.answer(f"<b>{joke}</b>", parse_mode=ParseMode.HTML)
        elif text == BLACK:
            joke: RFUNNY = choice((rfunny1, rfunny2, rfunny3))
            joke = joke.get_joke()
            await message.answer(f"<b>{joke}</b>", parse_mode=ParseMode.HTML)
        if text.startswith('/'):
            await message.reply(text="Не понял")


if __name__ == '__main__':
    dp.run_polling(bot)
