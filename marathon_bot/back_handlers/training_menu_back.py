from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from marathon_bot.handlers.tasks_handler import send_category_tasks, send_tasks
from marathon_bot.states.all_states_menu import TrainingMenu


async def back_to_category_training(query: CallbackQuery):
    await TrainingMenu.previous()
    return await send_category_tasks(query)


async def back_to_list_menus(query: CallbackQuery, state: FSMContext):
    await TrainingMenu.previous()
    await TrainingMenu.previous()
    return await send_tasks(query, state)



