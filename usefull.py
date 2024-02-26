import os
import asyncio
import img2pdf
from typing import Any, Awaitable, Callable, Dict, List, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class MediaGroupMiddleware(BaseMiddleware):
    __version__ = '1.0.0'
    ALBUM_DATA: Dict[str, List[Message]] = {}
    DEFAULT_DELAY = 0.6

    def __init__(self, delay: Union[int, float] = DEFAULT_DELAY):
        self.delay = delay

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        try:
            self.ALBUM_DATA[event.media_group_id].append(event)
            return
        except KeyError:
            self.ALBUM_DATA[event.media_group_id] = [event]
            await asyncio.sleep(self.delay)
            data["album"] = self.ALBUM_DATA.pop(event.media_group_id)

        return await handler(event, data)


class PDFer:
    __version__ = '1.0.0'

    def __init__(self, username: str):
        self.username = username
        self.filename = f"{self.username}.pdf"

    def __call__(self):
        filespath = './photos/'
        photos = os.listdir(filespath)
        with open(f"{self.username}.pdf", "wb") as f:
            photos = list(filter(lambda name: self.username in name, photos))
            photos = list(map(lambda name: filespath + name, photos))
            pdf_data = img2pdf.convert(photos)
            f.write(pdf_data)
        [os.remove(photo) for photo in photos]
        return self.filename

    def clear(self):
        os.remove(self.filename)
