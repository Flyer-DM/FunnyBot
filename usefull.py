from pytube import YouTube
from pytube.exceptions import RegexMatchError
from typing import Optional


class YT:
    __version__ = '1.0'

    def __init__(self):
        self.__max_file_size = 52_428_800
        self.__save_path = 'videos/'

    def download(self, link: str, name: str) -> Optional[str]:
        try:
            video = YouTube(link)
            size = video.streams.get_highest_resolution().filesize
            if size >= self.__max_file_size:
                return f"Слишком большой размер видео ({size // 1024 // 1024}Mb) 😐, телега не пропустит"
            yt = video.streams.filter(file_extension='mp4').get_highest_resolution()
            yt.download(self.__save_path, filename=f'video for {name}.mp4')
        except RegexMatchError:
            return "Видео не найдено 😣"
