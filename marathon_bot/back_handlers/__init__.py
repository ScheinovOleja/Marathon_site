from aiogram import Dispatcher

from marathon_bot.back_handlers.ready_made_back import back_to_send_category, back_to_all_day, back_to_time_day, \
    back_to_menu_list, back_to_kcal_welcome
from marathon_bot.back_handlers.task_back import back_to_category, back_to_list_tasks
from marathon_bot.back_handlers.training_menu_back import back_to_category_training, back_to_list_menus
from marathon_bot.back_handlers.user_photo_back import back_user_info_photos, back_to_user_info_photo_choice, \
    back_to_user_info_add_get
from marathon_bot.states.all_states_menu import TrainingMenu, ReadyMadeMenuState, TaskMenu, UserInfoMenuPhotos
from marathon_bot.states.state_scenarios import Photos, CalculateKcal


def back_training_menu(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_category_training, lambda query: 'back' == query.data,
                                       state=TrainingMenu.list_menu_from_training)
    dp.register_callback_query_handler(back_to_list_menus, lambda query: 'back' == query.data,
                                       state=TrainingMenu.menu_training_info)


def back_ready_made(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_kcal_welcome, lambda query: 'back' == query.data,
                                       state=[ReadyMadeMenuState.list_kcal_ready_made_menu,
                                              TrainingMenu.list_category_menu_training,
                                              CalculateKcal.set_weight])
    dp.register_callback_query_handler(back_to_send_category, lambda query: 'back' == query.data,
                                       state=ReadyMadeMenuState.list_day_ready_made_menu)
    dp.register_callback_query_handler(back_to_all_day, lambda query: 'back' == query.data,
                                       state=ReadyMadeMenuState.list_day_time_ready_made)
    dp.register_callback_query_handler(back_to_time_day, lambda query: 'back' == query.data,
                                       state=ReadyMadeMenuState.list_ready_made_menus_by_day_time)
    dp.register_callback_query_handler(back_to_menu_list, lambda query: 'back' == query.data,
                                       state=ReadyMadeMenuState.menu_from_ready_made_info)


def back_task(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_category, lambda query: 'back' == query.data,
                                       state=TaskMenu.list_tasks_from_category)
    dp.register_callback_query_handler(back_to_list_tasks, lambda query: 'back' == query.data,
                                       state=TaskMenu.task_info)


def back_photos_user(dp: Dispatcher):
    dp.register_callback_query_handler(back_user_info_photos,
                                       lambda query: 'back' == query.data,
                                       state=UserInfoMenuPhotos.photos_user_info_states)
    dp.register_callback_query_handler(back_to_user_info_photo_choice,
                                       lambda query: 'back' == query.data,
                                       state=UserInfoMenuPhotos.photos_user_info_choice)
    dp.register_callback_query_handler(back_to_user_info_add_get,
                                       lambda query: 'back' == query.data,
                                       state=[Photos.get_photo, Photos.add_photo])
