from aiogram import types
from aiogram.dispatcher import FSMContext
from pony.orm import db_session

from marathon_bot.handlers.main_menu_handler import main_menu, back
from marathon_bot.models import KcalCategoryReadyMadeMenu, DayReadyMadeMenu, TimeDayReadyMadeMenu, ReadyMadeMenu
from marathon_bot.states.all_states_menu import ReadyMadeMenuState


@db_session
async def send_category_ready_made_menu(query: types.CallbackQuery):
    categories_kcal = KcalCategoryReadyMadeMenu.select()[:]
    markup = types.InlineKeyboardMarkup()
    text = 'Выберите количество калорий:'
    if not categories_kcal:
        text = 'К сожалению, на данный момент еще нет ни одной категории!'
    else:
        for category in categories_kcal:
            markup.add(types.InlineKeyboardButton(text=f'{category.kcal_category}',
                                                  callback_data=f'Kcal_{category.id}'))
    markup.add(back, main_menu)
    await ReadyMadeMenuState.first()
    await query.message.edit_text(text, reply_markup=markup)


@db_session
async def send_all_day(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    data = await state.get_data()
    try:
        category_kcal = KcalCategoryReadyMadeMenu.get(id=data['callback'].split('_')[1])
        await state.update_data({'callback': data['callback']})
    except KeyError:
        category_kcal = KcalCategoryReadyMadeMenu.get(id=query.data.split('_')[1])
        await state.update_data({'callback': query.data})
    all_day = DayReadyMadeMenu.select().where(kcal_category=category_kcal.id)[:]
    for day in all_day:
        markup.add(types.InlineKeyboardButton(text=f'{day.day}', callback_data=f'Day_{day.id}'))
    markup.add(back, main_menu)
    await ReadyMadeMenuState.next()
    await query.message.edit_text('Выберите день недели:', reply_markup=markup)


@db_session
async def send_time_day(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    data = await state.get_data()
    try:
        all_times = TimeDayReadyMadeMenu.select().where(day=data['callback'].split('_')[1])
        await state.update_data({'callback': data['callback']})
    except KeyError:
        all_times = TimeDayReadyMadeMenu.select().where(day=query.data.split('_')[1])
        await state.update_data({'callback': query.data})
    for time in all_times:
        markup.add(types.InlineKeyboardButton(text=f'{time.time_day}', callback_data=f'Time_{time.id}'))
    markup.add(back, main_menu)
    await ReadyMadeMenuState.next()
    await query.message.edit_text('Выберите время дня:', reply_markup=markup)


@db_session
async def send_ready_made_menu_list(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    data = await state.get_data()
    try:
        ready_made_menu_list = ReadyMadeMenu.select(time_day=data['callback'].split("_")[1])
        await state.update_data({'callback': data['callback']})
    except KeyError:
        ready_made_menu_list = ReadyMadeMenu.select(time_day=query.data.split("_")[1])
        await state.update_data({'callback': query.data})
    for menu in ready_made_menu_list:
        markup.add(types.InlineKeyboardButton(text=f'{menu.name_menu}', callback_data=f'Menu_{menu.id}'))
    markup.add(back, main_menu)
    await ReadyMadeMenuState.next()
    await query.message.edit_text("Выберите рецепт:", reply_markup=markup)


@db_session
async def send_info_by_ready_made_menu(query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    ready_made = ReadyMadeMenu.get(id=query.data.split("_")[1])
    text = f"{ready_made.name_menu}\n\n" \
           f"{ready_made.description}\n\n"
    markup.add(back, main_menu)
    if ready_made.photo:
        try:
            await query.message.answer_photo(photo=open(f'{ready_made.photo.file.name}', 'rb'), caption=text,
                                             reply_markup=markup)
            await query.message.delete()
            return
        except Exception as exc:
            await query.message.edit_text(text, reply_markup=markup)
            return
    await ReadyMadeMenuState.last()
    await query.message.edit_text(text, reply_markup=markup)
