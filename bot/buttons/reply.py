from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.buttons.text import *


def menu_btn():
    k1 = KeyboardButton(text = presentation_txt)
    k2 = KeyboardButton(text = referat_mustaqil_ish_txt)
    k3 = KeyboardButton(text = balans_txt)
    k4 = KeyboardButton(text=qollanma_txt)
    design = [
        [k1 , k2],
        [k3 , k4]
    ]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)

