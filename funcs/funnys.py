import requests
import asyncio
import aiohttp
import pkgutil
from bs4 import BeautifulSoup
from random import choice
from typing import List, Literal, Optional


class DBFUNNY:
    __version__ = '1.0'

    @staticmethod
    def open_file() -> List[str]:
        with open('D:/python_projects/Funny_BOT/funcs/anek_djvu.txt', 'r', encoding='utf-8') as file:
            dbfunny = file.readlines()
        transfer = '\n'
        dbfunny = list(filter(lambda elem: elem != transfer, dbfunny))
        return dbfunny

    def __init__(self):
        self.__dbfunny: List[str] = DBFUNNY.open_file()

    def get_joke(self) -> str:
        option: str = choice(self.__dbfunny)
        option = option.replace('<|startoftext|>', '', 1)
        option = option.replace('- ', '\n- ')
        return option


class RFUNNY:
    __version__ = '2.0'

    async def get_page_data(self, session, page):
        HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'}
        if self.__url_type:
            page = f'{page}/' if page != 1 else ''
            url = self.__url + page
        else:
            url = f'{self.__url}{page}.html'
        async with session.get(url=url, headers=HEADERS) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, "html.parser")
            allp = map(lambda html: html.findAll('p')[0].get_text(), soup.findAll(class_=self.__findall_cls))
            self.jokes.extend(allp)

    async def parse_pages(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for page in range(*self.__pages):
                task = asyncio.create_task(self.get_page_data(session, page))
                tasks.append(task)
            await asyncio.gather(*tasks)

    def __init__(self, url: str, pages: tuple[int, int], findall_cls: str, url_type: bool = True):
        self.__url = url
        self.__pages = pages
        self.__findall_cls = findall_cls
        self.__url_type = url_type
        self.jokes = []
        asyncio.run(self.parse_pages())

    def get_joke(self) -> str:
        if not self.__url_type:
            return choice(self.jokes)
        option = choice(self.jokes)
        option = option.replace('— ', '\n— ')
        if option.startswith('\n'):
            option = option.replace('\n', '', 1)
        return option


class AZTRO:
    __version__ = '1.0'
    SIGNS = Literal['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓']
    TRANSLATE_SIGNS = {'♈': 'aries', '♉': 'taurus', '♊': 'gemini', '♋': 'cancer', '♌': 'leo', '♍': 'virgo',
                       '♎': 'libra', '♏': 'scorpio', '♐': 'sagittarius', '♑': 'capricorn', '♒': 'aquarius',
                       '♓': 'pisces'}

    def __init__(self):
        self.url = 'https://horoscopes.rambler.ru/'

    def get_answer(self, sign: SIGNS) -> tuple[str, str] | None:
        response = requests.get(self.url + AZTRO.TRANSLATE_SIGNS[sign] + '/')
        if response.status_code == 200:
            text = response.text
            sign = BeautifulSoup(text, "html.parser").find('h1').text
            text = BeautifulSoup(text, "html.parser").find('p').text
            return sign, text
        return


class MORNING:
    __version__ = '1.0'

    def __init__(self):
        self.first_url = 'https://api.thecatapi.com/v1/images/search'
        self.second_url = 'https://forumsmile.net/cards/goodmorning/'

    def get_image(self) -> Optional[str]:
        response = requests.get(self.first_url)
        if response.status_code == 200:
            return response.json()[0]['url']
        return

    def get_caption(self) -> Optional[str]:
        response = requests.get(self.second_url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser").find(class_='tag_message_top').p.text
        return
