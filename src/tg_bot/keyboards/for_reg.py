from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_button_phone():
    button_phone = KeyboardButton(
        text="Поделиться номером телефона",
        request_contact=True
    )
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[[button_phone]]
    )
    return keyboard

def get_button_reg():
    button_reg = InlineKeyboardButton(
        text="Зарегистрироваться",
        callback_data="reg"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_reg]]
    )
    return keyboard

