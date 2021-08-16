from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    choice_marathon = State()
    check_register = State()
    register_in_marathon = State()
    set_full_name = State()


class MeasurementState(StatesGroup):
    set_breast = State()
    set_waist = State()
    set_femur = State()
    set_weight = State()


class Photos(StatesGroup):
    add_photo = State()
    get_photo = State()


class CalculateKcal(StatesGroup):
    set_weight = State()
    set_height = State()
    set_age = State()
    set_sex = State()
    choice_purpose = State()
    choice_activity = State()
