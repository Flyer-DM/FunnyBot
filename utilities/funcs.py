from logging import Logger
from aiogram.types import Message


def name_to_log(logger: Logger, message: str, user: Message):
    curr_info = ''
    if username := user.from_user.username:
        curr_info += username
    if surname := user.from_user.last_name:
        curr_info += f' - {surname}'
    if name := user.from_user.first_name:
        curr_info += f' {name}'
    if curr_info:
        curr_info = f'({curr_info})'
    user_info = f'{user.from_user.id} {curr_info}'
    logger.info(f'{message} {user_info}')
