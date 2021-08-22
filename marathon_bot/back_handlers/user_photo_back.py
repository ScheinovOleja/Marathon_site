from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from marathon_bot.handlers.user_info_photo_handler import send_menu_user_info_photos, \
    send_menu_user_info_photos_choice, send_menu_user_info_photos_add_get
from marathon_bot.states.all_states_menu import UserInfoMenuPhotos, UserInfoMenu


async def back_user_info_photos(query: CallbackQuery, state: FSMContext):
    await UserInfoMenu.first()
    data = await state.get_data()
    await state.set_data({'marathon_id': data['marathon_id']})
    return await send_menu_user_info_photos(query, state)


async def back_to_user_info_photo_choice(query: CallbackQuery, state: FSMContext):
    await UserInfoMenuPhotos.previous()
    await UserInfoMenuPhotos.previous()
    data = await state.get_data()
    await state.set_data({'marathon_id': data['marathon_id'], 'callback_1': data['callback_1']})
    return await send_menu_user_info_photos_choice(query, state)


async def back_to_user_info_add_get(query: CallbackQuery, state: FSMContext):
    await UserInfoMenuPhotos.last()
    return await send_menu_user_info_photos_add_get(query, state)
