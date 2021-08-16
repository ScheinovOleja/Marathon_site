from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from marathon_bot.handlers.tasks_handler import send_category_tasks, send_tasks
from marathon_bot.states.all_states_menu import TaskMenu


async def back_to_category(query: CallbackQuery):
    await TaskMenu.previous()
    return await send_category_tasks(query)


async def back_to_list_tasks(query: CallbackQuery, state: FSMContext):
    await TaskMenu.previous()
    await TaskMenu.previous()
    return await send_tasks(query, state)



