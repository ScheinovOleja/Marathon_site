from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from pony.orm import desc, db_session

from marathon_bot.handlers.main_menu_handler import main_menu
from marathon_bot.models import Users


@db_session
async def send_stats(query: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup().add(main_menu)
    state_data = await state.get_data()
    top_user = Users.select().where(marathon=state_data['marathon_id']).order_by(desc(Users.scopes))[:10]
    text = "ТОП-10 участников марафона:\n\n"
    for i, user in enumerate(top_user):
        if i == 0:
            text += f'🥇 <b>{user.first_name} {user.last_name}</b> - {user.scopes} вкусняшек 🍓\n\n'
        elif i == 1:
            text += f'🥈 <b>{user.first_name} {user.last_name}</b> - {user.scopes} вкусняшек 🍓\n\n'
        elif i == 2:
            text += f'🥉 <b>{user.first_name} {user.last_name}</b> - {user.scopes} вкусняшек 🍓\n\n'
        else:
            text += f"<b>{user.first_name} {user.last_name}</b> - {user.scopes} вкусняшек 🍓\n\n"
    await query.message.edit_text(text, reply_markup=markup)
