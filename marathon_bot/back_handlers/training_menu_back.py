from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from marathon_bot.handlers import send_training_menus, send_category_training
from marathon_bot.states.all_states_menu import TrainingMenu


async def back_to_category_training(query: CallbackQuery, state: FSMContext):
    await TrainingMenu.previous()
    data = await state.get_data()
    await state.set_data({'marathon_id': data['marathon_id']})
    return await send_category_training(query, state)


async def back_to_list_menus(query: CallbackQuery, state: FSMContext):
    await TrainingMenu.previous()
    await TrainingMenu.previous()
    data = await state.get_data()
    await state.update_data({'callback': data['callback']})
    return await send_training_menus(query, state)
