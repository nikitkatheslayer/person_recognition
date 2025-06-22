from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_button_photo():
    button_analysis = KeyboardButton(text="Проанализировать🔍")
    button_ident = KeyboardButton(text="Идентифицировать🔍")

    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [button_analysis],
            [button_ident]
        ]
    )
    return keyboard

def get_button_ident():
    button_ident = KeyboardButton(text="Идентифицировать🔍")

    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[button_ident]]
    )
    return keyboard

