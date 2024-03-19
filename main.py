from setup.commands import *
from setup.variables import *
from utilities.funnys import *
from utilities.usefull import *
from utilities.funcs import *
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.enums import ParseMode
from random import choice


@dp.message(Command(commands=COMMAND1[1:]))
async def get_request_anecdote(message: Message):
    name_to_log(logger, 'REQUEST FOR JOKES FROM', message)
    kb = [
        [
            KeyboardButton(text=KRINGE),
            KeyboardButton(text=BLACK)
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply(text='Какой?', reply_markup=keyboard)


@dp.message(Command(commands=[COMMAND2[1:]]))
async def get_request_horoscope(message: Message):
    name_to_log(logger, 'REQUEST FOR HOROSCOPE FROM', message)
    kb = [
        [KeyboardButton(text=elem) for elem in HOROSYMBS]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply(text='Кто ты?', reply_markup=keyboard)


@dp.message(Command(commands=[COMMAND3[1:]]))
async def get_request_horoscope(message: Message):
    name_to_log(logger, 'ASKED FOR PHOTO_TO_PDF FROM', message)
    await message.reply(text='Скинь мне одну или несколько картинок и я сделаю из них pdf')


@dp.message(Command(commands=[COMMAND4[1:]]))
async def get_request_horoscope(message: Message):
    name_to_log(logger, 'MESSAGE (MORNING) FROM', message)
    await bot.send_photo(message.chat.id, morning.get_image(), caption=morning.get_caption())


@dp.message(F.text.in_([KRINGE, BLACK]))
async def send_joke(message: Message) -> None:
    text = message.text
    name_to_log(logger, 'MESSAGE (JOKE) FROM', message)
    if text == KRINGE:
        joke: str = dbfunny.get_joke()
        await message.answer(f"<b>{joke}</b>", parse_mode=ParseMode.HTML)
    elif text == BLACK:
        joke: RFUNNY = choice((rfunny1, rfunny2, rfunny3))
        joke = joke.get_joke()
        await message.answer(f"<b>{joke}</b>", parse_mode=ParseMode.HTML)
    name_to_log(logger, 'RESPONSE SENT TO', message)


@dp.message(F.text.in_(HOROSYMBS))
async def send_horoscope(message: Message) -> None:
    text = message.text
    name_to_log(logger, 'MESSAGE (HOROSCOPE) FROM', message)
    response: tuple[str, str] | None = aztro.get_answer(text)
    if response is not None:
        sign, text = response
        await message.answer(f"<b>{sign}</b>\n{text}", parse_mode=ParseMode.HTML)
    else:
        await message.answer(f"<b>Ничего не нашёл(</b>", parse_mode=ParseMode.HTML)
    name_to_log(logger, 'RESPONSE SENT TO', message)


async def check_message(message: Message) -> Union[bool, str]:
    user_id = message.from_user.id
    chat_type = message.chat.type
    name_to_log(logger, f'REQUEST FOR IMAGE TO PDF IN {chat_type} FROM', message)
    if message.chat.type in (CHAT_GROUP, CHAT_SUPERGROUP):
        name_to_log(logger, f'REQUEST FOR IMAGE TO PDF DENIED FOR', message)
        await message.reply(text='Не могу выполнить это действие в групповом чате! Пиши мне в лс -> '
                                 'https://t.me/Sabir_Dobryak_bot')
        return False
    return str(user_id)


@dp.message(F.media_group_id)
async def photos_to_pdf(message: Message, album: List[Message]):
    if not (username := await check_message(message)):
        return
    pdfworker = PDFWorker(bot, username)
    my_message = await message.answer("Фото получил сохраняю..🤓.")
    for i, photo in enumerate(album, 1):
        if photo.photo:
            await my_message.edit_text(f"Сохраняю фото номер {i}🫡")
            await pdfworker.save_photo(photo.photo[-1].file_id, i)
        elif photo.document and photo.document.file_name.endswith(PHOTO_EXT):
            await my_message.edit_text(f"Сохраняю фото номер {i}🫡")
            await pdfworker.save_photo(photo.document.file_id, i)
        else:
            await bot.send_message(message.from_user.id, "Среди фото необрабатываемый файл😯! Его пропустил")
    logger.info(f'IMAGES FROM {username} SAVED')
    name_to_log(logger, 'IMAGES SAVED FROM', message)
    await pdfworker.send_pdf_photo(my_message, message)
    name_to_log(logger, 'PDF SENT FOR', message)


@dp.message((F.photo | F.document))
async def photo_to_pdf(message: Message):
    if not (username := await check_message(message)):
        return
    pdfworker = PDFWorker(bot, username)
    my_message = await message.answer("Фото получил сохраняю... 🤓")
    await my_message.edit_text(f"Сохраняю фото номер 1🫡")
    if message.photo:
        await pdfworker.save_photo(message.photo[-1].file_id)
    elif message.document.file_name.endswith(PHOTO_EXT):
        await pdfworker.save_photo(message.document.file_id)
    name_to_log(logger, 'IMAGE SAVED FROM', message)
    await pdfworker.send_pdf_photo(my_message, message)
    name_to_log(logger, 'PDF SENT FOR', message)


if __name__ == '__main__':
    setup_bot_commands(bot)
    dp.message.middleware(MediaGroupMiddleware())
    try:
        logger.info('WORKING')
        dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f'CRITICAL ERROR: {e}')
    finally:
        bot.session.close()
    logger.info('SHUTDOWN')
