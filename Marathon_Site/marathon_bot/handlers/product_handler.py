from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton
from aiogram.utils.exceptions import BadRequest
from pony.orm import db_session

from marathon_bot.general_func import send_photo
from marathon_bot.handlers.main_menu_handler import main_menu, back
from marathon_bot.models import Product
from marathon_bot.states.all_states_menu import ProductsMenu


@db_session
async def send_products(query: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup()
    data = await state.get_data()
    all_product = Product.select().where(marathon=data['marathon_id'])[:]
    text = 'Выберите товар:'
    if not all_product:
        text = 'Извините, но на данный момент нет ни одного приза'
    for product in all_product:
        markup.add(InlineKeyboardButton(text=f'{product.name}', callback_data=f'Product_{product.id}'))
    markup.add(main_menu)
    await ProductsMenu.first()
    try:
        await query.message.edit_text(text, reply_markup=markup)
    except BadRequest:
        await query.message.delete()
        await query.message.answer(text, reply_markup=markup)


async def back_to_send_products(query: CallbackQuery, state: FSMContext):
    await ProductsMenu.previous()
    return await send_products(query, state)


@db_session
async def send_product_info(query: CallbackQuery, state: FSMContext):
    await state.update_data({'callback': query.data})
    markup = InlineKeyboardMarkup()
    product = Product.get(id=query.data.split('_')[1])
    text = f'{product.name}\n\n' \
           f'{product.description}\n\n'
    markup.add(back, main_menu)
    if product.image:
        await send_photo(query, text, markup, product.image)
    else:
        await query.message.edit_text(text, reply_markup=markup)
    await ProductsMenu.next()
