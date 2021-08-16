from aiogram import types
from aiogram.dispatcher import FSMContext
from pony.orm import db_session

from marathon_bot.handlers.main_menu_handler import main_menu, back
from marathon_bot.models import CategoryTrainingMenu, TrainingInfo
from marathon_bot.states.all_states_menu import TrainingMenu


@db_session
async def send_category_training(query: types.CallbackQuery):
    categories = CategoryTrainingMenu.select()[:]
    markup = types.InlineKeyboardMarkup()
    text = 'Выберите категорию меню:'
    if not categories:
        text = 'К сожалению, на данный момент еще нет ни одной категории!'
    else:
        for category in categories:
            markup.add(types.InlineKeyboardButton(text=f'{category.category}', callback_data=f'Training_{category.id}'))
    markup.add(back, main_menu)
    await TrainingMenu.first()
    await query.message.edit_text(text, reply_markup=markup)


@db_session
async def send_training_menus(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    data = await state.get_data()
    try:
        all_menu = TrainingInfo.select().where(category=data['callback'].split('_')[1])[:]
        await state.update_data({"callback": data['callback']})
    except KeyError:
        all_menu = TrainingInfo.select().where(category=query.data.split('_')[1])[:]
        await state.update_data({"callback": query.data})
    for task in all_menu:
        markup.add(types.InlineKeyboardButton(text=f'{task.name}', callback_data=f'Menu_{task.id}'))
    markup.add(back, main_menu)
    await TrainingMenu.next()
    await query.message.edit_text('Выберите нужное меню:', reply_markup=markup)


@db_session
async def send_menu_info(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    menu = TrainingInfo.get(id=query.data.split('_')[1])
    text = f'{menu.name}\n\n' \
           f'{menu.description}\n\n'
    markup.add(back, main_menu)
    await TrainingMenu.last()
    if menu.photo:
        try:
            await query.message.answer_photo(photo=open(f'{menu.photo}', 'rb'), caption=text,
                                             reply_markup=markup)
            await query.message.delete()
            return
        except Exception as exc:
            await query.message.edit_text(text, reply_markup=markup)
            return
    await query.message.edit_text(text, reply_markup=markup)
