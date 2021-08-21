from aiogram.dispatcher.filters.state import StatesGroup, State


class MainMenu(StatesGroup):
    main_menu = State()


class GetScopes(StatesGroup):
    waiting_code = State()


class TaskMenu(StatesGroup):
    list_category_tasks = State()
    list_tasks_from_category = State()
    task_info = State()


class UserInfoMenu(StatesGroup):
    choice_menu_user_info = State()


class UserInfoMenuMeasurement(StatesGroup):
    measurement_user_info = State()


class UserInfoMenuPhotos(StatesGroup):
    photos_user_info = State()
    photos_user_info_states = State()
    photos_user_info_choice = State()


class CalculationOfKBZUMenu(StatesGroup):
    choice_menu = State()


class ReadyMadeMenuState(StatesGroup):
    list_kcal_ready_made_menu = State()
    list_day_ready_made_menu = State()
    list_day_time_ready_made = State()
    list_ready_made_menus_by_day_time = State()
    menu_from_ready_made_info = State()


class TrainingMenu(StatesGroup):
    list_category_menu_training = State()
    list_menu_from_training = State()
    menu_training_info = State()


class StatsMenu(StatesGroup):
    stats_menu = State()


class ProductsMenu(StatesGroup):
    list_products = State()
    product_info = State()
