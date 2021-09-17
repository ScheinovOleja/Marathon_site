from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from pony.orm import db_session

from marathon_bot import bot
from marathon_bot.handlers.main_menu_handler import main_menu
from marathon_bot.models import Codes, Users, Tasks
from marathon_bot.states.all_states_menu import GetScopes


async def send_codes_message(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup().add(main_menu)
    text = "Пожалуйста введите код, чтобы получить вкусняшки 🍓\nВводите его в точности как он был выдан:"
    await GetScopes.first()
    msg = await query.message.edit_text(text, reply_markup=markup)
    await state.update_data({'msg': msg.to_python()})


async def get_code(message: types.Message, state: FSMContext):
    markup = types.InlineKeyboardMarkup().add(main_menu)
    state_data = await state.get_data()
    with db_session:
        code = Codes.select().where(code=message.text.lower(), marathon=state_data['marathon_id'])[:]
        if code:
            user = await Users.get_user(tg_id=message.from_user.id, marathon_id=state_data['marathon_id'])
            if any([code[0].id == entered.id for entered in user.entered_codes]):
                text = "Вы уже вводили этот код! Вкусняшек вы не получите!"
            else:
                user.scopes += code[0].scopes
                text = f'Спасибо!\nВы получили {code[0].scopes} вкусняшек!\nЕсли есть еще что-то, вводите, не ' \
                       f'стесняйтесь)'
                code[0].user.add(user)
        else:
            code_task = Tasks.get(unique_code=message.text.lower())
            if code_task is not None:
                user = await Users.get_user(tg_id=message.from_user.id, marathon_id=state_data['marathon_id'])
                if any([code_task.id == completed.id for completed in user.completed_tasks]):
                    text = 'Вы уже выполнили это задание! Вкусняшек вы не получите!'
                else:
                    user.scopes += code_task.count_scopes
                    text = f'Спасибо!\nВы получили {code_task.count_scopes} вкусняшек!\nЕсли есть еще что-то, ' \
                           f'вводите, не стесняйтесь!'
                    user.completed_tasks.add(code_task)
            else:
                text = "Такого кода не найдено!\nПроверьте правильность написания и повторите попытку!"
    try:
        msg = await bot.edit_message_text(text, state_data['msg']['chat']['id'], state_data['msg']["message_id"],
                                          reply_markup=markup)
        await state.update_data({'msg': msg.to_python()})
        await message.delete()
    except MessageNotModified:
        await message.delete()
