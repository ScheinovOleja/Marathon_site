from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from pony.orm import db_session

from marathon_bot.general_func import btn
from marathon_bot.handlers.main_menu_handler import main_menu
from marathon_bot.models import Users, Marathon
from marathon_bot.states.all_states_menu import CalculationOfKBZUMenu

data_kcal_welcome_menu = CallbackData('kcal', 'id')

buttons_kcal_welcome_menu = [
    InlineKeyboardButton(text=f'{btn("kcal")}',
                         callback_data=data_kcal_welcome_menu.new(id='kcal')),
    InlineKeyboardButton(text=f'{btn("ready_made_menu")}',
                         callback_data=data_kcal_welcome_menu.new(id='ready_made_menu')),
]
paid_button = InlineKeyboardButton(text=f'{btn("training")}',
                                   callback_data='training')


async def send_menu_kcal_welcome(query: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(row_width=2)
    for button in buttons_kcal_welcome_menu:
        markup.add(button)
    state_data = await state.get_data()
    with db_session:
        user = await Users.get_user(tg_id=query.from_user.id, marathon_id=state_data['marathon_id'])
        marathon = await Marathon.get_marathon(marathon_id=state_data['marathon_id'])
        text = f'Привет, {user.first_name}!\n' \
               f'Ваши текущие расчеты:\n\n'
        if user.sex:
            if user.purpose == "-":
                purpose = "Похудение"
            elif user.purpose == "+":
                purpose = "Набор массы"
            else:
                purpose = "Поддержание веса"
            text += f'<pre>' \
                    f'Ваш вес - {user.weight} кг\n' \
                    f'Ваш рост -  {user.height} см\n' \
                    f'Ваш возраст - {user.age}\n' \
                    f'Ваша текущая цель - {purpose}\n' \
                    f'Необходимое для вас количество ККАЛ - {user.kcal}\n\n' \
                    f'</pre>'
        if marathon.price > 0.0:
            if user.bzu is not None:
                text += f'<pre>' \
                        f'Белки - {int(user.bzu.proteins)} гр\n' \
                        f'Жиры - {int(user.bzu.fats)} гр\n' \
                        f'Углеводы - {int(user.bzu.carbohydrates)} гр\n' \
                        f'</pre>'
            markup.add(paid_button)
    markup.add(main_menu)
    await CalculationOfKBZUMenu.choice_menu.set()
    await query.message.edit_text(text, reply_markup=markup)
