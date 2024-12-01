from aiogram.fsm.state import StatesGroup, State


class PPTState(StatesGroup):
    ppt_name = State()
    ppt_slide_count = State()
class ReferatState(StatesGroup):
    univer_name = State()
    referat_mavzusi = State()
    referat_muallif = State()
    referat_tili = State()
    referat_sahifa_soni = State()