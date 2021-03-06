import asyncio
import sys
from asyncio.log import logger

sys.path.append("/var/www/Marathon_site/")

from aiogram import executor, Dispatcher

from marathon_bot import dp, loop
from marathon_bot.back_handlers import back_task, back_ready_made, back_training_menu, back_photos_user
from marathon_bot.handlers import commons_handler, tasks_handler, user_info_measurement_handler, \
    user_info_photo_handler, kcal_menu_handler, ready_made_handler, training_menu_handler, all_stats_handler, \
    scopes_by_code_handler, product_handler
from marathon_bot.scenarios import calculate_kcal_handler, register_handlers, measurements_handler, photo_handler


async def register_handler_scenarios(dispatcher):
    register_handlers(dispatcher)
    calculate_kcal_handler(dispatcher)
    measurements_handler(dispatcher)
    photo_handler(dispatcher)


async def register_all_handlers(dispatcher):
    commons_handler(dispatcher)
    tasks_handler(dispatcher)
    user_info_measurement_handler(dispatcher)
    user_info_photo_handler(dispatcher)
    kcal_menu_handler(dispatcher)
    ready_made_handler(dispatcher)
    training_menu_handler(dispatcher)
    all_stats_handler(dispatcher)
    scopes_by_code_handler(dispatcher)
    product_handler(dispatcher)


async def register_back_handlers(dispatcher):
    back_task(dispatcher)
    back_ready_made(dispatcher)
    back_training_menu(dispatcher)
    back_photos_user(dispatcher)


async def main(dispatcher: Dispatcher):
    await register_handler_scenarios(dispatcher)
    await register_all_handlers(dispatcher)
    await register_back_handlers(dispatcher)


async def shutdown(dispatcher: Dispatcher):
    logger.error(f"Shutdowning...")
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=loop, on_shutdown=shutdown, on_startup=main)
    # main(dp, loop)
