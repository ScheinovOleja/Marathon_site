from aiogram import types
from aiogram.dispatcher import FSMContext
from pony.orm import db_session

from marathon_bot.general_func import send_photo
from marathon_bot.handlers.main_menu_handler import main_menu, back
from marathon_bot.models import TrainingInfo, Marathon, CategoryTrainingMenu
from marathon_bot.states.all_states_menu import TrainingMenu


@db_session
async def send_category_training(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    marathon = await Marathon.get_marathon(marathon_id=data['marathon_id'])
    markup = types.InlineKeyboardMarkup()
    text = 'Выберите категорию меню:'
    if not marathon.category_training_menu:
        text = 'К сожалению, на данный момент еще нет ни одной категории!'
    else:
        for category in marathon.category_training_menu.order_by(CategoryTrainingMenu.id):
            markup.add(types.InlineKeyboardButton(text=f'{category.category}', callback_data=f'Training_{category.id}'))
    if len(markup.inline_keyboard) == 0:
        text = 'К сожалению, на данный момент нет готовых меню! Ждите новостей в моём ' \
               'инстаграме: instagram.com/vkus_viki'
    markup.add(back, main_menu)
    await TrainingMenu.first()
    await query.message.edit_text(text, reply_markup=markup)


@db_session
async def send_training_menus(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    data = await state.get_data()
    try:
        all_menu = TrainingInfo.select().where(category=data['callback'].split('_')[1]).order_by(TrainingInfo.id)[:]
        await state.update_data({"callback": data['callback']})
    except KeyError:
        all_menu = TrainingInfo.select().where(category=query.data.split('_')[1]).order_by(TrainingInfo.id)[:]
        await state.update_data({"callback": query.data})
    for task in all_menu:
        markup.add(types.InlineKeyboardButton(text=f'{task.name}', callback_data=f'Menu_{task.id}'))
    markup.add(back, main_menu)
    await TrainingMenu.next()
    if query.message.content_type == 'photo':
        await query.message.delete()
        await query.message.answer("Выберите нужное меню:", reply_markup=markup)
        return
    else:
        await query.message.edit_text("Выберите нужное меню:", reply_markup=markup)


@db_session
async def send_menu_info(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    menu = TrainingInfo.get(id=query.data.split('_')[1])
    text = f'{menu.name}\n\n' \
           f'{menu.description}\n\n'
    markup.add(back, main_menu)
    if menu.photo:
        await send_photo(query, text, markup, menu.photo)
    else:
        await query.message.edit_text(text, reply_markup=markup)
    await TrainingMenu.last()
