import asyncio
import configparser
import logging
import os
from pathlib import Path

import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'settings/config.cfg'))
con = psycopg2.connect(**config['database'])

loop = asyncio.get_event_loop()
bot = Bot(token=config['bot']["API_TOKEN"], parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=JSONStorage('settings/user_states.json'), loop=loop)
dp.middleware.setup(LoggingMiddleware())

if not os.path.isdir(f'{os.getcwd()}/logs'):
    os.mkdir(f'{os.getcwd()}/logs')
logging.basicConfig(level=logging.ERROR, filename='logs/log_error.log')
logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, "Marathon_Site/media/")
