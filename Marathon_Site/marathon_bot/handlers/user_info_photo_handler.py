from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest
from pony.orm import db_session

from marathon_bot import MEDIA_ROOT
from marathon_bot.general_func import btn
from marathon_bot.handlers.main_menu_handler import back, main_menu
from marathon_bot.models import Users, PhotoStates
from marathon_bot.states.all_states_menu import UserInfoMenuPhotos
from marathon_bot.states.state_scenarios import Photos

data_photos_choice = CallbackData('choice', 'id', 'action')

states = {"front_after": 'photo_front_after',
          "sideways_after": 'photo_sideways_after',
          "back_after": 'photo_back_after',
          "front_before": 'photo_front_before',
          "sideways_before": 'photo_sideways_before',
          "back_before": 'photo_back_before'}

buttons_photos_choice_after = [
    types.InlineKeyboardButton(text=f'{btn("front_after")}',
                               callback_data=data_photos_choice.new(action='front_after', id='choice')),
    types.InlineKeyboardButton(text=f'{btn("sideways_after")}',
                               callback_data=data_photos_choice.new(action='sideways_after', id='choice')),
    types.InlineKeyboardButton(text=f'{btn("back_after")}',
                               callback_data=data_photos_choice.new(action='back_after', id='choice'))
]

buttons_photos_choice_before = [
    types.InlineKeyboardButton(text=f'{btn("front_before")}',
                               callback_data=data_photos_choice.new(action='front_before', id='choice')),
    types.InlineKeyboardButton(text=f'{btn("sideways_before")}',
                               callback_data=data_photos_choice.new(action='sideways_before', id='choice')),
    types.InlineKeyboardButton(text=f'{btn("back_before")}',
                               callback_data=data_photos_choice.new(action='back_before', id='choice'))
]

data_photos_get_add = CallbackData('post', 'id', 'action')

buttons_photos_add_after = {
    'photo_front_after': types.InlineKeyboardButton(text=f'{btn("add_front_after")}',
                                                    callback_data=data_photos_get_add.new(
                                                        action='add_front_after', id='add')),
    'photo_sideways_after': types.InlineKeyboardButton(text=f'{btn("add_sideways_after")}',
                                                       callback_data=data_photos_get_add.new(
                                                           action='add_sideways_after', id='add')),
    'photo_back_after': types.InlineKeyboardButton(text=f'{btn("add_back_after")}',
                                                   callback_data=data_photos_get_add.new(action='add_back_after',
                                                                                         id='add'))
}

buttons_photos_add_before = {
    'photo_front_before': types.InlineKeyboardButton(text=f'{btn("add_front_before")}',
                                                     callback_data=data_photos_get_add.new(
                                                         action='add_front_before', id='add')),
    'photo_sideways_before': types.InlineKeyboardButton(text=f'{btn("add_sideways_before")}',
                                                        callback_data=data_photos_get_add.new(
                                                            action='add_sideways_before', id='add')),
    'photo_back_before': types.InlineKeyboardButton(text=f'{btn("add_back_before")}',
                                                    callback_data=data_photos_get_add.new(
                                                        action='add_back_before', id='add')),
}

buttons_photos_get_after = {
    'photo_front_after': types.InlineKeyboardButton(text=f'{btn("front_after_get")}',
                                                    callback_data=data_photos_get_add.new(action='front_after_get',
                                                                                          id='get')),
    'photo_sideways_after': types.InlineKeyboardButton(text=f'{btn("sideways_after_get")}',
                                                       callback_data=data_photos_get_add.new(
                                                           action='sideways_after_get', id='get')),
    'photo_back_after': types.InlineKeyboardButton(text=f'{btn("back_after_get")}',
                                                   callback_data=data_photos_get_add.new(action='back_after_get',
                                                                                         id='get')),
}

buttons_photos_get_before = {
    'photo_front_before': types.InlineKeyboardButton(text=f'{btn("front_before_get")}',
                                                     callback_data=data_photos_get_add.new(action='front_before_get',
                                                                                           id='get')),
    'photo_sideways_before': types.InlineKeyboardButton(text=f'{btn("sideways_before_get")}',
                                                        callback_data=data_photos_get_add.new(
                                                            action='sideways_before_get', id='get')),
    'photo_back_before': types.InlineKeyboardButton(text=f'{btn("back_before_get")}',
                                                    callback_data=data_photos_get_add.new(action='back_before_get',
                                                                                          id='get')),
}


async def send_menu_user_info_photos(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup(row_width=2)
    state_data = await state.get_data()
    with db_session:
        user = await Users.get_user(tg_id=query.from_user.id, marathon_id=state_data['marathon_id'])
        if user.marathon.send_measurements_after:
            markup.add(types.InlineKeyboardButton(text=f'{btn("after")}',
                                                  callback_data='after'))
        if user.marathon.send_measurements_before:
            markup.add(types.InlineKeyboardButton(text=f'{btn("before")}',
                                                  callback_data='before'))
    markup.add(back, main_menu)
    await UserInfoMenuPhotos.first()
    await query.message.edit_text('Выберите пункт меню:', reply_markup=markup)


async def send_menu_user_info_photos_choice(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup(row_width=2)
    text = 'Выберите пункт меню '
    data = await state.get_data()
    try:
        choice_data = data['callback_1']
        await state.update_data({'callback_1': data['callback_1']})
    except KeyError:
        choice_data = query.data
        await state.update_data({'callback_1': query.data})
    if 'after' in choice_data:
        for button in buttons_photos_choice_after:
            markup.add(button)
        text += 'ДО:'
    elif 'before' in choice_data:
        for button in buttons_photos_choice_before:
            markup.add(button)
        text += 'ПОСЛЕ:'
    markup.add(back, main_menu)
    await UserInfoMenuPhotos.next()
    await query.message.edit_text(text, reply_markup=markup)


async def send_menu_user_info_photos_add_get(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup(row_width=2)
    data = await state.get_data()
    try:
        choice_data = data['callback_2']
        await state.update_data({'callback_2': data['callback_2']})
    except KeyError:
        choice_data = query.data
        await state.update_data({'callback_2': query.data.split("choice:choice:")[1]})
    with db_session:
        user = await Users.get_user(tg_id=query.from_user.id, marathon_id=data['marathon_id'])
        photo = user.photos
        try:
            callback = states.get(data['callback'])
            await state.update_data({'callback': data['callback']})
        except KeyError:
            callback = states.get(query.data.split('choice:choice:')[1])
            await state.update_data({'callback': query.data})
        if 'after' in choice_data:
            try:
                if getattr(photo, callback):
                    button_add = buttons_photos_add_after[callback]
                    button_add.text = button_add.text.replace('Загрузить', 'Поменять')
                    markup.add(button_add)
                    markup.add(buttons_photos_get_after[callback])
                else:
                    markup.add(buttons_photos_add_after[callback])
            except Exception as exc:
                markup.add(buttons_photos_add_after[callback])
        if 'before' in choice_data:
            try:
                if getattr(photo, callback):
                    button_add = buttons_photos_add_before[callback]
                    button_add.text = button_add.text.replace('Загрузить', 'Поменять')
                    markup.add(button_add)
                    markup.add(buttons_photos_get_before[callback])
                else:
                    markup.add(buttons_photos_add_before[callback])
            except:
                markup.add(buttons_photos_add_before[callback])
    markup.add(back, main_menu)
    await UserInfoMenuPhotos.last()
    try:
        await query.message.edit_text('Выберите пункт меню:', reply_markup=markup)
    except BadRequest:
        await query.message.answer('Выберите пункт меню:', reply_markup=markup)
        await query.message.delete()


async def get_photo_from_db(query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    markup = types.InlineKeyboardMarkup(row_width=2)
    text = "Вы здесь очень красивый(ая)!"
    with db_session:
        user = await Users.get_user(tg_id=query.from_user.id, marathon_id=state_data['marathon_id'])
        photo_from_db = getattr(user.photos, states.get(query.data.split("post:get:")[1].split("_get")[0]))
        photo = open(MEDIA_ROOT + photo_from_db, 'rb')
        markup.add(back, main_menu)
        msg = await query.message.answer_photo(photo, caption=text, reply_markup=markup)
    await query.message.delete()
    await state.update_data({'msg': msg.to_python(),
                             'callback': query.data.split("post:get:")[1].split("_get")[0]})
    await Photos.get_photo.set()


async def send_menu_wait_photo_from_user(query: types.CallbackQuery, state: FSMContext):
    markup = types.InlineKeyboardMarkup(row_width=2)
    text = "Вы должны сделать такую же фотографию"
    markup.add(back, main_menu)
    with db_session:
        try:
            photo_from_db = PhotoStates.get(category_photo=f'{query.data.split("post:add:")[1].split("_")[1]}')
            photo = open(MEDIA_ROOT + photo_from_db.photo, 'rb')
            msg = await query.message.answer_photo(photo, caption=text, reply_markup=markup)
            await query.message.delete()
        except AttributeError:
            msg = await query.message.edit_text(text, reply_markup=markup)
    await state.update_data({'msg': msg.to_python(),
                             'callback': query.data.split("post:add:")[1].split("add_")[1]})
    await Photos.add_photo.set()
