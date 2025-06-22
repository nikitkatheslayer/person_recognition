from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_button_start():
    button_start = InlineKeyboardButton(
        text="Начать",
        callback_data="start"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_start]]
    )
    return keyboard

