from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.exceptions import BadRequest, MessageCantBeEdited
from pony.orm import db_session

from marathon_bot import bot
from marathon_bot.models import Users, Marathon
from marathon_bot.states.all_states_menu import MainMenu
from marathon_bot.states.state_scenarios import Register

buttons = [
    InlineKeyboardButton(text='💼 Задания', callback_data='main_menu_tasks'),
    InlineKeyboardButton(text='Фотографии и замеры', callback_data='main_menu_user_info'),
    InlineKeyboardButton(text='Расчет КБЖУ и Меню', callback_data='main_menu_kcal'),
    InlineKeyboardButton(text='🍓 Получить вкусняшки за задание', callback_data='main_menu_get_scopes'),
    InlineKeyboardButton(text='🏆 Статистика по вкусняшкам', callback_data='stats_all'),
    InlineKeyboardButton(text='⚡️ Призы', callback_data='main_menu_buy_product'),
    InlineKeyboardButton(text='🔁 Сменить марафон', callback_data='marathon_switch'),
]
main_menu = InlineKeyboardButton(text='🏠 В главное меню', callback_data='main_menu')
back = InlineKeyboardButton(text='⬅️ Назад', callback_data='back')


async def send_main_menu(query: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup()
    state_data = await state.get_data()
    with db_session:
        marathon = await Marathon.get_marathon(marathon_id=state_data['marathon_id'])
        user = await Users.get_user(tg_id=query.message.chat.id, marathon_id=state_data['marathon_id'])
        await MainMenu.main_menu.set()
        text = f"Привет, {user.first_name}!\n" \
               f"У вас {user.scopes} вкусняшек 🍓"
        if marathon.close:
            try:
                await bot.edit_message_text('Простите, марафон еще закрыт! Нажмите /start',
                                            state_data['msg']['chat']['id'],
                                            state_data['msg']["message_id"], reply_markup=markup)
                await query.message.delete()
            except KeyError:
                await query.message.edit_text('Простите, марафон еще закрыт! Нажмите /start', reply_markup=markup)
            await Register.choice_marathon.set()
            return
    for button in buttons:
        markup.add(button)
    if query.message.content_type == 'photo':
        await query.message.delete()
        await query.message.answer(text, reply_markup=markup)
        return
    try:
        await query.message.edit_text(text, reply_markup=markup)
    except MessageCantBeEdited:
        try:
            await bot.edit_message_text(text, state_data['msg']['chat']['id'], state_data['msg']["message_id"],
                                        reply_markup=markup)
            await query.message.delete()
        except BadRequest:
            await query.message.answer(text, reply_markup=markup)
            await query.message.delete()
    await state.set_data({"marathon_id": state_data['marathon_id']})



