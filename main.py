from variables import *
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.enums import ParseMode
from random import choice


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


if __name__ == '__main__':
    dp.run_polling(bot)
    logger.info('SHUTDOWN')
