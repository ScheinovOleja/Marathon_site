from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from pony.orm import db_session

from marathon_bot.general_func import btn
from marathon_bot.handlers.main_menu_handler import main_menu, back
from marathon_bot.models import Users, Marathon
from marathon_bot.states.all_states_menu import UserInfoMenu, UserInfoMenuMeasurement

buttons_menu = [
    types.InlineKeyboardButton(text=f'{btn("user_info_measurement_choice")}',
                               callback_data='user_info_measurement_choice'),
    types.InlineKeyboardButton(text=f'{btn("user_info_photos_choice")}', callback_data='user_info_photos_choice'),
]

data_measurement = CallbackData('measurement', 'id', 'action')

buttons_measurement = {
    'after': types.InlineKeyboardButton(text=f'{btn("measurement_after")}',
                                        callback_data=data_measurement.new(id="-", action='measurement_after')),
    'before': types.InlineKeyboardButton(text=f'{btn("measurement_before")}',
                                         callback_data=data_measurement.new(id="-", action='measurement_before')),
}


async def send_menu_user_info(query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    for button in buttons_menu:
        markup.add(button)
    markup.add(main_menu)
    await query.message.edit_text('Выберите пункт меню:', reply_markup=markup)
    await UserInfoMenu.first()


async def back_to_menu_user_info(query: types.CallbackQuery):
    await UserInfoMenu.first()
    return await send_menu_user_info(query)


@db_session
async def send_menu_user_info_measurement(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup(row_width=2)
    state_data = await state.get_data()
    user = await Users.get_user(tg_id=query.from_user.id, marathon_id=state_data['marathon_id'])
    measurement = user.measurement
    if not measurement:
        text = "Вы не предоставляли информацию о своих замерах!"
    else:
        text = f'<pre>ДО:      ----->   ПОСЛЕ:</pre>\n' \
               f'<pre>Грудь:{measurement.breast_after if measurement.breast_after else ""}----->' \
               f'Грудь: {measurement.breast_before if measurement.breast_before else ""},</pre>\n' \
               f'<pre>Талия: {measurement.waist_after if measurement.waist_after else ""}----->' \
               f'Талия: {measurement.waist_before if measurement.waist_before else ""},</pre>\n' \
               f'<pre>Бедра: {measurement.femur_after if measurement.femur_after else ""}----->' \
               f'Бедра: {measurement.femur_before if measurement.femur_before else ""},</pre>\n' \
               f'<pre>Вес: {measurement.weight_after if measurement.weight_after else ""}----->' \
               f'Вес: {measurement.weight_before if measurement.weight_before else ""}</pre>'
    if Marathon.get(id=user.marathon.id).send_measurements_after:
        markup.add(buttons_measurement['after'])
    if Marathon.get(id=user.marathon.id).send_measurements_before:
        markup.add(buttons_measurement['before'])
    markup.add(back, main_menu)
    await query.message.edit_text(text, 'html', reply_markup=markup)
    await UserInfoMenuMeasurement.first()


async def back_to_menu_user_info_measurement(query: types.CallbackQuery, state: FSMContext):
    await UserInfoMenu.first()
    return await send_menu_user_info_measurement(query, state)
