from aiogram import Dispatcher

from marathon_bot.handlers.all_stats_handler import send_stats
from marathon_bot.handlers.kcal_menu_handler import send_menu_kcal_welcome, data_kcal_welcome_menu
from marathon_bot.handlers.main_menu_handler import send_main_menu
from marathon_bot.handlers.product_handler import send_products, send_product_info, back_to_send_products
from marathon_bot.handlers.ready_made_menu_handler import send_category_ready_made_menu, send_all_day, send_time_day, \
    send_ready_made_menu_list, send_info_by_ready_made_menu
from marathon_bot.handlers.scopes_by_code_handler import send_codes_message, get_code
from marathon_bot.handlers.tasks_handler import send_category_tasks, send_tasks, send_task_info
from marathon_bot.handlers.training_menu_handler import send_category_training, send_training_menus, send_menu_info
from marathon_bot.handlers.user_info_measurement_handler import send_menu_user_info, send_menu_user_info_measurement, \
    back_to_menu_user_info, back_to_menu_user_info_measurement
from marathon_bot.handlers.user_info_photo_handler import send_menu_user_info_photos, send_menu_user_info_photos_choice, \
    send_menu_user_info_photos_add_get, data_photos_choice, send_menu_wait_photo_from_user, data_photos_get_add, \
    get_photo_from_db
from marathon_bot.states.all_states_menu import MainMenu, TaskMenu, UserInfoMenu, CalculationOfKBZUMenu, \
    ReadyMadeMenuState, TrainingMenu, ProductsMenu, GetScopes, UserInfoMenuMeasurement, UserInfoMenuPhotos
from marathon_bot.states.state_scenarios import MeasurementState


def all_stats_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_stats, lambda query: "stats_all" == query.data, state=MainMenu.main_menu)


def kcal_menu_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_menu_kcal_welcome, lambda query: 'main_menu_kcal' == query.data,
                                       state=MainMenu.main_menu)


def product_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_products, lambda query: 'main_menu_buy_product' == query.data,
                                       state="*")
    dp.register_callback_query_handler(send_product_info, lambda query: 'Product_' in query.data,
                                       state=ProductsMenu.list_products)
    dp.register_callback_query_handler(back_to_send_products, lambda query: 'back' == query.data,
                                       state=ProductsMenu.product_info)


def ready_made_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_category_ready_made_menu,
                                       data_kcal_welcome_menu.filter(id=['ready_made_menu']),
                                       state=CalculationOfKBZUMenu.choice_menu)
    dp.register_callback_query_handler(send_all_day, lambda query: 'Kcal_' in query.data,
                                       state=ReadyMadeMenuState.list_kcal_ready_made_menu)
    dp.register_callback_query_handler(send_time_day,
                                       lambda query: 'Day_' in query.data,
                                       state=ReadyMadeMenuState.list_day_ready_made_menu)
    dp.register_callback_query_handler(send_ready_made_menu_list,
                                       lambda query: 'Time_' in query.data,
                                       state=ReadyMadeMenuState.list_day_time_ready_made)
    dp.register_callback_query_handler(send_info_by_ready_made_menu,
                                       lambda query: 'Menu_' in query.data,
                                       state=ReadyMadeMenuState.list_ready_made_menus_by_day_time)


def scopes_by_code_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_codes_message, lambda query: "main_menu_get_scopes" == query.data,
                                       state=MainMenu.main_menu)
    dp.register_message_handler(get_code, state=GetScopes.waiting_code)


def tasks_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_category_tasks, lambda query: 'main_menu_tasks' == query.data, state='*')
    dp.register_callback_query_handler(send_tasks, lambda query: 'Category_' in query.data,
                                       state=TaskMenu.list_category_tasks)
    dp.register_callback_query_handler(send_task_info, lambda query: 'Task_' in query.data,
                                       state=TaskMenu.list_tasks_from_category)


def training_menu_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_category_training,
                                       lambda query: 'training' == query.data, state='*')
    dp.register_callback_query_handler(send_training_menus, lambda query: 'Training_' in query.data,
                                       state=TrainingMenu.list_category_menu_training)
    dp.register_callback_query_handler(send_menu_info, lambda query: 'Menu_' in query.data,
                                       state=TrainingMenu.list_menu_from_training)


def user_info_measurement_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_menu_user_info, lambda query: "main_menu_user_info" == query.data,
                                       state=MainMenu.main_menu)
    dp.register_callback_query_handler(send_menu_user_info_measurement,
                                       lambda query: "user_info_measurement_choice" == query.data,
                                       state=UserInfoMenu.choice_menu_user_info)
    dp.register_callback_query_handler(back_to_menu_user_info, lambda query: 'back' == query.data,
                                       state=[UserInfoMenuMeasurement.measurement_user_info,
                                              UserInfoMenuPhotos.photos_user_info])
    dp.register_callback_query_handler(back_to_menu_user_info_measurement, lambda query: 'back' == query.data,
                                       state=MeasurementState.set_breast)


def user_info_photo_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_menu_user_info_photos,
                                       lambda query: "user_info_photos_choice" == query.data,
                                       state=UserInfoMenu.choice_menu_user_info)
    dp.register_callback_query_handler(send_menu_user_info_photos_choice,
                                       lambda query: 'after' == query.data or 'before' == query.data,
                                       state=UserInfoMenuPhotos.photos_user_info)
    dp.register_callback_query_handler(send_menu_user_info_photos_add_get,
                                       data_photos_choice.filter(id='choice'),
                                       state=UserInfoMenuPhotos.photos_user_info_states)
    dp.register_callback_query_handler(send_menu_wait_photo_from_user,
                                       data_photos_get_add.filter(id='add'),
                                       state=UserInfoMenuPhotos.photos_user_info_choice)
    dp.register_callback_query_handler(get_photo_from_db,
                                       data_photos_get_add.filter(id='get'),
                                       state=UserInfoMenuPhotos.photos_user_info_choice)


def commons_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_main_menu, lambda query: "main_menu" == query.data,
                                       state='*')
