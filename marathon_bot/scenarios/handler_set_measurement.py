from aiogram import types
from aiogram.dispatcher import FSMContext
from pony.orm import db_session, commit

from marathon_bot import bot
from marathon_bot.handlers.main_menu_handler import back, main_menu
from marathon_bot.models import Users, Measurement
from marathon_bot.states.all_states_menu import MainMenu
from marathon_bot.states.state_scenarios import MeasurementState


async def treatment_measurement(message: types.Message, state: FSMContext, text, failure_text, measurement):
    state_data = await state.get_data()
    markup = types.InlineKeyboardMarkup()
    try:
        await state.update_data({measurement: float(message.text)})
    except ValueError:
        await message.delete()
        if state_data['msg']['text'] == failure_text:
            pass
        else:
            msg = await bot.edit_message_text(failure_text,
                                              state_data['msg']['chat']['id'],
                                              state_data['msg']["message_id"], reply_markup=markup)
            await state.update_data({'msg': msg.to_python()})
        return False
    if await state.get_state() == MeasurementState.set_weight.state:
        markup.add(main_menu)
        await MainMenu.main_menu.set()
        await successfully(message, state)
    await message.delete()
    await bot.edit_message_text(text, state_data['msg']['chat']["id"],
                                state_data['msg']['message_id'], reply_markup=markup)
    return True


async def send_first_scenario_message_measurement(query: types.CallbackQuery, state: FSMContext):
    text = "Введите обхват груди в см:\n❗️ Например: 84"
    markup = types.InlineKeyboardMarkup().add(back)
    await MeasurementState.first()
    msg = await query.message.edit_text(text, reply_markup=markup)
    await state.update_data({'msg': msg.to_python(), 'measurement': query.data.split("measurement_")[1]})


async def set_breast(message: types.Message, state: FSMContext):
    text = "Введите обхват талии в см:\n❗️ Например: 63"
    failure_text = "Что-то пошло не так. Повторите попытку!\n Введите обхват груди в см:\n❗️ Например: 84"
    data = await state.get_data()
    if await treatment_measurement(message, state, text, failure_text, f"breast_{data['measurement']}"):
        await MeasurementState.next()
    else:
        pass


async def set_waist(message: types.Message, state: FSMContext):
    text = "Введите обхват бедер в см:\n❗️ Например: 96"
    failure_text = "Что-то пошло не так. Повторите попытку!\n Введите обхват талии в см:\n❗️ Например: 63"
    data = await state.get_data()
    if await treatment_measurement(message, state, text, failure_text, f"waist_{data['measurement']}"):
        await MeasurementState.next()
    else:
        pass


async def set_femur(message: types.Message, state: FSMContext):
    text = "Введите ваш вес в кг:\n❗️ Например: 57"
    failure_text = "Что-то пошло не так. Повторите попытку!\n Введите обхват бедер в см:\n❗️ Например: 96"
    data = await state.get_data()
    if await treatment_measurement(message, state, text, failure_text, f"femur_{data['measurement']}"):
        await MeasurementState.next()
    else:
        pass


async def set_weight_measurement(message: types.Message, state: FSMContext):
    text = "Ваши данные успешно введены! Спасибо за предоставленную информацию!"
    failure_text = "Что-то пошло не так. Повторите попытку!\nВведите ваш вес в кг:\n❗️ Например: 57"
    data = await state.get_data()
    if await treatment_measurement(message, state, text, failure_text, f"weight_{data['measurement']}"):
        await MeasurementState.next()
    else:
        pass


@db_session
async def successfully(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = await Users.get_user(tg_id=message.from_user.id, marathon_id=data['marathon_id'])
    if user.measurement is None:
        measurement_db = Measurement()
    else:
        measurement_db = await Measurement.get_measurement(measurement_id=user.measurement.id)
    commit()
    for key in data.keys():
        try:
            setattr(measurement_db, key, data[key])
        except KeyError:
            continue
    await state.set_data({'marathon_id': data['marathon_id']})
    user.measurement = measurement_db.id
