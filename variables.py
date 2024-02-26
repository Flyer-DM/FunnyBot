import logging
from funnys import *
from aiogram import Bot, Dispatcher


KRINGE = "Kringe"
BLACK = "Black"
HOROSYMBS = '♈♉♊♋♌♍♎♏♐♑♒♓'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger('FunnyBot')
logger.setLevel(logging.INFO)
logger.info('START')

dbfunny = DBFUNNY()
rfunny1 = RFUNNY('https://anekdoty.ru/cherniy-yumor/', (1, 6), 'holder-body')
rfunny2 = RFUNNY('https://anekdotov.net/anekdot/black/index-page-', (0, 37), 'anekdot', False)
rfunny3 = RFUNNY('https://anekdotovstreet.com/chernyy-yumor/', (1, 16), 'anekdot-text')
aztro = AZTRO()
logger.info('END OF WEB PARSING')

# ********* READING MY BOT TOKEN ***********#
with open('token.txt', 'r') as token_file:  #
    token = token_file.read()               #
# ******************************************#

bot = Bot(token=token)
dp = Dispatcher()
