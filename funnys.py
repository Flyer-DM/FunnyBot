import requests
from bs4 import BeautifulSoup
from random import choice
from typing import List, Literal, Tuple


class DBFUNNY:
    __version__ = '1.0'

    @staticmethod
    def open_file() -> List[str]:
        with open('anek_djvu.txt', 'r', encoding='utf-8') as file:
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
    __version__ = '1.0'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'}

    @classmethod
    def __parse_jokes(cls, url: str, pages: tuple[int, int], findall_cls: str, url_type: bool = True) -> List[str]:
        jokes: List[str] = []
        for i in range(*pages):
            if url_type:
                page = f'{i}/' if i != 1 else ''
                url = url + page
            else:
                url = f'{url}{i}.html'
            response = requests.get(url, headers=cls.HEADERS)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                allp = map(lambda text: text.findAll('p')[0].get_text(), soup.findAll(class_=findall_cls))
                jokes.extend(allp)
        return jokes

    def __init__(self, url: str, pages: tuple[int, int], findall_cls: str, url_type: bool = True):
        self.__url_type = url_type
        self.__jokes: List[str] = RFUNNY.__parse_jokes(url, pages, findall_cls, url_type)

    def get_joke(self) -> str:
        if not self.__url_type:
            return choice(self.__jokes)
        option = choice(self.__jokes)
        option = option.replace('— ', '\n— ')
        if option.startswith('\n'):
            option = option.replace('\n', '', 1)
        return option


class AZTRO:
    __version__ = '1.0.0'
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
