from aiogram import types
from aiogram.dispatcher import FSMContext
from pony.orm import commit, db_session

from marathon_bot import bot
from marathon_bot.handlers.main_menu_handler import back, main_menu
from marathon_bot.handlers.user_info_photo_handler import states
from marathon_bot.models import Users, Photo
from marathon_bot.states.state_scenarios import Photos


async def add_photo_to_db(message: types.Message, state: FSMContext):
    markup = types.InlineKeyboardMarkup(row_width=2)
    state_data = await state.get_data()
    if message.content_type == 'document':
        file = await bot.download_file_by_id(message.document.file_id)
    elif message.content_type == 'photo':
        try:
            file = await bot.download_file_by_id(message.photo[-1].file_id)
        except Exception as exc:
            file = await bot.download_file_by_id(message.photo[-2].file_id)
    else:
        return
    with db_session:
        user = await Users.get_user(tg_id=message.from_user.id, marathon_id=state_data['marathon_id'])
        if user.photos is None:
            photo = Photo()
            commit()
        else:
            photo = await Photo.get_photo(photo_id=user.photos.id)
        setattr(photo, states.get(state_data['callback']), file.read())
        user.photos = photo.id
    await message.delete()
    markup.add(back, main_menu)
    await Photos.add_photo.set()
    await bot.delete_message(state_data['msg']['chat']['id'], state_data['msg']["message_id"])
    await message.answer('Спасибо! Вы очень красивы!',
                         reply_markup=markup)
    # await state.set_data({'marathon_id': state_data['marathon_id']})
