from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.buttons.text import *

def TIL():
    uz_btn = InlineKeyboardButton(text=uz_txt, callback_data=uz_txt)
    en_btn = InlineKeyboardButton(text=rys_txt, callback_data=rys_txt)
    rus_btn = InlineKeyboardButton(text=eng_txt, callback_data=eng_txt)
    return InlineKeyboardMarkup(inline_keyboard=[[uz_btn ],[ en_btn],[rus_btn]])

def Sahifalar_soni():
    besh_on_btn = InlineKeyboardButton(text=besh_on, callback_data=besh_on)
    en_btn = InlineKeyboardButton(text=on_onbesh, callback_data=on_onbesh)
    rus_btn = InlineKeyboardButton(text=onbesh_yigirma, callback_data=onbesh_yigirma)
    yigirma_yigirmabesh_btn = InlineKeyboardButton(text=yigirma_yigirmabesh,callback_data=yigirma_yigirmabesh)
    return InlineKeyboardMarkup(inline_keyboard=[[besh_on_btn ],[ en_btn],[rus_btn],[yigirma_yigirmabesh_btn]])
def send():
    send_btn = InlineKeyboardButton(text="🚀 Send", url=send_txt,)
    return InlineKeyboardMarkup(inline_keyboard=[[send_btn]])

def buy_method():
    payme_btn =  InlineKeyboardButton(text="🟢 Payme", callback_data=payme_txt,)
    click_btn = InlineKeyboardButton(text="🔵 Click", callback_data=click_txt)
    return InlineKeyboardMarkup(inline_keyboard=[[payme_btn],[click_btn]])