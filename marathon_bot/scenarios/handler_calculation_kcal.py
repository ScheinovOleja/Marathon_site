from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from pony.orm import db_session, commit

from marathon_bot import bot
from marathon_bot.handlers.main_menu_handler import main_menu, back
from marathon_bot.models import Users, BZUUsers
from marathon_bot.states.state_scenarios import CalculateKcal

data_activity = CallbackData('post', 'id', 'action')

buttons_activity = [
    types.InlineKeyboardButton(text='Сидячий образ жизни',
                               callback_data=data_activity.new(id='activity', action=1.2)),
    types.InlineKeyboardButton(text='Легкие тренировки, 1-2 раза в неделю',
                               callback_data=data_activity.new(id='activity', action=1.375)),
    types.InlineKeyboardButton(text='Умеренная активность, 3-5 раз в неделю',
                               callback_data=data_activity.new(id='activity', action=1.55)),
    types.InlineKeyboardButton(text='Повышенная активность, 6-7 раз в неделю',
                               callback_data=data_activity.new(id='activity', action=1.725)),
    types.InlineKeyboardButton(text='Сверх интенсивная работа, профессиональный спорт',
                               callback_data=data_activity.new(id='activity', action=1.9))
]


async def treatment_calculate_kcal(message: types.Message, state: FSMContext, text, failure_text, dict_key,
                                   markup=None):
    state_data = await state.get_data()
    try:
        await state.update_data({dict_key: float(message.text)})
    except ValueError:
        await message.delete()
        if state_data['msg']['text'] == failure_text:
            return False
        else:
            msg = await bot.edit_message_text(failure_text,
                                              state_data['msg']['chat']['id'],
                                              state_data['msg']["message_id"])
            await state.update_data({'msg': msg.to_python()})
            return False
    await message.delete()
    msg = await bot.edit_message_text(text, state_data['msg']['chat']["id"],
                                      state_data['msg']['message_id'], reply_markup=markup)
    await state.update_data({'msg': msg.to_python()})
    return True


async def send_first_scenario_message_calculate_kcal(query: types.CallbackQuery, state: FSMContext):
    text = "Введите ваш вес на данный момент (в кг):\n❗️Например: 57"
    markup = types.InlineKeyboardMarkup(row_width=2).add(back)
    await CalculateKcal.first()
    msg = await query.message.edit_text(text, reply_markup=markup)
    await state.update_data({'msg': msg.to_python()})


async def set_weight_kcal(message: types.Message, state: FSMContext):
    text = "Введите ваш рост в данный момент (в см):\n❗️Например: 164"
    failure_text = "Что-то пошло не так. Повторите попытку!\n Введите ваш вес на данный момент(в кг):\n❗️Например: 57"
    if await treatment_calculate_kcal(message, state, text, failure_text, "weight"):
        await CalculateKcal.next()
    else:
        pass


async def set_height(message: types.Message, state: FSMContext):
    text = "Введите ваш возраст (в годах):\n❗️Например: 23"
    failure_text = "Что-то пошло не так. Повторите попытку!\n Введите ваш рост в данный момент (в см):\n❗️Например: 164"
    if await treatment_calculate_kcal(message, state, text, failure_text, "height"):
        await CalculateKcal.next()
    else:
        pass


async def set_age(message: types.Message, state: FSMContext):
    text = "Выберите ваш пол:"
    failure_text = "Что-то пошло не так. Повторите попытку!\n Введите ваш возраст (в годах):\n❗️Например: 23"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Мужчина', callback_data='man'))
    markup.add(types.InlineKeyboardButton(text='Женщина', callback_data='woman'))
    if await treatment_calculate_kcal(message, state, text, failure_text, "age", markup):
        await CalculateKcal.next()
    else:
        pass


async def set_sex(query: types.CallbackQuery, state: FSMContext):
    text = "Выберите вашу цель:"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Похудение', callback_data='-'))
    markup.add(types.InlineKeyboardButton(text='Поддержание веса', callback_data='='))
    markup.add(types.InlineKeyboardButton(text='Набор массы', callback_data='+'))
    await state.update_data({'sex': query.data})
    await CalculateKcal.next()
    await query.message.edit_text(text, reply_markup=markup)


async def set_purpose(query: types.CallbackQuery, state: FSMContext):
    text = "Выберите ваш уровень активности:"
    markup = types.InlineKeyboardMarkup()
    for button in buttons_activity:
        markup.add(button)
    await state.update_data({'purpose': query.data})
    await CalculateKcal.next()
    await query.message.edit_text(text, reply_markup=markup)


async def calculate_kcal(sex, weight, height, age, activity, purpose):
    if sex == 'man':
        kcal = ((65.5 + 13.75 * weight + 5 * height - 6.78 * age) * activity)
    elif sex == 'woman':
        kcal = ((655 + 9.56 * weight + 1.85 * height - 4.68 * age) * activity)
    else:
        kcal = 0
    if purpose == '-':
        return kcal - 571
    elif purpose == '+':
        return kcal + 571
    else:
        return kcal


async def successfully(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    markup = types.InlineKeyboardMarkup()
    activity = float(query.data.split('activity:')[1])
    with db_session:
        user = await Users.get_user(tg_id=query.from_user.id, marathon_id=state_data['marathon_id'])
        kcal = round(
            await calculate_kcal(state_data['sex'], state_data['weight'], state_data['height'], state_data['age'],
                                 activity, state_data['purpose']))
        text = f'<pre>' \
               f'Необходимое для вас количество ККАЛ - {kcal}\n' \
               f'</pre>\n'
        if user.marathon.price > 0.0:
            if user.bzu is None:
                bzu = BZUUsers(
                    proteins=round(kcal * 0.0625),
                    fats=round(kcal * 0.03333),
                    carbohydrates=round(kcal * 0.1125)
                )
                commit()
                user.bzu = bzu
            else:
                user.bzu.proteins = int(round(kcal * 0.0625))
                user.bzu.fats = int(round(kcal * 0.03333))
                user.bzu.carbohydrates = int(round(kcal * 0.1125))
            commit()
            text += f'<pre>' \
                    f'Белки - {user.bzu.proteins} гр\n' \
                    f'Жиры - {user.bzu.fats} гр\n' \
                    f'Углеводы - {user.bzu.carbohydrates} гр\n' \
                    f'</pre>'
        user.age = int(state_data['age'])
        user.height = int(state_data['height'])
        user.weight = int(state_data['weight'])
        user.sex = state_data['sex'][0]
        user.purpose = state_data['purpose']
        user.kcal = kcal
    markup.add(main_menu)
    await query.message.edit_text(text, reply_markup=markup)
