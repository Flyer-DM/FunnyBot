import logging
from utilities.funnys import *
from utilities.log_setup import CustomFormatter
from aiogram import Bot, Dispatcher

TOKEN_PATH = 'D:/python_projects/Funny_BOT/setup/token.txt'

CHAT_GROUP = 'group'
CHAT_PRIVATE = 'private'
CHAT_SUPERGROUP = 'supergroup'

PHOTO_EXT = ('png', 'jpg', 'jpeg')

KRINGE = "Kringe"
BLACK = "Black"
HOROSYMBS = '♈♉♊♋♌♍♎♏♐♑♒♓'

fmt = '%(asctime)s | %(levelname)8s | %(message)s'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(CustomFormatter(fmt))
logger.addHandler(stdout_handler)
logger.info('START OF BOT')

dbfunny = DBFUNNY()
logger.info('START OF WEB PARSING')
morning = MORNING()
rfunny1 = RFUNNY('https://anekdoty.ru/cherniy-yumor/', (1, 6), 'holder-body')
rfunny2 = RFUNNY('https://anekdotov.net/anekdot/black/index-page-', (0, 37), 'anekdot', False)
rfunny3 = RFUNNY('https://anekdotovstreet.com/chernyy-yumor/', (1, 16), 'anekdot-text')
aztro = AZTRO()
logger.info('END OF WEB PARSING')

# ********* READING MY BOT TOKEN **********#
with open(TOKEN_PATH, 'r') as token_file:  #
    token = token_file.read()              #
# *****************************************#

bot = Bot(token=token)
dp = Dispatcher()
