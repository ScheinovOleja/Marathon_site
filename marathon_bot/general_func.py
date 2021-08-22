from aiogram import types
from pony.orm import db_session

from marathon_bot import MEDIA_ROOT, con


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


@db_session
def btn(call: str):
    cur = con.cursor()
    cur.execute(
        f"""
                SELECT bt.{call}
                FROM btn_text as bt
            """
    )
    text = cur.fetchone()
    return text[0]
