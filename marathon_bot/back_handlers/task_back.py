from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from marathon_bot.handlers.tasks_handler import send_category_tasks, send_tasks
from marathon_bot.states.all_states_menu import TaskMenu


async def back_to_category(query: CallbackQuery, state: FSMContext):
    await TaskMenu.previous()
    data = await state.get_data()
    await state.set_data({'marathon_id': data['marathon_id']})
    return await send_category_tasks(query, state)


async def back_to_list_tasks(query: CallbackQuery, state: FSMContext):
    await TaskMenu.previous()
    await TaskMenu.previous()
    data = await state.get_data()
    await state.set_data({'marathon_id': data['marathon_id'], 'callback': data['callback']})
    return await send_tasks(query, state)



