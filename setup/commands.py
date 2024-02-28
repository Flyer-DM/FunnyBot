from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot


COMMAND1 = "/anecdote"
COMMAND2 = "/horoscope"
COMMAND3 = "/photo_to_pdf"


async def setup_bot_commands(bot: Bot):
    bot_commands = [
        BotCommand(command=COMMAND1, description="Рассказать шутку"),
        BotCommand(command=COMMAND2, description="Показать гороскоп на сегодня"),
        BotCommand(command=COMMAND3, description="Преобразовать картинки в pdf файл")
    ]
    await bot.set_my_commands(bot_commands, BotCommandScopeDefault())
