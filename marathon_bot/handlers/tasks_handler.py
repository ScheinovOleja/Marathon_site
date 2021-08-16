from aiogram import types
from aiogram.dispatcher import FSMContext
from pony.orm import db_session

from marathon_bot.handlers.main_menu_handler import main_menu, back
from marathon_bot.models import CategoryTasks, Users, Tasks
from marathon_bot.states.all_states_menu import TaskMenu


@db_session
async def send_category_tasks(query: types.CallbackQuery):
    categories = CategoryTasks.select()[:]
    markup = types.InlineKeyboardMarkup()
    text = 'Выберите категорию:'
    if not categories:
        text = 'К сожалению, на данный момент еще нет ни одной категории!'
    else:
        for category in categories:
            markup.add(types.InlineKeyboardButton(text=f'{category.category}', callback_data=f'Category_{category.id}'))
    markup.add(main_menu)
    await TaskMenu.first()
    await query.message.edit_text(text, reply_markup=markup)


@db_session
async def send_tasks(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    data = await state.get_data()
    completed_task = await Users.get_user(tg_id=query.from_user.id, marathon_id=data['marathon_id'])
    try:
        all_task = Tasks.select().where(category=data['callback'].split('_')[1])[:]
        await state.update_data({'callback': data['callback']})
    except KeyError:
        all_task = Tasks.select().where(category=query.data.split('_')[1])[:]
        await state.update_data({'callback': query.data})
    for task in all_task:
        if any([task.id == complete.id for complete in completed_task.completed_tasks]):
            continue
        else:
            markup.add(types.InlineKeyboardButton(text=f'{task.name}', callback_data=f'Task_{task.id}'))
    markup.add(back, main_menu)
    await TaskMenu.next()
    await query.message.edit_text('Выберите задание:', reply_markup=markup)


@db_session
async def send_task_info(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    task = Tasks.get(id=query.data.split('_')[1])
    text = f'{task.name}\n\n' \
           f'{task.description}\n\n'
    markup.add(back, main_menu)
    if task.image:
        try:
            await query.message.answer_photo(photo=open(f'{task.image.file.name}', 'rb'), caption=text,
                                             reply_markup=markup)
            await query.message.delete()
            return
        except Exception as exc:
            await query.message.edit_text(text, reply_markup=markup)
            return
    await TaskMenu.next()
    await query.message.edit_text(text, reply_markup=markup)
