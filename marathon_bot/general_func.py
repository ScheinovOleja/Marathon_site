from aiogram import types

from marathon_bot import MEDIA_ROOT


async def send_photo(query: types.CallbackQuery, text, markup, photo):
    try:
        photo = open(MEDIA_ROOT + photo, 'rb')
        await query.message.answer_photo(photo=photo, caption=text,
                                         reply_markup=markup)
        await query.message.delete()
        return
    except FileNotFoundError:
        await query.message.edit_text(text, reply_markup=markup)
        return
