from aiogram import types
from aiogram.dispatcher import FSMContext

from marathon_bot.handlers import send_menu_kcal_welcome
from marathon_bot.handlers.ready_made_menu_handler import send_category_ready_made_menu, send_all_day, send_time_day, \
    send_ready_made_menu_list
from marathon_bot.states.all_states_menu import ReadyMadeMenuState, MainMenu


async def back_to_kcal_welcome(query: types.CallbackQuery, state: FSMContext):
    await MainMenu.main_menu.set()
    return await send_menu_kcal_welcome(query, state)


async def back_to_send_category(query: types.CallbackQuery, state: FSMContext):
    await ReadyMadeMenuState.previous()
    return await send_category_ready_made_menu(query, state)


async def back_to_all_day(query: types.CallbackQuery, state: FSMContext):
    await ReadyMadeMenuState.previous()
    await ReadyMadeMenuState.previous()
    return await send_all_day(query, state)


async def back_to_time_day(query: types.CallbackQuery, state: FSMContext):
    await ReadyMadeMenuState.previous()
    await ReadyMadeMenuState.previous()
    return await send_time_day(query, state)


async def back_to_menu_list(query: types.CallbackQuery, state: FSMContext):
    await ReadyMadeMenuState.previous()
    await ReadyMadeMenuState.previous()
    return await send_ready_made_menu_list(query, state)
