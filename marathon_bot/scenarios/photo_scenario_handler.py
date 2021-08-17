import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from pony.orm import commit, db_session

from marathon_bot import bot, MEDIA_ROOT
from marathon_bot.handlers.main_menu_handler import back, main_menu
from marathon_bot.handlers.user_info_photo_handler import states
from marathon_bot.models import Users, Photo
from marathon_bot.states.state_scenarios import Photos


async def add_photo_to_db(message: types.Message, state: FSMContext):
    markup = types.InlineKeyboardMarkup(row_width=2)
    state_data = await state.get_data()
    file_path = MEDIA_ROOT + 'users_photo'
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    if not os.path.isdir(file_path + f'/{message.chat.id}'):
        os.mkdir(file_path + f'/{message.chat.id}')
    if message.content_type == 'document':
        name_file = message.document.file_unique_id
        state_file = state_data['callback']
        file = await message.document.download(f'{file_path}/{message.chat.id}/{name_file}_{state_file}.jpg')
    elif message.content_type == 'photo':
        try:
            name_file = message.photo[-1].file_unique_id
            state_file = state_data['callback']
            file = await message.photo[-1].download(f'{file_path}/{message.chat.id}/{name_file}_{state_file}.jpg')
        except Exception as exc:
            name_file = message.photo[-2].file_unique_id
            state_file = state_data['callback']
            file = await message.photo[-2].download(f'{file_path}/{message.chat.id}/{name_file}_{state_file}.jpg')
    else:
        return
    with db_session:
        user = await Users.get_user(tg_id=message.from_user.id, marathon_id=state_data['marathon_id'])
        if user.photos is None:
            photo = Photo()
            commit()
        else:
            photo = await Photo.get_photo(photo_id=user.photos.id)
        setattr(photo, states.get(state_data['callback']), file.name.split("users_photo/")[1])
        user.photos = photo
    await message.delete()
    markup.add(back, main_menu)
    await Photos.add_photo.set()
    await bot.delete_message(state_data['msg']['chat']['id'], state_data['msg']["message_id"])
    await message.answer('Спасибо! Вы очень красивы!',
                         reply_markup=markup)
    # await state.set_data({'marathon_id': state_data['marathon_id']})
