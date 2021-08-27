import configparser
import datetime
import os

import psycopg2
from pony.orm import Database, Required, Set, PrimaryKey, Optional

config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'settings/config.cfg'))
con = psycopg2.connect(**config['database'])

db = Database()
db.bind(**config['database'], provider='postgres')


class Measurement(db.Entity):
    _table_ = 'measurement'
    id = PrimaryKey(int, auto=True)
    waist_before = Optional(float, nullable=True)
    breast_before = Optional(float, nullable=True)
    femur_before = Optional(float, nullable=True)
    weight_before = Optional(float, nullable=True)
    # --------------------------------------------------------
    waist_after = Optional(float, nullable=True)
    breast_after = Optional(float, nullable=True)
    femur_after = Optional(float, nullable=True)
    weight_after = Optional(float, nullable=True)
    user = Optional("Users")

    @staticmethod
    async def get_measurement(measurement_id):
        return Measurement.get(lambda m: m.id == measurement_id)


class Photo(db.Entity):
    _table_ = 'photo'
    id = PrimaryKey(int, auto=True)
    photo_front_before = Optional(str, nullable=True, default='')
    photo_sideways_before = Optional(str, nullable=True, default='')
    photo_back_before = Optional(str, nullable=True, default='')
    # --------------------------------------------------------
    photo_front_after = Optional(str, nullable=True, default='')
    photo_sideways_after = Optional(str, nullable=True, default='')
    photo_back_after = Optional(str, nullable=True, default='')
    user = Optional("Users")

    @staticmethod
    async def get_photo(photo_id):
        return Photo.get(lambda p: p.id == photo_id)


class CategoryTasks(db.Entity):
    _table_ = 'category_tasks'
    id = PrimaryKey(int, auto=True)
    category = Required(str, index=True)
    marathon = Set("Marathon", reverse='category_task', column='marathon_id')
    tasks = Optional('Tasks')


class Tasks(db.Entity):
    _table_ = 'tasks'
    id = PrimaryKey(int, auto=True)
    name = Required(str, index=True, nullable=False)
    category = Required(CategoryTasks, nullable=False, column='category_id')
    description = Required(str, nullable=False)
    count_scopes = Required(int, nullable=False)
    image = Optional(str, nullable=True)
    date_start = Required(datetime.datetime, nullable=False)
    date_stop = Required(datetime.datetime, nullable=False)
    user = Set("Users", column='users_id', reverse='completed_tasks')


class Product(db.Entity):
    _table_ = 'product'
    id = PrimaryKey(int, auto=True)
    name = Required(str, index=True, nullable=False)
    description = Required(str, nullable=False)
    image = Optional(str, nullable=True)
    marathon = Required("Marathon", reverse='product', column='marathon_id')
    user = Set("Users", reverse='purchased_products', column='users_id')


class Marathon(db.Entity):
    _table_ = 'marathon'
    id = PrimaryKey(int, auto=True)
    name = Required(str, index=True, nullable=False)
    description = Required(str, nullable=False)
    date_start = Required(datetime.date)
    date_end = Required(datetime.date)
    send_measurements_before = Optional(bool, sql_default=False)
    send_measurements_after = Optional(bool, sql_default=False)
    close = Optional(bool, sql_default=False)
    price = Optional(int, sql_default=0)
    category_task = Set(CategoryTasks, nullable=True, reverse='marathon', column='category_id')
    product = Optional(Product, nullable=True, cascade_delete=True)
    user = Set("Users", reverse='marathon')
    kcal_category_ready_made = Set('KcalCategoryReadyMadeMenu', nullable=True, reverse='marathon',
                                   column='category_id')
    category_training_menu = Set('CategoryTrainingMenu', nullable=True, reverse='marathon',
                                 column='category_id')
    codes = Optional('Codes', nullable=True, cascade_delete=True)
    invite_code = Optional('InviteCode', nullable=True, reverse='marathon')
    count_users = Required(int)

    @staticmethod
    async def get_marathon(marathon_id):
        return Marathon.get(lambda m: m.id == marathon_id)


class BZUUsers(db.Entity):
    _table_ = 'bzu_users'
    id = PrimaryKey(int, auto=True)

    proteins = Required(int)
    fats = Required(int)
    carbohydrates = Required(int)
    user = Optional("Users", reverse='bzu', index=True)


class Codes(db.Entity):
    _table_ = 'codes'

    id = PrimaryKey(int, auto=True)
    code = Required(str, nullable=False, index=True)
    scopes = Required(int, nullable=False)
    marathon = Required(Marathon, nullable=False, column='marathon_id', reverse='codes')
    user = Set("Users", column='users_id', reverse='entered_codes')


class Users(db.Entity):
    _table_ = 'users'
    id = PrimaryKey(int, auto=True)
    tg_id = Required(int, nullable=False, index=True)
    username = Required(str, nullable=True)
    first_name = Required(str, nullable=False)
    last_name = Required(str, nullable=False)
    scopes = Required(int, nullable=False)
    sex = Optional(str, nullable=True)
    age = Optional(int, nullable=True)
    weight = Optional(int, nullable=True)
    height = Optional(int, nullable=True)
    purpose = Optional(str, nullable=True)
    kcal = Optional(int, nullable=True)
    is_enter_invite_code = Optional(bool, nullable=True)
    marathon = Required(Marathon, nullable=False, reverse='user', column='marathon_id')
    completed_tasks = Set(Tasks, nullable=True, reverse='user', column='tasks_id')
    purchased_products = Set(Product, nullable=True, reverse='user', column='product_id')
    measurement = Optional(Measurement, nullable=True, reverse='user', column='measurement_id', cascade_delete=True)
    photos = Optional(Photo, nullable=True, reverse='user', column='photos_id', cascade_delete=True)
    bzu = Optional(BZUUsers, nullable=True, reverse='user', column='bzu_id', cascade_delete=True)
    entered_codes = Set(Codes, nullable=True, reverse='user', column='codes_id')
    is_pay = Optional(bool)

    @staticmethod
    async def get_user(tg_id, marathon_id):
        return Users.get(lambda u: u.marathon.id == marathon_id and u.tg_id == tg_id)


class PhotoStates(db.Entity):
    _table_ = 'photo_states'

    id = PrimaryKey(int, auto=True)
    category_photo = Required(str)
    photo = Optional(str, nullable=True, default='')


class KcalCategoryReadyMadeMenu(db.Entity):
    _table_ = "kcal_category_ready_made"

    id = PrimaryKey(int, auto=True)
    kcal_category = Required(str)
    day = Set("DayReadyMadeMenu")
    marathon = Set(Marathon, nullable=True, reverse='kcal_category_ready_made', column='marathon_id')


class DayReadyMadeMenu(db.Entity):
    _table_ = "day_ready_made"

    id = PrimaryKey(int, auto=True)
    day = Required(str, index=True)
    kcal_category = Required(KcalCategoryReadyMadeMenu, nullable=False, reverse='day', column='kcal_category_id')
    time_day = Set('TimeDayReadyMadeMenu')


class TimeDayReadyMadeMenu(db.Entity):
    _table_ = "time_day_ready_made"

    id = PrimaryKey(int, auto=True)
    time_day = Required(str, index=True)
    day = Required(DayReadyMadeMenu, nullable=False, reverse='time_day', column='day_id')
    menu = Set('ReadyMadeMenu')


class ReadyMadeMenu(db.Entity):
    _table_ = "ready_made"

    id = PrimaryKey(int, auto=True)
    name_menu = Required(str, index=True)
    description = Required(str)
    time_day = Required(TimeDayReadyMadeMenu, nullable=False, reverse='menu', column='time_day_id')
    photo = Optional(str, nullable=True, default='', column='photo')


class CategoryTrainingMenu(db.Entity):
    _table_ = 'category_training'

    id = PrimaryKey(int, auto=True)
    category = Required(str, nullable=False)
    recipes = Optional('TrainingInfo')
    marathon = Set(Marathon, nullable=True, reverse='category_training_menu', column='marathon_id')


class TrainingInfo(db.Entity):
    _table_ = 'training_info'

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Required(str)
    category = Required(CategoryTrainingMenu, column='category_id')
    photo = Optional(str, nullable=True, default='', column='photo')


class AllUsers(db.Entity):
    _table_ = 'all_users'
    id = PrimaryKey(int, auto=True)
    tg_id = Required(int, unique=True)


class InviteCode(db.Entity):
    _table_ = 'invite_code'
    marathon = Required(Marathon, column='marathon_id')
    code = Required(str)
    date_delete = Required(datetime.datetime)


class ButtonsText(db.Entity):
    _table_ = 'btn_text'
    main_menu_tasks = Required(str)
    main_menu_user_info = Required(str)
    main_menu_kcal = Required(str)
    main_menu_get_scopes = Required(str)
    main_menu_buy_product = Required(str)
    marathon_switch = Required(str)
    back = Required(str)
    main_menu = Required(str)
    user_info_measurement_choice = Required(str)
    user_info_photos_choice = Required(str)
    stats_all = Required(str)
    kcal = Required(str)
    ready_made_menu = Required(str)
    training = Required(str)
    measurement_after = Required(str)
    measurement_before = Required(str)
    after = Required(str)
    before = Required(str)
    front_after = Required(str)
    sideways_after = Required(str)
    back_after = Required(str)
    front_before = Required(str)
    sideways_before = Required(str)
    back_before = Required(str)
    add_front_after = Required(str)
    add_sideways_after = Required(str)
    add_back_after = Required(str)
    add_front_before = Required(str)
    add_sideways_before = Required(str)
    add_back_before = Required(str)
    replace_add_front_after = Required(str)
    replace_add_sideways_after = Required(str)
    replace_add_back_after = Required(str)
    replace_add_front_before = Required(str)
    replace_add_sideways_before = Required(str)
    replace_add_back_before = Required(str)
    front_after_get = Required(str)
    sideways_after_get = Required(str)
    back_after_get = Required(str)
    front_before_get = Required(str)
    sideways_before_get = Required(str)
    back_before_get = Required(str)


class BotConfig(db.Entity):
    _table_ = 'bot_cfg'
    name_bot = Required(str)
    bot_token = Required(str)
    pay_token = Required(str)
    admin_id = Required(int)


db.generate_mapping(create_tables=True)
