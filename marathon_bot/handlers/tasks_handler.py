import datetime
import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BadRequest
from pony.orm import db_session

from marathon_bot.general_func import send_photo
from marathon_bot.handlers.main_menu_handler import main_menu, back
from marathon_bot.models import Users, Tasks, Marathon, CategoryTasks
from marathon_bot.states.all_states_menu import TaskMenu


@db_session
async def send_category_tasks(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    marathon = await Marathon.get_marathon(marathon_id=data['marathon_id'])
    markup = types.InlineKeyboardMarkup()
    text = 'Выберите категорию:'
    if not marathon.category_task:
        text = 'К сожалению, на данный момент нет заданий на выполнение! Ждите новостей по новым заданиям в моём ' \
               'инстаграме: instagram.com/vkus_viki'
    else:
        for category in marathon.category_task.order_by(CategoryTasks.id):
            if category.date_start < datetime.datetime.now(category.date_start.tzinfo) < category.date_stop:
                markup.add(types.InlineKeyboardButton(text=f'{category.category}', callback_data=f'Category_{category.id}'))
    if len(markup.inline_keyboard) == 0:
        text = 'К сожалению, на данный момент нет категорий! Ждите новостей в моём ' \
               'инстаграме: instagram.com/vkus_viki'
    markup.add(main_menu)
    await TaskMenu.first()
    await query.message.edit_text(text, reply_markup=markup)


@db_session
async def send_tasks(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    data = await state.get_data()
    text = 'Выберите задание:'
    completed_task = await Users.get_user(tg_id=query.from_user.id, marathon_id=data['marathon_id'])
    try:
        all_task = Tasks.select().where(category=data['callback'].split('_')[1]).order_by(Tasks.id)[:]
        await state.update_data({'callback': data['callback']})
    except KeyError:
        all_task = Tasks.select().where(category=query.data.split('_')[1]).order_by(Tasks.id)[:]
        await state.update_data({'callback': query.data})
    for task in all_task:
        if any([task.id == complete.id for complete in completed_task.completed_tasks]):
            continue
        else:
            if task.date_start < datetime.datetime.now(task.date_start.tzinfo) < task.date_stop:
                markup.add(types.InlineKeyboardButton(text=f'{task.name}', callback_data=f'Task_{task.id}'))
    if len(markup.inline_keyboard) == 0:
        text = 'К сожалению, на данный момент нет заданий на выполнение! Ждите новостей по новым заданиям в моём ' \
               'инстаграме: instagram.com/vkus_viki'
    markup.add(back, main_menu)
    await TaskMenu.next()
    try:
        await query.message.edit_text(text, reply_markup=markup)
    except BadRequest:
        await query.message.delete()
        await query.message.answer(text, reply_markup=markup)


@db_session
async def send_task_info(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    task = Tasks.get(id=query.data.split('_')[1])
    time_task = task.date_stop.astimezone(pytz.timezone('Europe/Moscow'))
    text = f'{task.name}\n\n' \
           f'{task.description}\n\n' \
           f'Дата закрытия задания: {time_task.strftime("%H:%M:%S %d.%m.%Y")}'
    markup.add(back, main_menu)
    if task.image:
        await send_photo(query, text, markup, task.image)
    else:
        await query.message.edit_text(text, reply_markup=markup)
    await TaskMenu.next()
