from aiogram import Dispatcher
from aiogram.types import ContentType

from marathon_bot.handlers import data_kcal_welcome_menu
from marathon_bot.handlers.user_info_measurement_handler import data_measurement
from marathon_bot.scenarios.handler_calculation_kcal import send_first_scenario_message_calculate_kcal, set_height, \
    set_age, set_sex, set_purpose, successfully, set_weight_kcal, data_activity
from marathon_bot.scenarios.handler_register import send_welcome, check_register_from_marathon, register_marathon, \
    none_register_marathon, get_full_name, process_pre_checkout_query, process_successful_payment
from marathon_bot.scenarios.handler_set_measurement import set_weight_measurement, \
    send_first_scenario_message_measurement, set_breast, set_waist, set_femur
from marathon_bot.scenarios.photo_scenario_handler import add_photo_to_db
from marathon_bot.states.all_states_menu import CalculationOfKBZUMenu, UserInfoMenuMeasurement
from marathon_bot.states.state_scenarios import CalculateKcal, Register, MeasurementState, Photos


def calculate_kcal_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_first_scenario_message_calculate_kcal,
                                       data_kcal_welcome_menu.filter(id=['kcal']),
                                       state=CalculationOfKBZUMenu.choice_menu)
    dp.register_message_handler(set_weight_kcal, state=CalculateKcal.set_weight)
    dp.register_message_handler(set_height, state=CalculateKcal.set_height)
    dp.register_message_handler(set_age, state=CalculateKcal.set_age)
    dp.register_callback_query_handler(set_sex, state=CalculateKcal.set_sex)
    dp.register_callback_query_handler(set_purpose, state=CalculateKcal.choice_purpose)
    dp.register_callback_query_handler(successfully, data_activity.filter(id=['activity']),
                                       state=CalculateKcal.choice_activity)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, state="*", commands=['start'])
    dp.register_callback_query_handler(check_register_from_marathon, lambda query: '_marathon' in query.data,
                                       state=Register.choice_marathon)
    dp.register_callback_query_handler(register_marathon, lambda query: 'Register_from_Marathon' in query.data,
                                       state=Register.check_register)
    dp.register_callback_query_handler(none_register_marathon, lambda query: "None" == query.data,
                                       state=Register.check_register)
    dp.register_callback_query_handler(none_register_marathon, lambda query: "marathon_switch" == query.data,
                                       state='*')
    dp.register_message_handler(get_full_name, state=Register.register_in_marathon)
    dp.register_pre_checkout_query_handler(process_pre_checkout_query, state="*")
    dp.register_message_handler(process_successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT, state="*")


def measurements_handler(dp: Dispatcher):
    dp.register_callback_query_handler(send_first_scenario_message_measurement,
                                       data_measurement.filter(action=['measurement_after', 'measurement_before']),
                                       state=UserInfoMenuMeasurement.measurement_user_info)
    dp.register_message_handler(set_breast, state=MeasurementState.set_breast)
    dp.register_message_handler(set_waist, state=MeasurementState.set_waist)
    dp.register_message_handler(set_femur, state=MeasurementState.set_femur)
    dp.register_message_handler(set_weight_measurement, state=MeasurementState.set_weight)


def photo_handler(dp: Dispatcher):
    dp.register_message_handler(add_photo_to_db, content_types=['document', 'photo'],
                                state=Photos.add_photo)
