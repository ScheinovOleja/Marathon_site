import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from pony.orm import db_session
from psycopg2.extras import NamedTupleCursor

from marathon_bot import con, bot, config
from marathon_bot.handlers.main_menu_handler import send_main_menu
from marathon_bot.models import Marathon, Users
from marathon_bot.states.all_states_menu import MainMenu
from marathon_bot.states.state_scenarios import Register


@db_session
async def send_welcome(message: types.Message, action='send'):
    marathons = Marathon.select().order_by(Marathon.id)[:]
    markup = types.InlineKeyboardMarkup()
    users = Users.select().where(tg_id=message.chat.id)[:]
    for marathon in marathons:
        if not marathon.date_start <= datetime.datetime.now().date() < marathon.date_end:
            continue
        text = f"{marathon.name}"
        if any([user for user in users if user.marathon == marathon]):
            text += " ✅️"
        if marathon.price > 0:
            text += " 💎"
        else:
            text += " 🆓"
        if marathon.close:
            text += " 🔒"
        else:
            text += " 🔓"
        markup.add(
            types.InlineKeyboardButton(
                text=text,
                callback_data=marathon.name + '_marathon')
        )
    if action == 'send':
        await message.answer("Добро пожаловать!\nСписок доступных на данный момент марафонов:\n\n"
                             "🔒/🔓 - закрытый/открытый марафон\n"
                             "💎/🆓 - платный/бесплатный марафон\n"
                             "✅ - вы зарегистрированы в марафоне\n", reply_markup=markup)
    elif action == 'edit':
        await message.edit_text("Добро пожаловать!\nСписок доступных на данный момент марафонов:", reply_markup=markup)
    await Register.choice_marathon.set()


@db_session
async def check_register_from_marathon(query: types.CallbackQuery, state: FSMContext):
    cur = con.cursor(cursor_factory=NamedTupleCursor)
    cur.execute(
        f"""
            SELECT pam.id
            FROM marathon as pam
            INNER JOIN users as pau ON pam.id = pau.marathon_id
            WHERE pau.tg_id = {query.from_user.id} AND pam.name = \'{query.data.split("_marathon")[0]}\'
        """
    )
    marathon = cur.fetchone()
    if not marathon:
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                text='Да',
                callback_data=f'Register_from_Marathon_{query.data.split("_marathon")[0]}')
        )
        markup.add(
            types.InlineKeyboardButton(
                text='Нет',
                callback_data='None')
        )
        marathon = Marathon.get(name=query.data.split('_marathon')[0])
        await query.message.edit_text(
            f"{marathon.description}\n\nХотите зарегистрироваться?",
            reply_markup=markup,
        )
        await Register.next()
        await state.update_data({'marathon_id': marathon.id})
    else:
        await MainMenu.main_menu.set()
        await state.set_data({'marathon_id': marathon.id})
        await send_main_menu(query, state)


async def none_register_marathon(query: types.CallbackQuery):
    await Register.choice_marathon.set()
    await send_welcome(message=query.message, action='edit')


@db_session
async def register_marathon(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    marathon = await Marathon.get_marathon(marathon_id=data['marathon_id'])
    if marathon.price > 0.0:
        prices = [types.LabeledPrice(label=marathon.name, amount=marathon.price * 100)]
        await query.message.delete()
        await bot.send_invoice(
            query.message.chat.id,
            title=marathon.name,
            description=marathon.description,
            provider_token=config['bot']['PAY'],
            currency='rub',
            prices=prices,
            need_name=True,
            need_email=True,
            need_phone_number=True,
            start_parameter='time-machine-example',
            payload='register-marathon-payments'
        )
    else:
        msg = await query.message.edit_text(
            "Доброго времени суток!\nПрошу заполнять данные верно, так как в дальнейшем они будут использоваться "
            "для подсчета данных!\n Как вас зовут?(Напишите ваши Фамилию и Имя через пробел)\n"
            "❗️ Например: Иванова Мария"
        )
        await state.update_data({'msg': msg.to_python()})
        await Register.next()


async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_successful_payment(message: types.Message, state: FSMContext):
    msg = await message.answer(
        "Доброго времени суток!\nПрошу заполнять данные верно, так как в дальнейшем они будут использоваться "
        "для подсчета данных!\n Как вас зовут?(Напишите ваши Фамилию и Имя через пробел)\n"
        "❗️ Например: Иванова Мария"
    )
    await state.update_data({'msg': msg.to_python()})
    await Register.next()


async def get_full_name(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    try:
        sql = "insert into users(tg_id, username, first_name, last_name, scopes, marathon_id) values " \
              f"(\'{message.from_user.id}\', \'{message.from_user.username if message.from_user.username else '-'}\'," \
              f"\'{message.text.split(' ')[1]}\', \'{message.text.split(' ')[0]}\', 0, {state_data['marathon_id']})"
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
    except Exception as exc:
        failure_text = "Что-то пошло не так. Повторите попытку! (Напишите ваши Фамилию и Имя через пробел)\n" \
                       "❗️Например: Иванова Мария"
        if state_data['msg']['text'] == failure_text:
            pass
        else:
            msg = await bot.edit_message_text(failure_text, state_data['msg']['chat']['id'],
                                              state_data['msg']['message_id'])
            await state.update_data({'msg': msg.to_python()})
        await message.delete()
        return
    await state.update_data({"marathon_id": state_data['marathon_id'], 'msg': state_data['msg']})
    await send_main_menu(types.CallbackQuery(message=message), state)
    await message.delete()
